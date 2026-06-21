"""
暂停场景模块
游戏暂停界面
"""

import pygame
from scene.base_scene import BaseScene
from ui.button import Button
from ui.font_utils import get_font


class PauseScene(BaseScene):
    """暂停场景"""

    def __init__(self, game_controller=None):
        super().__init__(game_controller)
        self.name = "pause"

        self.title_font = None
        self.text_font = None
        self.buttons = []

    def _on_enter(self):
        """进入暂停场景"""
        self._init_fonts()
        self._init_buttons()

    def _init_fonts(self):
        """初始化字体"""
        self.title_font = get_font(48, bold=True)
        self.text_font = get_font(24)

    def _init_buttons(self):
        """初始化按钮"""
        self.buttons = []
        screen_width = 900

        resume_btn = Button(
            x=screen_width // 2 - 100,
            y=280,
            width=200,
            height=50,
            text="继续游戏",
            on_click=self._on_resume,
            bg_color=(80, 180, 80),
            hover_color=(60, 160, 60),
            text_color=(255, 255, 255),
            font_size=24
        )
        self.buttons.append(resume_btn)

        restart_btn = Button(
            x=screen_width // 2 - 100,
            y=350,
            width=200,
            height=50,
            text="重新开始",
            on_click=self._on_restart,
            bg_color=(200, 180, 80),
            hover_color=(180, 160, 60),
            text_color=(255, 255, 255),
            font_size=24
        )
        self.buttons.append(restart_btn)

        menu_btn = Button(
            x=screen_width // 2 - 100,
            y=420,
            width=200,
            height=50,
            text="返回主菜单",
            on_click=self._on_menu,
            bg_color=(180, 80, 80),
            hover_color=(160, 60, 60),
            text_color=(255, 255, 255),
            font_size=24
        )
        self.buttons.append(menu_btn)

    def _on_resume(self):
        """继续游戏"""
        self.set_next_scene("game", {"from_pause": True})

    def _on_restart(self):
        """重新开始"""
        self.scene_data["restart"] = True
        self.set_next_scene("game")

    def _on_menu(self):
        """返回主菜单"""
        self.set_next_scene("menu")

    def handle_event(self, event: pygame.event.Event):
        """处理事件"""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_p):
                self.set_next_scene("game", {"from_pause": True})
            elif event.key == pygame.K_r:
                self.scene_data["restart"] = True
                self.set_next_scene("game")
            elif event.key == pygame.K_m:
                self.set_next_scene("menu")

        for button in self.buttons:
            button.handle_event(event)

    def update(self, current_time: int, *args, **kwargs):
        """更新暂停场景"""
        for button in self.buttons:
            button.update(current_time)

    def render(self, surface: pygame.Surface):
        """渲染暂停界面"""
        overlay = pygame.Surface((surface.get_width(), surface.get_height()))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        title = self.title_font.render("游戏暂停", True, (255, 255, 255))
        title_rect = title.get_rect(center=(surface.get_width() // 2, 180))
        surface.blit(title, title_rect)

        for button in self.buttons:
            button.draw(surface)

        hint_text = self.text_font.render(
            "按 ESC 或 P 继续 | R 重开 | M 菜单",
            True, (200, 200, 200)
        )
        hint_rect = hint_text.get_rect(center=(surface.get_width() // 2, 520))
        surface.blit(hint_text, hint_rect)
