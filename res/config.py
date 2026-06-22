"""
游戏配置模块
管理游戏所有配置数据，包括窗口设置、游戏参数、路径配置等
"""

import os
from dataclasses import dataclass, field


@dataclass
class GameConfig:
    """游戏配置类，集中管理所有游戏参数"""

    # ========== 窗口设置 ==========
    SCREEN_WIDTH: int = 900
    SCREEN_HEIGHT: int = 600
    WINDOW_TITLE: str = "植物大战僵尸 - PvZ"
    FPS: int = 60
    FULLSCREEN: bool = False

    # ========== 音量设置 ==========
    BGM_VOLUME: float = 0.5
    SFX_VOLUME: float = 0.7

    # ========== 网格设置 ==========
    GRID_ROWS: int = 5
    GRID_COLS: int = 9
    CELL_WIDTH: int = 80
    CELL_HEIGHT: int = 100
    GRID_OFFSET_X: int = 80
    GRID_OFFSET_Y: int = 80

    # ========== 游戏经济设置 ==========
    INITIAL_SUN: int = 150
    SUN_FALL_INTERVAL: int = 10000
    SUN_VALUE: int = 25

    # ========== 植物配置 ==========
    PLANT_COSTS: dict = field(default_factory=lambda: {
        "sunflower": 50,
        "peashooter": 100,
        "wallnut": 50,
    })
    PLANT_COOLDOWNS: dict = field(default_factory=lambda: {
        "sunflower": 7500,
        "peashooter": 7500,
        "wallnut": 30000,
    })

    # ========== 植物物种映射（游戏名称 -> 真实植物学名） ==========
    PLANT_SPECIES: dict = field(default_factory=lambda: {
        "sunflower": {
            "scientific_name": "Helianthus annuus",
            "common_name_cn": "向日葵",
            "views": ["front", "side", "top"],
            "image_format": "png",
        },
        "peashooter": {
            "scientific_name": "Pisum sativum",
            "common_name_cn": "豌豆",
            "views": ["front", "side", "top"],
            "image_format": "png",
        },
        "wallnut": {
            "scientific_name": "Juglans regia",
            "common_name_cn": "核桃",
            "views": ["front", "side", "top"],
            "image_format": "png",
        },
    })

    # ========== 资源文件命名规范 ==========
    # 主视图: {plant_name}.png
    # 多视图: {view}_{plant_name}.png
    # 示例: sunflower.png, front_sunflower.png, side_sunflower.png, top_sunflower.png
    PLANT_IMAGE_NAMING: dict = field(default_factory=lambda: {
        "pattern_view": "{view}_{plant_name}.{ext}",
        "pattern_main": "{plant_name}.{ext}",
        "supported_views": ["front", "side", "top"],
        "supported_formats": ["png", "jpg", "jpeg"],
        "max_file_size_kb": 2048,
        "min_resolution": (1920, 1080),
    })

    # ========== 僵尸配置 ==========
    ZOMBIE_BASE_SPEED: float = 0.5
    ZOMBIE_BASE_HP: int = 100
    ZOMBIE_SPAWN_INTERVAL: int = 5000

    # ========== 路径设置 ==========
    BASE_DIR: str = field(default_factory=lambda: os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    ))
    ASSETS_DIR: str = field(default_factory=lambda: "")
    IMAGES_DIR: str = field(default_factory=lambda: "")
    AUDIO_DIR: str = field(default_factory=lambda: "")
    FONTS_DIR: str = field(default_factory=lambda: "")
    PLANTS_IMAGES_DIR: str = field(default_factory=lambda: "")

    def __post_init__(self):
        """初始化路径"""
        self.ASSETS_DIR = os.path.join(self.BASE_DIR, "assets")
        self.IMAGES_DIR = os.path.join(self.ASSETS_DIR, "images")
        self.AUDIO_DIR = os.path.join(self.ASSETS_DIR, "audio")
        self.FONTS_DIR = os.path.join(self.ASSETS_DIR, "fonts")
        self.PLANTS_IMAGES_DIR = os.path.join(self.IMAGES_DIR, "plants")

    def get_image_path(self, filename: str) -> str:
        """获取图片文件完整路径"""
        return os.path.join(self.IMAGES_DIR, filename)

    def get_plant_image_path(self, plant_name: str, view: str = None) -> str:
        """获取植物图片完整路径

        Args:
            plant_name: 植物名称（如 sunflower）
            view: 视图角度（front/side/top），None表示主视图

        Returns:
            图片文件完整路径
        """
        naming = self.PLANT_IMAGE_NAMING
        ext = self.PLANT_SPECIES.get(plant_name, {}).get("image_format", "png")

        if view is None:
            filename = naming["pattern_main"].format(plant_name=plant_name, ext=ext)
            return os.path.join(self.IMAGES_DIR, filename)
        else:
            filename = naming["pattern_view"].format(view=view, plant_name=plant_name, ext=ext)
            return os.path.join(self.PLANTS_IMAGES_DIR, plant_name, filename)

    def get_audio_path(self, filename: str) -> str:
        """获取音频文件完整路径"""
        return os.path.join(self.AUDIO_DIR, filename)

    def get_font_path(self, filename: str) -> str:
        """获取字体文件完整路径"""
        return os.path.join(self.FONTS_DIR, filename)

    def toggle_fullscreen(self):
        """切换全屏模式"""
        self.FULLSCREEN = not self.FULLSCREEN

    def set_bgm_volume(self, volume: float):
        """设置背景音乐音量"""
        self.BGM_VOLUME = max(0.0, min(1.0, volume))

    def set_sfx_volume(self, volume: float):
        """设置音效音量"""
        self.SFX_VOLUME = max(0.0, min(1.0, volume))
