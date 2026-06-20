"""
场景基类模块
定义所有场景的通用接口
"""

import pygame
from typing import Optional, Any


class BaseScene:
    """场景基类，所有场景的父类"""

    def __init__(self, game_controller=None):
        """
        初始化场景

        Args:
            game_controller: 游戏控制器引用
        """
        self.game_controller = game_controller
        self.name: str = "base"
        self.active: bool = False
        self.next_scene: Optional[str] = None
        self.scene_data: dict = {}

    def enter(self, data: dict = None):
        """
        进入场景时调用

        Args:
            data: 传递给场景的数据
        """
        self.active = True
        if data:
            self.scene_data = data
        self._on_enter()

    def _on_enter(self):
        """进入场景的具体实现，子类重写"""
        pass

    def exit(self) -> dict:
        """
        退出场景时调用

        Returns:
            传递给下一个场景的数据
        """
        self.active = False
        self._on_exit()
        return self.scene_data

    def _on_exit(self):
        """退出场景的具体实现，子类重写"""
        pass

    def handle_event(self, event: pygame.event.Event):
        """
        处理事件

        Args:
            event: Pygame事件
        """
        pass

    def update(self, current_time: int, *args, **kwargs):
        """
        更新场景状态

        Args:
            current_time: 当前时间（毫秒）
        """
        pass

    def render(self, surface: pygame.Surface):
        """
        渲染场景

        Args:
            surface: 绘制表面
        """
        pass

    def is_done(self) -> bool:
        """
        检查场景是否结束

        Returns:
            是否结束
        """
        return self.next_scene is not None

    def get_next_scene(self) -> Optional[str]:
        """
        获取下一个场景名称

        Returns:
            下一个场景名称
        """
        return self.next_scene

    def set_next_scene(self, scene_name: str, data: dict = None):
        """
        设置下一个场景

        Args:
            scene_name: 场景名称
            data: 传递的数据
        """
        self.next_scene = scene_name
        if data:
            self.scene_data = data

    def reset(self):
        """重置场景状态"""
        self.next_scene = None
        self.scene_data = {}
