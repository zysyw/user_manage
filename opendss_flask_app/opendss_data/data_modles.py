from admin.models import * 
from app import db
from datetime import datetime
from peewee import *

class Calculation_Process(db.Model):
    user = ForeignKeyField(User, backref='calculation_processes')
    upload_time = DateTimeField(default=datetime.now) # 上传时间
    json_data = TextField(default="") # 接收的 JSON 数据
    opendss_script = TextField(default="") # 生成的 OpenDSS 脚本
    
    @classmethod
    def create_with_related_tables(cls, user):
        # 创建新的 Calculation_Process 对象
        new_process = cls.create(user=user)

        # 创建相关联的空表
        VI.create(calculation_process=new_process)
        VIHourValue.create(vi=VI.select().where(VI.calculation_process == new_process))
        Loss.create(calculation_process=new_process)

        return new_process

    def __str__(self):
        return f"{self.user.username}'s calculation process at {self.upload_time}"
    
class VI(db.Model):
    calculation_process = ForeignKeyField(Calculation_Process, backref='vi')
    component_name = TextField(default="")
    unit = TextField(default="")  # "V" 或 "A"

    def generate_hourly_values(self):
        return [f'{value.value:.1f}' for value in self.values] # 形成24小时数据list，数值保留一位小数

    def __str__(self):
        return f"{self.component_name} ({self.unit})"
    
class VIHourValue(db.Model):
    vi = ForeignKeyField(VI, backref='values')
    hour = IntegerField(default=0)  # 表示24小时
    value = FloatField(default=0.0)  # 24整点数值
    
class Loss(db.Model):
    calculation_process = ForeignKeyField(Calculation_Process, backref='loss')
    component_name = TextField(default="")
    unit = TextField(default="")  # kW
    total_loss = FloatField(default=0.0)  # 总损耗
    load_loss = FloatField(default=0.0)  # 负载损耗
    no_load_loss = FloatField(default=0.0)  # 空载损耗

    def __str__(self):
        return f"{self.component_name} Total Loss: {self.total_loss} {self.unit}"