"""
场景模块 (scene)
实现游戏场景管理系统，包含主菜单场景、游戏场景、暂停场景、胜利/失败场景。
"""

from .base_scene import BaseScene
from .scene_manager import SceneManager
from .menu_scene import MenuScene
from .game_scene import GameScene
from .pause_scene import PauseScene
from .end_scene import EndScene

__all__ = [
    "BaseScene",
    "SceneManager",
    "MenuScene",
    "GameScene",
    "PauseScene",
    "EndScene",
]
