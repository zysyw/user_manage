import tempfile
from flask_security import auth_token_required
import opendssdirect as dss
from flask import Blueprint, jsonify, render_template
import json
import re
from app import app, db
from opendss_data.data_modles import *
from opendss_calculation.error_class import NoConvergedError

transformer_losses = {}
line_losses = {}

def run_opendss(opendss_script, new_process):
    global transformer_losses, line_losses
    # 初始化 OpenDSS
    dss.Basic.Start(0)
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        # 写入数据到临时文件
        temp_file.write(opendss_script)
        
    opendss_script_filename = temp_file.name
     
    # 执行opendss脚本命令 
    dss.run_command(f"Redirect [{opendss_script_filename}]")
    
    # 在使用完成后，删除临时文件
    import os
    os.unlink(opendss_script_filename)

    # 初始化 OpenDSS
    transformer_losses = {}
    line_losses = {}
    hourly_voltages = {}
    hourly_currents = {}
    dss.Solution.Number(1)
    # 以下程序在solve的时候可能出现不收敛，增加错误处理
    for hour in range(24): # 这个24有点生硬，今后应修改
        dss.Solution.Solve()
        if dss.Solution.Converged():
            raise NoConvergedError(hour)
        hourly_voltages[hour] = dict(zip(dss.Circuit.AllNodeNames(), dss.Circuit.AllBusVMag()))
        hourly_currents[hour] = get_line_currents()
        # 累加每个小时的元件损耗
        # 过滤以 "Sub" 开头或以 "publictransformer" 结尾的变压器，即公用变压器
        pattern = r"^(sub)|(.*publictransformer)$"
        transformer_losses = add_transformer_losses(transformer_losses, get_transformer_losses(filter_pattern=pattern))
        line_losses = add_line_losses(line_losses, get_line_losses())

    save_opendss_voltages(new_process, hourly_voltages)
    save_opendss_currents(new_process, hourly_currents)
    save_opendss_losses(new_process, transformer_losses, line_losses)
    
    return {"Load Flow Completed": "Yes" if dss.Solution.Converged() else "No"}

def save_opendss_voltages(new_process, hourly_voltages):
    transformed_voltages = {}
    for hour, voltages in hourly_voltages.items():
        for index, (node_name, voltage) in enumerate(voltages.items()):
            # 每隔三个节点取一个值
            if index % 3 != 0:
                continue
            
            # 去掉节点名称结尾的 ".1"
            if node_name.endswith(".1"):
                node_name = node_name[:-2]  # 删除最后两个字符，即 ".1"
                
            # 如果节点名称不在新结构的字典中，则创建一个新的节点名称条目
            if node_name not in transformed_voltages:
                transformed_voltages[node_name] = {}
                
            # 将该小时的电压值添加到相应的节点名称条目中
            transformed_voltages[node_name][hour] = voltage

    # 将每个节点的电压值存储到 VI 和 VIHourValue 表中       
    for node_name, voltages in transformed_voltages.items():
        # 创建或获取与当前节点名称相关联的 VI 实例
        vi_instance = VI.create(
            calculation_process=new_process,
            component_name=node_name,
            unit = 'V'  # 电压单位是 kV
        )
        
        # 将每个小时的电压值存储到 VIHourValue 表中
        for hour, voltage in voltages.items():
            VIHourValue.create(
                vi=vi_instance,
                hour=hour,
                value=voltage
            )

def get_line_currents():
    
    line_names = dss.Lines.AllNames()
    currents_data = {}

    for name in line_names:
        dss.Lines.Name(name)
        currents = dss.CktElement.CurrentsMagAng()
        currents_data[name] = currents[0] # 只取A相电流幅值
        
    return currents_data

def save_opendss_currents(new_process, hourly_currents):
    transformed_currents = {}
    for hour, currents in hourly_currents.items():
        for line_name, current in currents.items():                
            # 如果节点名称不在新结构的字典中，则创建一个新的节点名称条目
            if line_name not in transformed_currents:
                transformed_currents[line_name] = {}
                
            # 将该小时的电流值添加到相应的线路名称条目中
            transformed_currents[line_name][hour] = current

    # 将每条线路的电流值存储到 VI 和 VIHourValue 表中       
    for line_name, currents in transformed_currents.items():
        # 创建或获取与当前节点名称相关联的 VI 实例
        vi_instance = VI.create(
            calculation_process=new_process,
            component_name=line_name,
            unit = 'A'  # 电压单位是 kV
        )
        
        # 将每个小时的电流值存储到 VIHourValue 表中
        for hour, current in currents.items():
            VIHourValue.create(
                vi=vi_instance,
                hour=hour,
                value=current
            )

@app.route('/show_first-meter')
@auth_token_required
def get_opendss_meters():
    meter_names = dss.Meters.RegisterNames()
    meter_values = dss.Meters.RegisterValues()
    registers = zip(meter_names, meter_values)
    
    return render_template('show_meter_registers.html', registers=registers,)

@app.route('/api/circut-losses')
@auth_token_required
def get_circut_losses():
    global transformer_losses, line_losses
    # 收集 EnergyMeter 数据
    dss.Meters.First()
    meter_data = {}
    json_data = 'Null'
    while True:
        name = dss.Meters.Name()
        registers = dss.Meters.RegisterNames()
        values = dss.Meters.RegisterValues()
        meter_data[name] = dict(zip(registers, values))
        if not dss.Meters.Next() > 0:
            break

    # 整合所有数据并转换为 JSON
    all_data = {
        "EnergyMeters": meter_data,
        "TransformerLosses": transformer_losses,
        "LineLosses": line_losses
    }
    json_data = json.dumps(all_data)

    # 输出 JSON 数据或进行后续处理
    return jsonify(json_data)

def get_transformer_losses(filter_pattern=""):
    # 收集变压器损耗数据
    dss.Transformers.First()
    transformer_losses = {}
    while True:
        name = dss.Transformers.Name()

        # 使用复杂的过滤规则
        if not filter_name(name, filter_pattern):
            losses = {
                "TotalLoss": dss.Transformers.LossesByType()[0]/1000,  # 总损耗,改变单位kVA
                "LoadLoss": dss.Transformers.LossesByType()[2]/1000,  # 负载损耗
                "NoLoadLoss": dss.Transformers.LossesByType()[4]/1000  # 空载损耗
            }
            transformer_losses[name] = losses

        if not dss.Transformers.Next() > 0:
            break

    return transformer_losses

def add_transformer_losses(losses1, losses2):
    # 如果losses1为空，直接返回losses2
    if not losses1:
        return losses2

    sum_losses = {}
    for key in losses1:
        # 确保losses2也包含相同的键
        if key in losses2:
            sum_losses[key] = {
                "TotalLoss": losses1[key]["TotalLoss"] + losses2[key]["TotalLoss"],
                "LoadLoss": losses1[key]["LoadLoss"] + losses2[key]["LoadLoss"],
                "NoLoadLoss": losses1[key]["NoLoadLoss"] + losses2[key]["NoLoadLoss"]
            }
        else:
            # 如果losses2中没有对应的键，只使用losses1的值
            sum_losses[key] = losses1[key]
    
    return sum_losses

def get_line_losses():
    # 收集线路损耗数据
    dss.Lines.First()
    line_losses = {}
    while True:
        name = dss.Lines.Name()
        # 获取损耗（返回的是一个包含有功和无功损耗的元组）
        losses = dss.CktElement.Losses()[0]/1000
        line_losses[name] = losses
        if not dss.Lines.Next() > 0:
            break
    return line_losses

def add_line_losses(losses1, losses2):
    # 如果losses1为空，直接返回losses2
    if not losses1:
        return losses2

    sum_losses = {}
    for key in losses1:
        # 确保losses2也包含相同的键
        if key in losses2:
            sum_losses[key] = losses1[key] + losses2[key]
        else:
            # 如果losses2中没有对应的键，只使用losses1的值
            sum_losses[key] = losses1[key]

    return sum_losses

def filter_name(name, pattern):
    """
    根据提供的模式过滤名称。
    返回 True 如果名称与模式匹配，否则返回 False。
    """
    return re.match(pattern, name) is not None

def save_opendss_losses(new_process, transformer_losses, line_losses):
    for name, losses in transformer_losses.items():
        Loss.create(
            calculation_process=new_process,
            component_name=name,
            unit="kWh",  
            total_loss=losses["TotalLoss"],
            load_loss=losses["LoadLoss"],
            no_load_loss=losses["NoLoadLoss"]
        )
    for name, losses in line_losses.items():
        Loss.create(
            calculation_process=new_process,
            component_name=name,
            unit="kWh",  
            total_loss=losses,
            load_loss=losses,
            no_load_loss=0
        )