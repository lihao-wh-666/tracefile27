"""
按钮组件模块
通用按钮UI元素
"""

import pygame
from typing import Callable, Optional, Tuple

from ui.font_utils import get_font


class Button:
    """按钮组件"""

    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 on_click: Optional[Callable] = None,
                 bg_color: Tuple[int, int, int] = (200, 200, 200),
                 hover_color: Tuple[int, int, int] = (180, 180, 180),
                 text_color: Tuple[int, int, int] = (0, 0, 0),
                 font_size: int = 24,
                 border_color: Tuple[int, int, int] = (0, 0, 0),
                 border_width: int = 2):
        """
        初始化按钮

        Args:
            x: X坐标
            y: Y坐标
            width: 宽度
            height: 高度
            text: 按钮文本
            on_click: 点击回调
            bg_color: 背景颜色
            hover_color: 悬停颜色
            text_color: 文本颜色
            font_size: 字体大小
            border_color: 边框颜色
            border_width: 边框宽度
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.on_click = on_click
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width
        self.enabled = True
        self.is_hovered = False

        self.font = get_font(font_size)

    def set_text(self, text: str):
        """设置按钮文本"""
        self.text = text

    def set_enabled(self, enabled: bool):
        """设置按钮是否可用"""
        self.enabled = enabled

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        处理事件

        Args:
            event: Pygame事件

        Returns:
            是否处理了事件
        """
        if not self.enabled:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click:
                    self.on_click()
                return True

        elif event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)

        return False

    def update(self, current_time: int = 0):
        """
        更新按钮状态

        Args:
            current_time: 当前时间
        """
        pass

    def draw(self, surface: pygame.Surface):
        """
        绘制按钮

        Args:
            surface: 绘制表面
        """
        if self.enabled:
            color = self.hover_color if self.is_hovered else self.bg_color
        else:
            color = (150, 150, 150)

        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, self.border_width)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def get_rect(self) -> pygame.Rect:
        """获取按钮矩形"""
        return self.rect
