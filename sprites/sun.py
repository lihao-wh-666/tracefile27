"""
阳光模块
游戏中的资源道具
"""

import pygame


class Sun(pygame.sprite.Sprite):
    """阳光道具"""

    def __init__(self, x: float, y: float, value: int = 25,
                 fall_speed: float = 1.0, from_plant: bool = False,
                 resource_loader=None):
        """
        初始化阳光

        Args:
            x: 初始X坐标
            y: 初始Y坐标
            value: 阳光价值
            fall_speed: 下落速度
            from_plant: 是否来自植物
            resource_loader: 资源加载器
        """
        super().__init__()

        self.x = float(x)
        self.y = float(y)
        self.value = value
        self.fall_speed = fall_speed
        self.from_plant = from_plant
        self.resource_loader = resource_loader

        self.name = "sun"
        self.collected = False
        self.collect_callback = None

        if from_plant:
            self.target_y = y + 50
            self.fall_speed = 0.5
        else:
            self.target_y = 500
            self.fall_speed = 1.5

        self.lifetime = 10000
        self.spawn_time = 0

        self._load_image()
        self._update_position()

    def _load_image(self):
        """加载阳光图像"""
        if self.resource_loader:
            self.image = self.resource_loader.load_image(self.name)
        else:
            self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 255, 0), (20, 20), 18)
            pygame.draw.circle(self.image, (255, 200, 0), (20, 20), 18, 3)

        self.rect = self.image.get_rect()

    def _update_position(self):
        """更新位置"""
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

    def update(self, current_time: int = 0, *args, **kwargs):
        """
        更新阳光状态

        Args:
            current_time: 当前时间
        """
        if self.spawn_time == 0:
            self.spawn_time = current_time

        if self.y < self.target_y:
            self.y += self.fall_speed
            self._update_position()

        if current_time > 0 and current_time - self.spawn_time > self.lifetime:
            self.kill()

    def is_clicked(self, pos: tuple) -> bool:
        """
        检测是否被点击

        Args:
            pos: 点击位置

        Returns:
            是否被点击
        """
        return self.rect.collidepoint(pos)

    def collect(self):
        """收集阳光"""
        if not self.collected:
            self.collected = True
            if self.collect_callback:
                self.collect_callback(self.value)
            self.kill()

    def set_collect_callback(self, callback):
        """设置收集回调"""
        self.collect_callback = callback
