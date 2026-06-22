"""
坚果墙模块
高血量的防御植物
"""

import pygame
from sprites.base.plant import PlantBase


class WallNut(PlantBase):
    """坚果墙：高血量防御植物"""

    def __init__(self, row: int, col: int, grid_offset_x: int, grid_offset_y: int,
                 cell_width: int, cell_height: int, resource_loader=None):
        super().__init__(row, col, grid_offset_x, grid_offset_y,
                         cell_width, cell_height, resource_loader, name="wallnut")
        self.hp = 400
        self.max_hp = 400
        self.cost = 50
        self.attack_damage = 0
        self.attack_interval = 0

    def update(self, current_time: int, *args, **kwargs):
        """
        坚果墙不主动攻击，只更新状态

        Args:
            current_time: 当前时间
        """
        pass
