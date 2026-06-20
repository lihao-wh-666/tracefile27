"""
普通僵尸模块
最基础的僵尸类型
"""

from sprites.base.zombie import ZombieBase


class NormalZombie(ZombieBase):
    """普通僵尸：基础僵尸类型"""

    def __init__(self, row: int, x: float, grid_offset_x: int, grid_offset_y: int,
                 cell_width: int, cell_height: int, resource_loader=None):
        super().__init__(row, x, grid_offset_x, grid_offset_y,
                         cell_width, cell_height, resource_loader)

        self.name = "normal_zombie"
        self.hp = 100
        self.max_hp = 100
        self.speed = 0.5
        self.attack_damage = 20
        self.attack_interval = 1000
