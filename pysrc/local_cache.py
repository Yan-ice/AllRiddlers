import json
import os

##########################################
# Configs

config_file = 'config/team_name.json'
first_night_order_file = 'config/first_night_order.txt'
other_night_order_file = 'config/other_night_order.txt'

def load_team_map():
    with open(config_file, "r") as f:
        return json.load(f)

def load_first_night_order():
    with open(first_night_order_file, 'r') as f:
        return f.readlines()

def load_other_night_order():
    with open(other_night_order_file, 'r') as f:
        return f.readlines()

def save_team_map(d):
    with open(config_file, "w") as f:
        json.dump(d, f)

def save_first_night_order(d):
    with open(first_night_order_file, 'w') as f:
        for i in d:
            first_night_order_file.write(i+'\n')

def save_other_night_order(d):
    with open(other_night_order_file, 'w') as f:
        for i in d:
            other_night_order_file.write(i+'\n')

#############################################
# Characters

data_dir = 'data'

def load_character_list():
    return [f for f in os.listdir(data_dir)]

def load_character_meta(name):
    data_path = os.path.join(data_dir, name).replace("\\", "/")  # 兼容 Windows 路径
    metadata_path = os.path.join(data_path, 'meta.json').replace("\\", "/")

    with open(metadata_path, "r") as f:
        return json.load(f)
    
def load_character_reminder(name):
    data_path = os.path.join(data_dir, name).replace("\\", "/")  # 兼容 Windows 路径
    remind_path = os.path.join(data_path, 'remind.json').replace("\\", "/")
    
    with open(remind_path, "r") as f:
        return json.load(f)
    
def save_character_meta(name, data):
    data_path = os.path.join(data_dir, name).replace("\\", "/")  # 兼容 Windows 路径
    metadata_path = os.path.join(data_path, 'meta.json').replace("\\", "/")

    with open(metadata_path, "w") as f:
        json.dump(data, f, ensure_ascii=False)
    
def save_character_reminder(name, data):
    data_path = os.path.join(data_dir, name).replace("\\", "/")  # 兼容 Windows 路径
    remind_path = os.path.join(data_path, 'remind.json').replace("\\", "/")
    
    with open(remind_path, "w") as f:
        json.dump(data, f, ensure_ascii=False)