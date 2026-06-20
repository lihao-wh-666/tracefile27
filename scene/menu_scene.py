"""
主菜单场景模块
游戏的主菜单界面
"""

import pygame
from scene.base_scene import BaseScene
from ui.button import Button


class MenuScene(BaseScene):
    """主菜单场景"""

    def __init__(self, game_controller=None):
        super().__init__(game_controller)
        self.name = "menu"

        self.title_font = None
        self.subtitle_font = None
        self.help_font = None
        self.buttons = []

    def _on_enter(self):
        """进入菜单场景"""
        self._init_fonts()
        self._init_buttons()

    def _init_fonts(self):
        """初始化字体"""
        self.title_font = pygame.font.Font(None, 48)
        self.subtitle_font = pygame.font.Font(None, 24)
        self.help_font = pygame.font.Font(None, 18)

    def _init_buttons(self):
        """初始化按钮"""
        self.buttons = []
        screen_width = 900

        start_btn = Button(
            x=screen_width // 2 - 100,
            y=320,
            width=200,
            height=50,
            text="开始游戏",
            on_click=self._on_start_game,
            bg_color=(80, 180, 80),
            hover_color=(60, 160, 60),
            text_color=(255, 255, 255),
            font_size=24
        )
        self.buttons.append(start_btn)

        quit_btn = Button(
            x=screen_width // 2 - 100,
            y=390,
            width=200,
            height=50,
            text="退出游戏",
            on_click=self._on_quit,
            bg_color=(180, 80, 80),
            hover_color=(160, 60, 60),
            text_color=(255, 255, 255),
            font_size=24
        )
        self.buttons.append(quit_btn)

    def _on_start_game(self):
        """开始游戏按钮回调"""
        self.set_next_scene("game")

    def _on_quit(self):
        """退出按钮回调"""
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def handle_event(self, event: pygame.event.Event):
        """处理事件"""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.set_next_scene("game")
            elif event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

        for button in self.buttons:
            button.handle_event(event)

    def update(self, current_time: int, *args, **kwargs):
        """更新菜单"""
        for button in self.buttons:
            button.update(current_time)

    def render(self, surface: pygame.Surface):
        """渲染菜单"""
        surface.fill((100, 180, 100))

        title = self.title_font.render("植物大战僵尸", True, (255, 255, 255))
        title_rect = title.get_rect(center=(surface.get_width() // 2, 150))
        surface.blit(title, title_rect)

        subtitle = self.subtitle_font.render("Plants vs Zombies", True, (200, 255, 200))
        subtitle_rect = subtitle.get_rect(center=(surface.get_width() // 2, 210))
        surface.blit(subtitle, subtitle_rect)

        for button in self.buttons:
            button.draw(surface)

        help_lines = [
            "操作说明：",
            "1/2/3 - 选择植物 (向日葵/豌豆射手/坚果墙)",
            "左键 - 种植/收集阳光",
            "右键 - 取消选择",
            "ESC - 暂停/返回",
        ]
        y_offset = 480
        for line in help_lines:
            text = self.help_font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(surface.get_width() // 2, y_offset))
            surface.blit(text, text_rect)
            y_offset += 25
