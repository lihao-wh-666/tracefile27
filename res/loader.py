"""
资源加载器模块
负责统一管理游戏内所有资源的加载、缓存、释放机制
"""

import os
import pygame
from typing import Dict, Optional


class ResourceLoader:
    """资源加载器，统一管理游戏资源的加载与缓存"""

    def __init__(self, config):
        """
        初始化资源加载器

        Args:
            config: GameConfig 配置对象
        """
        self.config = config
        self._image_cache: Dict[str, pygame.Surface] = {}
        self._audio_cache: Dict[str, pygame.mixer.Sound] = {}
        self._font_cache: Dict[str, pygame.font.Font] = {}
        self._bgm_loaded: bool = False

    def load_image(self, name: str, filename: Optional[str] = None) -> pygame.Surface:
        """
        加载图片资源，支持缓存

        Args:
            name: 资源名称（用于缓存索引）
            filename: 文件名，默认为 name + '.png'

        Returns:
            pygame.Surface 图片表面
        """
        if name in self._image_cache:
            return self._image_cache[name]

        if filename is None:
            filename = name + ".png"

        filepath = self.config.get_image_path(filename)

        try:
            if os.path.exists(filepath):
                image = pygame.image.load(filepath).convert_alpha()
            else:
                image = self._generate_placeholder_image(name)
        except Exception as e:
            print(f"加载图片 {name} 失败: {e}，使用占位图")
            image = self._generate_placeholder_image(name)

        self._image_cache[name] = image
        return image

    def _generate_placeholder_image(self, name: str) -> pygame.Surface:
        """
        生成占位图片（当资源文件不存在时使用）

        Args:
            name: 资源名称，用于决定占位图样式

        Returns:
            pygame.Surface 占位图片
        """
        size_map = {
            "sunflower": (70, 70),
            "peashooter": (70, 70),
            "wallnut": (70, 70),
            "normal_zombie": (60, 90),
            "cone_zombie": (60, 90),
            "pea_bullet": (15, 15),
            "sun": (50, 50),
            "lawn_mower": (50, 50),
        }

        color_map = {
            "sunflower": (255, 215, 0),
            "peashooter": (34, 139, 34),
            "wallnut": (139, 90, 43),
            "normal_zombie": (128, 128, 128),
            "cone_zombie": (255, 140, 0),
            "pea_bullet": (0, 255, 0),
            "sun": (255, 255, 0),
            "lawn_mower": (192, 192, 192),
        }

        size = size_map.get(name, (60, 60))
        color = color_map.get(name, (100, 100, 100))

        surface = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.ellipse(surface, color, (0, 0, size[0], size[1]))
        pygame.draw.ellipse(surface, (0, 0, 0), (0, 0, size[0], size[1]), 2)

        try:
            font = pygame.font.SysFont("arial", 12, bold=True)
            text = font.render(name[:3], True, (0, 0, 0))
            text_rect = text.get_rect(center=(size[0] // 2, size[1] // 2))
            surface.blit(text, text_rect)
        except Exception:
            pass

        return surface

    def load_sound(self, name: str, filename: Optional[str] = None) -> Optional[pygame.mixer.Sound]:
        """
        加载音效资源，支持缓存

        Args:
            name: 资源名称
            filename: 文件名，默认为 name + '.wav'

        Returns:
            pygame.mixer.Sound 音效对象或 None
        """
        if name in self._audio_cache:
            return self._audio_cache[name]

        if filename is None:
            filename = name + ".wav"

        filepath = self.config.get_audio_path(filename)

        try:
            if os.path.exists(filepath):
                sound = pygame.mixer.Sound(filepath)
                sound.set_volume(self.config.SFX_VOLUME)
                self._audio_cache[name] = sound
                return sound
        except Exception as e:
            print(f"加载音效 {name} 失败: {e}")

        self._audio_cache[name] = None
        return None

    def play_sound(self, name: str):
        """播放音效"""
        sound = self.load_sound(name)
        if sound:
            sound.set_volume(self.config.SFX_VOLUME)
            sound.play()

    def load_bgm(self, filename: str = "bgm.mp3") -> bool:
        """
        加载背景音乐

        Args:
            filename: 背景音乐文件名

        Returns:
            是否加载成功
        """
        filepath = self.config.get_audio_path(filename)

        try:
            if os.path.exists(filepath):
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.set_volume(self.config.BGM_VOLUME)
                self._bgm_loaded = True
                return True
        except Exception as e:
            print(f"加载背景音乐失败: {e}")

        self._bgm_loaded = False
        return False

    def play_bgm(self, loops: int = -1):
        """播放背景音乐"""
        if self._bgm_loaded:
            pygame.mixer.music.set_volume(self.config.BGM_VOLUME)
            pygame.mixer.music.play(loops)

    def stop_bgm(self):
        """停止背景音乐"""
        if self._bgm_loaded:
            pygame.mixer.music.stop()

    def pause_bgm(self):
        """暂停背景音乐"""
        if self._bgm_loaded:
            pygame.mixer.music.pause()

    def resume_bgm(self):
        """继续播放背景音乐"""
        if self._bgm_loaded:
            pygame.mixer.music.unpause()

    def load_font(self, name: str, size: int, filename: Optional[str] = None) -> pygame.font.Font:
        """
        加载字体资源

        Args:
            name: 字体名称
            size: 字体大小
            filename: 字体文件名

        Returns:
            pygame.font.Font 字体对象
        """
        cache_key = f"{name}_{size}"
        if cache_key in self._font_cache:
            return self._font_cache[cache_key]

        if filename is None:
            filename = name + ".ttf"

        filepath = self.config.get_font_path(filename)

        try:
            if os.path.exists(filepath):
                font = pygame.font.Font(filepath, size)
            else:
                font = pygame.font.Font(None, size)
        except Exception:
            font = pygame.font.Font(None, size)

        self._font_cache[cache_key] = font
        return font

    def release_image(self, name: str):
        """释放指定图片缓存"""
        if name in self._image_cache:
            del self._image_cache[name]

    def release_sound(self, name: str):
        """释放指定音效缓存"""
        if name in self._audio_cache:
            del self._audio_cache[name]

    def release_all_images(self):
        """释放所有图片缓存"""
        self._image_cache.clear()

    def release_all_sounds(self):
        """释放所有音效缓存"""
        self._audio_cache.clear()

    def release_all(self):
        """释放所有资源缓存"""
        self._image_cache.clear()
        self._audio_cache.clear()
        self._font_cache.clear()
        self._bgm_loaded = False
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        except Exception:
            pass
