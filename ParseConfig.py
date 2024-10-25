# 解析Config.json文件
import json
import os

# 全局变量
config = None


def load_config():
    """加载Config.json文件并返回其内容"""
    global config
    if config is not None:
        return config

    config_path = os.path.join(os.getcwd(), "Config.json")
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            config = json.load(file)
    except FileNotFoundError:
        print("Config.json文件未找到")
        config = {}
    except json.JSONDecodeError:
        print("Config.json文件格式错误")
        config = {}

    return config


def get_xlsx_path():
    """从Config.json中获取xlsx路径"""
    config_data = load_config()
    return config_data.get("xlsx_path", "路径未找到")


# 更新xlsx路径并保存，json易读
def set_xlsx_path(new_path):
    """更新xlsx路径并保存到Config.json文件中"""
    config_data = load_config()
    config_data["xlsx_path"] = new_path
    with open(os.path.join(os.getcwd(), "Config.json"), "w", encoding="utf-8") as file:
        json.dump(config_data, file, ensure_ascii=False, indent=4)


# 获取所有渠道类型
def get_all_channels():
    """获取Config.json中所有渠道类型"""
    config_data = load_config()
    channels = config_data.get("channels", {})
    return list(channels.keys())


def get_channel_params(channel_name: str) -> list:
    """获取指定渠道的参数"""
    config_data = load_config()
    channels = config_data.get("channels", {})
    channel_info = channels.get(channel_name, {})
    return [channel_info.get("AppID", ""), channel_info.get("AppKey", "")]
