"""
字体工具模块
提供跨平台兼容的字体加载功能
"""

import pygame
from typing import Optional


def load_font(size: int, bold: bool = False) -> pygame.font.Font:
    """
    加载字体，自动回退到默认字体

    Args:
        size: 字体大小
        bold: 是否加粗

    Returns:
        pygame.font.Font 字体对象
    """
    font_candidates = [
        "microsoftyahei",
        "simhei",
        "arial",
        "sans",
    ]

    for font_name in font_candidates:
        try:
            font = pygame.font.SysFont(font_name, size, bold=bold)
            if font:
                return font
        except Exception:
            continue

    try:
        return pygame.font.Font(None, size)
    except Exception:
        default_font = pygame.font.SysFont(None, size, bold=bold)
        return default_font


def get_font(size: int, bold: bool = False,
             resource_loader: Optional[object] = None,
             font_name: str = "default") -> pygame.font.Font:
    """
    获取字体对象的统一接口

    Args:
        size: 字体大小
        bold: 是否加粗
        resource_loader: 资源加载器（可选）
        font_name: 字体名称

    Returns:
        pygame.font.Font 字体对象
    """
    if resource_loader and hasattr(resource_loader, 'load_font'):
        try:
            return resource_loader.load_font(font_name, size)
        except Exception:
            pass

    return load_font(size, bold)
