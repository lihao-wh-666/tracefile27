"""
场景管理器模块
管理场景的切换和生命周期
"""

import pygame
from typing import Dict, Optional

from scene.base_scene import BaseScene


class SceneManager:
    """场景管理器"""

    def __init__(self):
        """初始化场景管理器"""
        self.scenes: Dict[str, BaseScene] = {}
        self.current_scene: Optional[BaseScene] = None
        self.current_scene_name: Optional[str] = None

    def register_scene(self, name: str, scene: BaseScene):
        """
        注册场景

        Args:
            name: 场景名称
            scene: 场景实例
        """
        self.scenes[name] = scene

    def get_scene(self, name: str) -> Optional[BaseScene]:
        """
        获取场景

        Args:
            name: 场景名称

        Returns:
            场景实例
        """
        return self.scenes.get(name)

    def switch_scene(self, name: str, data: dict = None) -> bool:
        """
        切换场景

        Args:
            name: 目标场景名称
            data: 传递的数据

        Returns:
            是否切换成功
        """
        if name not in self.scenes:
            return False

        if self.current_scene:
            exit_data = self.current_scene.exit()
            if data is None:
                data = exit_data

        self.current_scene = self.scenes[name]
        self.current_scene_name = name
        self.current_scene.enter(data)

        return True

    def handle_event(self, event: pygame.event.Event):
        """
        处理事件

        Args:
            event: Pygame事件
        """
        if self.current_scene:
            self.current_scene.handle_event(event)

    def update(self, current_time: int, *args, **kwargs):
        """
        更新当前场景

        Args:
            current_time: 当前时间
        """
        if self.current_scene:
            self.current_scene.update(current_time, *args, **kwargs)

            if self.current_scene.is_done():
                next_scene = self.current_scene.get_next_scene()
                if next_scene:
                    scene_data = self.current_scene.scene_data
                    self.switch_scene(next_scene, scene_data)

    def render(self, surface: pygame.Surface):
        """
        渲染当前场景

        Args:
            surface: 绘制表面
        """
        if self.current_scene:
            self.current_scene.render(surface)

    def get_current_scene_name(self) -> Optional[str]:
        """获取当前场景名称"""
        return self.current_scene_name

    def get_current_scene(self) -> Optional[BaseScene]:
        """获取当前场景"""
        return self.current_scene
