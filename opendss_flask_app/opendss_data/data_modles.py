from admin.models import * 
from app import db
from datetime import datetime
from peewee import *

class Calculation_Process(db.Model):
    user = ForeignKeyField(User, backref='calculation_processes')
    upload_time = DateTimeField(default=datetime.now) # 上传时间
    json_data = TextField(default="") # 接收的 JSON 数据
    opendss_script = TextField(default="") # 生成的 OpenDSS 脚本

    def __str__(self):
        return f"{self.user.username}'s calculation process at {self.upload_time}"
    
class VI(db.Model):
    calculation_process = ForeignKeyField(Calculation_Process, backref='vi', unique=True)
    component_name = TextField()
    unit = TextField()  # "kV" 或 "A"

    def __str__(self):
        return f"{self.component_name} ({self.unit})"
    
class VIHourValue(db.Model):
    vi = ForeignKeyField(VI, backref='values')
    hour = IntegerField()  # 表示24小时
    value = FloatField()  # 24整点数值
    
class Loss(db.Model):
    calculation_process = ForeignKeyField(Calculation_Process, backref='loss', unique=True)
    component_name = TextField()
    unit = TextField()  # kW
    total_loss = FloatField()  # 总损耗
    load_loss = FloatField()  # 负载损耗
    no_load_loss = FloatField()  # 空载损耗

    def __str__(self):
        return f"{self.component_name} Total Loss: {self.total_loss} {self.unit}"