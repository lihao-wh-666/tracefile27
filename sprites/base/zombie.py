"""
僵尸基类模块
定义所有僵尸的通用属性和行为
"""

import pygame
from typing import Tuple, Optional


class ZombieBase(pygame.sprite.Sprite):
    """僵尸基类，所有僵尸的父类"""

    def __init__(self, row: int, x: float, grid_offset_x: int, grid_offset_y: int,
                 cell_width: int, cell_height: int, resource_loader=None):
        """
        初始化僵尸

        Args:
            row: 所在行
            x: 初始X坐标
            grid_offset_x: 网格X偏移
            grid_offset_y: 网格Y偏移
            cell_width: 单元格宽度
            cell_height: 单元格高度
            resource_loader: 资源加载器
        """
        super().__init__()

        self.row = row
        self.x = float(x)
        self.grid_offset_x = grid_offset_x
        self.grid_offset_y = grid_offset_y
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.resource_loader = resource_loader

        self.name: str = "zombie"
        self.hp: int = 100
        self.max_hp: int = 100
        self.speed: float = 0.5
        self.attack_damage: int = 20
        self.attack_interval: int = 1000
        self.last_attack_time: int = 0

        self.is_eating: bool = False
        self.target_plant: Optional[pygame.sprite.Sprite] = None

        self._load_image()
        self._update_position()

    def _load_image(self):
        """加载僵尸图像"""
        if self.resource_loader:
            self.image = self.resource_loader.load_image(self.name)
        else:
            self.image = pygame.Surface((50, 80), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (128, 128, 128), (0, 0, 50, 80))

        self.rect = self.image.get_rect()

    def _update_position(self):
        """根据坐标更新rect位置"""
        center_y = self.grid_offset_y + self.row * self.cell_height + self.cell_height // 2
        self.rect.centerx = int(self.x)
        self.rect.centery = center_y

    def update(self, current_time: int, plants_group: pygame.sprite.Group = None,
               *args, **kwargs):
        """
        更新僵尸状态

        Args:
            current_time: 当前时间（毫秒）
            plants_group: 植物精灵组
        """
        if self.is_eating and self.target_plant and self.target_plant.alive():
            self._attack_plant(current_time)
        else:
            self.is_eating = False
            self.target_plant = None
            self._move()

        self._update_position()

    def _move(self):
        """僵尸向左移动"""
        self.x -= self.speed

    def _attack_plant(self, current_time: int):
        """
        攻击植物

        Args:
            current_time: 当前时间
        """
        if current_time - self.last_attack_time >= self.attack_interval:
            if self.target_plant and self.target_plant.alive():
                self.target_plant.take_damage(self.attack_damage)
                self.last_attack_time = current_time

    def check_collision_with_plant(self, plants_group: pygame.sprite.Group):
        """
        检测与植物的碰撞

        Args:
            plants_group: 植物精灵组
        """
        collided_plants = pygame.sprite.spritecollide(self, plants_group, False)
        for plant in collided_plants:
            if plant.row == self.row:
                self.is_eating = True
                self.target_plant = plant
                return

        self.is_eating = False
        self.target_plant = None

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

    def get_grid_pos(self) -> Tuple[int, int]:
        """获取所在网格行和大致列"""
        col = int((self.x - self.grid_offset_x) / self.cell_width)
        return self.row, col

    def has_reached_house(self, house_x: int) -> bool:
        """
        检查是否到达房子

        Args:
            house_x: 房子的X坐标

        Returns:
            是否到达
        """
        return self.x <= house_x

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
