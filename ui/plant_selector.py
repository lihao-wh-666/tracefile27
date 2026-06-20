"""
植物选择栏组件
显示可选择的植物卡片
"""

import pygame
from typing import List, Dict, Callable, Optional, Tuple


class PlantCard:
    """植物卡片"""

    def __init__(self, plant_type: str, name: str, cost: int,
                 x: int, y: int, width: int = 100, height: int = 70,
                 color: Tuple[int, int, int] = (0, 255, 0)):
        """
        初始化植物卡片

        Args:
            plant_type: 植物类型
            name: 显示名称
            cost: 花费阳光
            x: X坐标
            y: Y坐标
            width: 宽度
            height: 高度
            color: 植物颜色
        """
        self.plant_type = plant_type
        self.name = name
        self.cost = cost
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.selected = False
        self.can_afford = True
        self.cooldown_remaining = 0

        self.name_font = pygame.font.Font(None, 14)
        self.cost_font = pygame.font.Font(None, 16)

    def set_position(self, x: int, y: int):
        """设置位置"""
        self.rect.x = x
        self.rect.y = y

    def set_selected(self, selected: bool):
        """设置是否选中"""
        self.selected = selected

    def set_can_afford(self, can_afford: bool):
        """设置是否负担得起"""
        self.can_afford = can_afford

    def set_cooldown(self, remaining: int):
        """设置冷却剩余时间"""
        self.cooldown_remaining = remaining

    def is_clicked(self, pos: Tuple[int, int]) -> bool:
        """检测是否被点击"""
        return self.rect.collidepoint(pos) and self.can_afford and self.cooldown_remaining <= 0

    def draw(self, surface: pygame.Surface):
        """绘制卡片"""
        if self.selected:
            bg_color = (255, 255, 100)
        elif self.can_afford and self.cooldown_remaining <= 0:
            bg_color = (200, 200, 200)
        else:
            bg_color = (100, 100, 100)

        pygame.draw.rect(surface, bg_color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)

        icon_x = self.rect.left + 25
        icon_y = self.rect.centery
        pygame.draw.circle(surface, self.color, (icon_x, icon_y), 20)
        pygame.draw.circle(surface, (0, 0, 0), (icon_x, icon_y), 20, 2)

        name_text = self.name_font.render(self.name, True, (0, 0, 0))
        name_rect = name_text.get_rect(
            left=self.rect.left + 50,
            top=self.rect.top + 10
        )
        surface.blit(name_text, name_rect)

        cost_color = (0, 0, 0) if self.can_afford else (255, 0, 0)
        cost_text = self.cost_font.render(f"☀ {self.cost}", True, cost_color)
        cost_rect = cost_text.get_rect(
            left=self.rect.left + 50,
            bottom=self.rect.bottom - 10
        )
        surface.blit(cost_text, cost_rect)

        if self.cooldown_remaining > 0:
            cooldown_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            cooldown_surface.fill((128, 128, 128, 180))
            surface.blit(cooldown_surface, self.rect)


class PlantSelector:
    """植物选择栏"""

    def __init__(self, x: int, y: int, plants_config: List[Dict],
                 on_select: Optional[Callable[[str], None]] = None):
        """
        初始化植物选择栏

        Args:
            x: X坐标
            y: Y坐标
            plants_config: 植物配置列表
            on_select: 选中回调
        """
        self.x = x
        self.y = y
        self.on_select = on_select
        self.selected_plant: Optional[str] = None
        self.cards: List[PlantCard] = []

        self._init_cards(plants_config)

    def _init_cards(self, plants_config: List[Dict]):
        """初始化植物卡片"""
        card_width = 100
        card_height = 70
        spacing = 10

        for i, config in enumerate(plants_config):
            card_x = self.x + i * (card_width + spacing)
            card = PlantCard(
                plant_type=config["type"],
                name=config["name"],
                cost=config["cost"],
                x=card_x,
                y=self.y,
                width=card_width,
                height=card_height,
                color=config.get("color", (0, 255, 0))
            )
            self.cards.append(card)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        处理事件

        Args:
            event: Pygame事件

        Returns:
            是否处理了事件
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for card in self.cards:
                if card.is_clicked(event.pos):
                    self._select_plant(card.plant_type)
                    return True
        return False

    def _select_plant(self, plant_type: str):
        """选择植物"""
        if self.selected_plant == plant_type:
            self.selected_plant = None
        else:
            self.selected_plant = plant_type

        for card in self.cards:
            card.set_selected(card.plant_type == self.selected_plant)

        if self.on_select and self.selected_plant:
            self.on_select(self.selected_plant)

    def update(self, sun_count: int, cooldowns: Dict[str, int] = None):
        """
        更新选择栏状态

        Args:
            sun_count: 当前阳光数量
            cooldowns: 冷却时间字典
        """
        for card in self.cards:
            card.set_can_afford(sun_count >= card.cost)
            if cooldowns and card.plant_type in cooldowns:
                card.set_cooldown(cooldowns[card.plant_type])
            else:
                card.set_cooldown(0)

    def clear_selection(self):
        """清除选择"""
        self.selected_plant = None
        for card in self.cards:
            card.set_selected(False)

    def get_selected_plant(self) -> Optional[str]:
        """获取选中的植物类型"""
        return self.selected_plant

    def draw(self, surface: pygame.Surface):
        """绘制植物选择栏"""
        for card in self.cards:
            card.draw(surface)

    def get_width(self) -> int:
        """获取总宽度"""
        if not self.cards:
            return 0
        last_card = self.cards[-1]
        return last_card.rect.right - self.x

    def get_height(self) -> int:
        """获取高度"""
        if not self.cards:
            return 0
        return self.cards[0].rect.height
