"""
字体工具模块
提供跨平台兼容的中文字体加载功能
支持 Windows、Linux、macOS 的常见中文字体自动检测
"""

import os
import sys
import platform
import pygame
from typing import Optional, List


def _get_windows_font_paths() -> List[str]:
    """获取 Windows 系统常见中文字体路径"""
    windir = os.environ.get("WINDIR", r"C:\Windows")
    font_dir = os.path.join(windir, "Fonts")
    candidates = [
        os.path.join(font_dir, "msyh.ttc"),
        os.path.join(font_dir, "msyhbd.ttc"),
        os.path.join(font_dir, "simhei.ttf"),
        os.path.join(font_dir, "simsun.ttc"),
        os.path.join(font_dir, "simkai.ttf"),
    ]
    return [p for p in candidates if os.path.exists(p)]


def _get_linux_font_paths() -> List[str]:
    """获取 Linux 系统常见中文字体路径"""
    search_dirs = [
        "/usr/share/fonts",
        "/usr/local/share/fonts",
        os.path.expanduser("~/.fonts"),
        os.path.expanduser("~/.local/share/fonts"),
    ]
    candidates = []
    keywords = [
        "NotoSansCJK",
        "NotoSerifCJK",
        "wqy-microhei",
        "wqy-zenhei",
        "wenquanyi",
        "uming",
        "ukai",
        "SourceHanSans",
        "SourceHanSerif",
        "SimSun",
        "msyh",
        "simhei",
    ]
    for search_dir in search_dirs:
        if not os.path.isdir(search_dir):
            continue
        for root, _, files in os.walk(search_dir):
            for f in files:
                low = f.lower()
                if any(k.lower() in low for k in keywords) and f.lower().endswith((".ttf", ".otf", ".ttc")):
                    candidates.append(os.path.join(root, f))
    return candidates


def _get_macos_font_paths() -> List[str]:
    """获取 macOS 系统常见中文字体路径"""
    search_dirs = [
        "/System/Library/Fonts",
        "/Library/Fonts",
        os.path.expanduser("~/Library/Fonts"),
    ]
    candidates = []
    keywords = [
        "PingFang",
        "Heiti",
        "STHeiti",
        "HiraginoSansGB",
        "Songti",
        "STSong",
        "ArialUnicode",
    ]
    for search_dir in search_dirs:
        if not os.path.isdir(search_dir):
            continue
        for root, _, files in os.walk(search_dir):
            for f in files:
                low = f.lower()
                if any(k.lower() in low for k in keywords) and f.lower().endswith((".ttf", ".otf", ".ttc")):
                    candidates.append(os.path.join(root, f))
    return candidates


def _get_system_font_file() -> Optional[str]:
    """自动检测并返回一个可用的中文字体文件路径"""
    system = platform.system()
    if system == "Windows":
        paths = _get_windows_font_paths()
    elif system == "Darwin":
        paths = _get_macos_font_paths()
    else:
        paths = _get_linux_font_paths()

    if paths:
        return paths[0]
    return None


_cached_font_path: Optional[str] = None


def _get_cached_font_path() -> Optional[str]:
    """获取缓存的字体路径，避免重复扫描"""
    global _cached_font_path
    if _cached_font_path is None:
        _cached_font_path = _get_system_font_file()
    return _cached_font_path


def load_font(size: int, bold: bool = False) -> pygame.font.Font:
    """
    加载支持中文的字体

    Args:
        size: 字体大小（像素）
        bold: 是否加粗

    Returns:
        pygame.font.Font 字体对象，确保支持中文渲染
    """
    font_path = _get_cached_font_path()

    if font_path:
        try:
            font = pygame.font.Font(font_path, size)
            if bold and font:
                font.set_bold(True)
            return font
        except Exception:
            pass

    try:
        sys_names = []
        system = platform.system()
        if system == "Windows":
            sys_names = ["microsoftyahei", "simhei", "simsun", "microsoftjhenghei"]
        elif system == "Darwin":
            sys_names = ["pingfangsc", "heiti", "songti", "arialunicodems"]
        else:
            sys_names = ["notosanscjk", "notoserifcjk", "wenquanyimicrohei", "wenquanyizenhei"]

        for name in sys_names:
            try:
                font = pygame.font.SysFont(name, size, bold=bold)
                if font:
                    return font
            except Exception:
                continue
    except Exception:
        pass

    try:
        return pygame.font.SysFont(None, size, bold=bold)
    except Exception:
        return pygame.font.Font(None, size)


def get_font(size: int, bold: bool = False,
             resource_loader: Optional[object] = None,
             font_name: str = "default") -> pygame.font.Font:
    """
    获取字体对象的统一接口

    Args:
        size: 字体大小（像素）
        bold: 是否加粗
        resource_loader: 资源加载器（可选）
        font_name: 字体名称

    Returns:
        pygame.font.Font 字体对象
    """
    if resource_loader and hasattr(resource_loader, "load_font"):
        try:
            return resource_loader.load_font(font_name, size)
        except Exception:
            pass

    return load_font(size, bold)
