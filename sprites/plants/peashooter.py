"""
豌豆射手模块
发射豌豆攻击僵尸的植物
"""

import pygame
from sprites.base.plant import PlantBase


class Peashooter(PlantBase):
    """豌豆射手：发射豌豆攻击僵尸"""

    def __init__(self, row: int, col: int, grid_offset_x: int, grid_offset_y: int,
                 cell_width: int, cell_height: int, resource_loader=None):
        super().__init__(row, col, grid_offset_x, grid_offset_y,
                         cell_width, cell_height, resource_loader, name="peashooter")
        self.hp = 100
        self.max_hp = 100
        self.cost = 100
        self.attack_damage = 20
        self.attack_interval = 1500
        self.bullet_speed = 5
        self.bullet_spawn_callback = None

    def update(self, current_time: int, zombies_group: pygame.sprite.Group = None,
               *args, **kwargs):
        """
        更新豌豆射手状态，检测并攻击僵尸

        Args:
            current_time: 当前时间
            zombies_group: 僵尸精灵组
        """
        if zombies_group and self.can_attack(current_time):
            if self._has_zombie_in_row(zombies_group):
                self._shoot()
                self.last_attack_time = current_time

    def _has_zombie_in_row(self, zombies_group: pygame.sprite.Group) -> bool:
        """
        检查同行是否有僵尸

        Args:
            zombies_group: 僵尸精灵组

        Returns:
            是否有僵尸
        """
        for zombie in zombies_group:
            if zombie.row == self.row and zombie.rect.left > self.rect.right:
                return True
        return False

    def _shoot(self):
        """发射豌豆"""
        if self.bullet_spawn_callback:
            bullet_x = self.rect.right
            bullet_y = self.rect.centery
            self.bullet_spawn_callback(bullet_x, bullet_y, self.row,
                                       self.bullet_speed, self.attack_damage)

    def set_bullet_spawn_callback(self, callback):
        """设置子弹生成回调"""
        self.bullet_spawn_callback = callback
