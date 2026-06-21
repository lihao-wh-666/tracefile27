"""
阳光显示组件
显示当前阳光数量
"""

import pygame
from typing import Tuple

from ui.font_utils import get_font


class SunDisplay:
    """阳光显示组件"""

    def __init__(self, x: int, y: int, initial_sun: int = 150,
                 font_size: int = 28):
        """
        初始化阳光显示

        Args:
            x: X坐标
            y: Y坐标
            initial_sun: 初始阳光数量
            font_size: 字体大小
        """
        self.x = x
        self.y = y
        self.sun_count = initial_sun
        self.width = 120
        self.height = 50

        self.font = get_font(font_size)

    def update_sun(self, sun_count: int):
        """
        更新阳光数量

        Args:
            sun_count: 当前阳光数量
        """
        self.sun_count = sun_count

    def draw(self, surface: pygame.Surface):
        """
        绘制阳光显示

        Args:
            surface: 绘制表面
        """
        pygame.draw.rect(surface, (139, 90, 43),
                         (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, (101, 67, 33),
                         (self.x, self.y, self.width, self.height), 3)

        sun_icon_x = self.x + 15
        sun_icon_y = self.y + self.height // 2
        pygame.draw.circle(surface, (255, 255, 0),
                           (sun_icon_x, sun_icon_y), 15)
        pygame.draw.circle(surface, (255, 200, 0),
                           (sun_icon_x, sun_icon_y), 15, 2)

        text = self.font.render(str(self.sun_count), True, (255, 255, 0))
        text_rect = text.get_rect(
            left=self.x + 40,
            centery=self.y + self.height // 2
        )
        surface.blit(text, text_rect)

    def get_rect(self) -> pygame.Rect:
        """获取显示区域矩形"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
