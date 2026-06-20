"""
游戏核心逻辑模块 (game_core)
作为游戏主控制器，协调各模块间交互。
"""

from .game_controller import GameController
from .level import LevelManager
from .economy import EconomyManager
from .collision import CollisionManager

__all__ = [
    "GameController",
    "LevelManager",
    "EconomyManager",
    "CollisionManager",
]
