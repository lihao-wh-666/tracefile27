"""
路障僵尸模块
高血量的僵尸类型，戴着路障帽子
"""

from sprites.base.zombie import ZombieBase


class ConeZombie(ZombieBase):
    """路障僵尸：血量更高的僵尸"""

    def __init__(self, row: int, x: float, grid_offset_x: int, grid_offset_y: int,
                 cell_width: int, cell_height: int, resource_loader=None):
        super().__init__(row, x, grid_offset_x, grid_offset_y,
                         cell_width, cell_height, resource_loader)

        self.name = "cone_zombie"
        self.hp = 200
        self.max_hp = 200
        self.speed = 0.4
        self.attack_damage = 25
        self.attack_interval = 1000
