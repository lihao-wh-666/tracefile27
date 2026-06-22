"""
植物基类模块
定义所有植物的通用属性和行为
"""

import pygame
from typing import Tuple


class PlantBase(pygame.sprite.Sprite):
    """植物基类，所有植物的父类"""

    def __init__(self, row: int, col: int, grid_offset_x: int, grid_offset_y: int,
                 cell_width: int, cell_height: int, resource_loader=None):
        """
        初始化植物

        Args:
            row: 所在网格行
            col: 所在网格列
            grid_offset_x: 网格X偏移
            grid_offset_y: 网格Y偏移
            cell_width: 单元格宽度
            cell_height: 单元格高度
            resource_loader: 资源加载器
        """
        super().__init__()

        self.row = row
        self.col = col
        self.grid_offset_x = grid_offset_x
        self.grid_offset_y = grid_offset_y
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.resource_loader = resource_loader

        self.name: str = "plant"
        self.hp: int = 100
        self.max_hp: int = 100
        self.cost: int = 50
        self.attack_damage: int = 0
        self.attack_interval: int = 0
        self.last_attack_time: int = 0

        self._load_image()
        self._update_position()

    def _load_image(self):
        """加载植物图像"""
        target_width = int(self.cell_width * 0.75)
        target_height = int(self.cell_height * 0.75)

        if self.resource_loader:
            self.image = self.resource_loader.load_image(self.name)
            if self.image.get_width() != target_width or self.image.get_height() != target_height:
                self.image = pygame.transform.smoothscale(self.image, (target_width, target_height))
        else:
            self.image = pygame.Surface((target_width, target_height), pygame.SRCALPHA)
            pygame.draw.ellipse(self.image, (34, 139, 34), (0, 0, target_width, target_height))

        self.rect = self.image.get_rect()

    def _update_position(self):
        """根据网格位置更新实际像素坐标"""
        center_x = self.grid_offset_x + self.col * self.cell_width + self.cell_width // 2
        center_y = self.grid_offset_y + self.row * self.cell_height + self.cell_height // 2
        self.rect.center = (center_x, center_y)

    def update(self, current_time: int, *args, **kwargs):
        """
        更新植物状态

        Args:
            current_time: 当前时间（毫秒）
        """
        pass

    def take_damage(self, damage: int) -> bool:
        """
        受到伤害

        Args:
            damage: 伤害值

        Returns:
            是否死亡
        """
        self.hp -= damage
        if self.hp <= 0:
            self.kill()
            return True
        return False

    def can_attack(self, current_time: int) -> bool:
        """
        判断是否可以攻击

        Args:
            current_time: 当前时间

        Returns:
            是否可以攻击
        """
        if self.attack_damage <= 0 or self.attack_interval <= 0:
            return False
        return current_time - self.last_attack_time >= self.attack_interval

    def get_grid_pos(self) -> Tuple[int, int]:
        """获取网格位置"""
        return self.row, self.col

    def draw_hp_bar(self, surface: pygame.Surface):
        """绘制血条"""
        if self.hp < self.max_hp:
            bar_width = self.rect.width
            bar_height = 4
            bar_x = self.rect.left
            bar_y = self.rect.top - 8

            pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))

            hp_ratio = self.hp / self.max_hp
            pygame.draw.rect(surface, (0, 255, 0),
                             (bar_x, bar_y, int(bar_width * hp_ratio), bar_height))
