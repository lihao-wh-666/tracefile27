"""
结束场景模块
游戏胜利/失败界面
"""

import pygame
from scene.base_scene import BaseScene
from ui.button import Button
from ui.font_utils import get_font


class EndScene(BaseScene):
    """结束场景（胜利/失败）"""

    def __init__(self, game_controller=None, is_win: bool = False):
        super().__init__(game_controller)
        self.name = "end"
        self.is_win = is_win

        self.title_font = None
        self.text_font = None
        self.buttons = []

    def _on_enter(self):
        """进入结束场景"""
        if "is_win" in self.scene_data:
            self.is_win = self.scene_data["is_win"]

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

        restart_btn = Button(
            x=screen_width // 2 - 100,
            y=320,
            width=200,
            height=50,
            text="重新开始",
            on_click=self._on_restart,
            bg_color=(80, 180, 80),
            hover_color=(60, 160, 60),
            text_color=(255, 255, 255),
            font_size=24
        )
        self.buttons.append(restart_btn)

        menu_btn = Button(
            x=screen_width // 2 - 100,
            y=390,
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
            if event.key in (pygame.K_r, pygame.K_RETURN):
                self.scene_data["restart"] = True
                self.set_next_scene("game")
            elif event.key in (pygame.K_m, pygame.K_ESCAPE):
                self.set_next_scene("menu")

        for button in self.buttons:
            button.handle_event(event)

    def update(self, current_time: int, *args, **kwargs):
        """更新结束场景"""
        for button in self.buttons:
            button.update(current_time)

    def render(self, surface: pygame.Surface):
        """渲染结束界面"""
        overlay = pygame.Surface((surface.get_width(), surface.get_height()))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        if self.is_win:
            title_color = (255, 255, 0)
            title_text = "胜利！"
            sub_text = "恭喜你成功抵御了僵尸入侵！"
        else:
            title_color = (255, 0, 0)
            title_text = "游戏结束"
            sub_text = "僵尸入侵了你的房子！"

        title = self.title_font.render(title_text, True, title_color)
        title_rect = title.get_rect(center=(surface.get_width() // 2, 180))
        surface.blit(title, title_rect)

        subtitle = self.text_font.render(sub_text, True, (255, 255, 255))
        subtitle_rect = subtitle.get_rect(center=(surface.get_width() // 2, 250))
        surface.blit(subtitle, subtitle_rect)

        for button in self.buttons:
            button.draw(surface)

        hint_text = self.text_font.render(
            "按 R 或 Enter 重开 | M 或 ESC 返回菜单",
            True, (200, 200, 200)
        )
        hint_rect = hint_text.get_rect(center=(surface.get_width() // 2, 520))
        surface.blit(hint_text, hint_rect)
