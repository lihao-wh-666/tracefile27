"""
进度条组件
显示关卡/波次进度
"""

import pygame
from typing import Tuple

from ui.font_utils import get_font


class ProgressBar:
    """进度条组件"""

    def __init__(self, x: int, y: int, width: int, height: int,
                 bg_color: Tuple[int, int, int] = (100, 100, 100),
                 fill_color: Tuple[int, int, int] = (0, 200, 0),
                 border_color: Tuple[int, int, int] = (0, 0, 0),
                 border_width: int = 2,
                 show_text: bool = True,
                 text_format: str = "{:.0f}%"):
        """
        初始化进度条

        Args:
            x: X坐标
            y: Y坐标
            width: 宽度
            height: 高度
            bg_color: 背景颜色
            fill_color: 填充颜色
            border_color: 边框颜色
            border_width: 边框宽度
            show_text: 是否显示文本
            text_format: 文本格式
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.border_color = border_color
        self.border_width = border_width
        self.show_text = show_text
        self.text_format = text_format

        self.progress = 0.0

        self.font = get_font(14)

    def set_progress(self, progress: float):
        """
        设置进度

        Args:
            progress: 进度值 0.0 - 1.0
        """
        self.progress = max(0.0, min(1.0, progress))

    def get_progress(self) -> float:
        """获取当前进度"""
        return self.progress

    def draw(self, surface: pygame.Surface):
        """
        绘制进度条

        Args:
            surface: 绘制表面
        """
        pygame.draw.rect(surface, self.bg_color,
                         (self.x, self.y, self.width, self.height))

        fill_width = int(self.width * self.progress)
        if fill_width > 0:
            pygame.draw.rect(surface, self.fill_color,
                             (self.x, self.y, fill_width, self.height))

        pygame.draw.rect(surface, self.border_color,
                         (self.x, self.y, self.width, self.height), self.border_width)

        if self.show_text:
            text = self.font.render(
                self.text_format.format(self.progress * 100),
                True, (255, 255, 255)
            )
            text_rect = text.get_rect(center=(self.x + self.width // 2,
                                               self.y + self.height // 2))
            surface.blit(text, text_rect)

    def get_rect(self) -> pygame.Rect:
        """获取进度条矩形"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
