import os

def generate_dss_script(data):
    # 使用 Jinja2 生成 OpenDSS 脚本

    # 确保 JSON 数据的第一层只有一个键值对：excel侧形成json的规则是以文件名为key，所有的数据打包成value
    if len(data) != 1:
        raise ValueError("JSON 数据应该只包含一个顶级键")

    # 获取顶级键名，也即文件名
    top_level_key = list(data.keys())[0]
    top_level_data = data[top_level_key]

    from jinja2 import Environment, FileSystemLoader
    # 设置 Jinja2 环境
    env = Environment(
        loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__))),
        trim_blocks=True,
        lstrip_blocks=True
    )
    template = env.get_template('opendss_template.j2')
    opendss_script = template.render(top_level_key=top_level_key, top_level_data=top_level_data)

    return opendss_script