"""
豌豆子弹模块
豌豆射手发射的子弹
"""

import pygame


class PeaBullet(pygame.sprite.Sprite):
    """豌豆子弹"""

    def __init__(self, x: float, y: float, row: int, speed: float = 5,
                 damage: int = 20, resource_loader=None):
        """
        初始化豌豆子弹

        Args:
            x: 初始X坐标
            y: 初始Y坐标
            row: 所在行
            speed: 移动速度
            damage: 伤害值
            resource_loader: 资源加载器
        """
        super().__init__()

        self.x = float(x)
        self.y = float(y)
        self.row = row
        self.speed = speed
        self.damage = damage
        self.resource_loader = resource_loader

        self.name = "pea_bullet"
        self.active = True

        self._load_image()
        self._update_position()

    def _load_image(self):
        """加载子弹图像"""
        if self.resource_loader:
            self.image = self.resource_loader.load_image(self.name)
        else:
            self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (0, 200, 0), (7, 7), 7)
            pygame.draw.circle(self.image, (0, 100, 0), (7, 7), 7, 2)

        self.rect = self.image.get_rect()

    def _update_position(self):
        """更新位置"""
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

    def update(self, *args, **kwargs):
        """更新子弹位置"""
        if self.active:
            self.x += self.speed
            self._update_position()

            screen_width = kwargs.get("screen_width", 900)
            if self.x > screen_width + 50:
                self.kill()

    def hit_zombie(self):
        """命中僵尸后销毁"""
        self.kill()

    def get_damage(self) -> int:
        """获取伤害值"""
        return self.damage
