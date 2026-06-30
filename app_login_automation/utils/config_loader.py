"""配置加载工具：读取 config/caps.yaml。"""
from pathlib import Path

import yaml

# 配置文件路径（相对于项目根目录）
_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "caps.yaml"


def load_config() -> dict:
    """读取并返回 YAML 配置字典。"""
    with _CONFIG_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)
