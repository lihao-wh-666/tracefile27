"""
资源模块 (res)
负责统一管理游戏内所有资源，包括图片素材、音频文件、字体文件及配置数据。
"""

from .config import GameConfig
from .loader import ResourceLoader

__all__ = ["GameConfig", "ResourceLoader"]
