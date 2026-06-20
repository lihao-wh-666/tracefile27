"""
游戏控制器模块
作为游戏主控制器，协调各模块间交互
使用场景管理器进行场景切换与生命周期管理
"""

import pygame

from res.config import GameConfig
from res.loader import ResourceLoader
from game_core.economy import EconomyManager
from game_core.level import LevelManager
from game_core.collision import CollisionManager

from scene.scene_manager import SceneManager
from scene.menu_scene import MenuScene
from scene.game_scene import GameScene
from scene.pause_scene import PauseScene
from scene.end_scene import EndScene


class GameController:
    """游戏主控制器，协调所有模块"""

    def __init__(self, config: GameConfig):
        """
        初始化游戏控制器

        Args:
            config: 游戏配置对象
        """
        self.config = config
        self.resource_loader = ResourceLoader(config)
        self.economy = EconomyManager(config.INITIAL_SUN)
        self.level_manager = LevelManager()
        self.collision_manager = CollisionManager()
        self.scene_manager = SceneManager()

        self.screen = None
        self.clock = None
        self.current_time = 0

        self._init_window()
        self._init_scenes()

    def _init_window(self):
        """初始化游戏窗口"""
        flags = 0
        if self.config.FULLSCREEN:
            flags = pygame.FULLSCREEN

        self.screen = pygame.display.set_mode(
            (self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT),
            flags
        )
        pygame.display.set_caption(self.config.WINDOW_TITLE)
        self.clock = pygame.time.Clock()

    def _init_scenes(self):
        """初始化所有场景"""
        menu_scene = MenuScene(self)
        game_scene = GameScene(self)
        pause_scene = PauseScene(self)
        win_scene = EndScene(self, is_win=True)
        lose_scene = EndScene(self, is_win=False)

        self.scene_manager.register_scene("menu", menu_scene)
        self.scene_manager.register_scene("game", game_scene)
        self.scene_manager.register_scene("pause", pause_scene)
        self.scene_manager.register_scene("win", win_scene)
        self.scene_manager.register_scene("lose", lose_scene)

        self.scene_manager.switch_scene("menu")

    def run(self):
        """游戏主循环"""
        running = True
        while running:
            self.current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self._handle_event(event)

            self._update()
            self._render()

            self.clock.tick(self.config.FPS)

    def _handle_event(self, event: pygame.event.Event):
        """处理事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                self._toggle_fullscreen()

        self.scene_manager.handle_event(event)

    def _toggle_fullscreen(self):
        """切换全屏"""
        self.config.toggle_fullscreen()
        flags = 0
        if self.config.FULLSCREEN:
            flags = pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(
            (self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT),
            flags
        )

    def _update(self):
        """更新游戏状态"""
        self.scene_manager.update(self.current_time)

    def _render(self):
        """渲染画面"""
        self.scene_manager.render(self.screen)
        pygame.display.flip()

    def get_current_scene(self):
        """获取当前场景"""
        return self.scene_manager.get_current_scene()

    def switch_scene(self, scene_name: str, data: dict = None):
        """切换场景"""
        self.scene_manager.switch_scene(scene_name, data)

    def toggle_fullscreen(self):
        """切换全屏模式"""
        self._toggle_fullscreen()

    def set_bgm_volume(self, volume: float):
        """设置背景音乐音量"""
        self.config.set_bgm_volume(volume)
        if self.resource_loader:
            pass

    def set_sfx_volume(self, volume: float):
        """设置音效音量"""
        self.config.set_sfx_volume(volume)
