"""
向日葵模块
产生阳光的植物
"""

import pygame
from sprites.base.plant import PlantBase


class Sunflower(PlantBase):
    """向日葵：定期产生阳光"""

    def __init__(self, row: int, col: int, grid_offset_x: int, grid_offset_y: int,
                 cell_width: int, cell_height: int, resource_loader=None):
        super().__init__(row, col, grid_offset_x, grid_offset_y,
                         cell_width, cell_height, resource_loader)

        self.name = "sunflower"
        self.hp = 100
        self.max_hp = 100
        self.cost = 50
        self.sun_produce_interval = 8000
        self.last_sun_time = 0
        self.sun_value = 25
        self.sun_spawn_callback = None

    def update(self, current_time: int, *args, **kwargs):
        """
        更新向日葵状态，定期产生阳光

        Args:
            current_time: 当前时间
        """
        if current_time - self.last_sun_time >= self.sun_produce_interval:
            self._produce_sun()
            self.last_sun_time = current_time

    def _produce_sun(self):
        """产生阳光"""
        if self.sun_spawn_callback:
            sun_x = self.rect.centerx
            sun_y = self.rect.top
            self.sun_spawn_callback(sun_x, sun_y, True)

    def set_sun_spawn_callback(self, callback):
        """设置阳光生成回调"""
        self.sun_spawn_callback = callback
