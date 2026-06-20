"""
碰撞检测模块
管理游戏中的各种碰撞检测逻辑
"""

import pygame
from typing import List


class CollisionManager:
    """碰撞检测管理器"""

    def __init__(self):
        """初始化碰撞管理器"""
        pass

    def check_bullet_zombie_collisions(self, bullets: pygame.sprite.Group,
                                       zombies: pygame.sprite.Group) -> List[tuple]:
        """
        检测子弹与僵尸的碰撞

        Args:
            bullets: 子弹精灵组
            zombies: 僵尸精灵组

        Returns:
            碰撞对列表 [(bullet, zombie), ...]
        """
        collisions = []
        for bullet in bullets:
            hit_zombies = pygame.sprite.spritecollide(bullet, zombies, False)
            for zombie in hit_zombies:
                if bullet.row == zombie.row:
                    collisions.append((bullet, zombie))
        return collisions

    def check_zombie_plant_collisions(self, zombies: pygame.sprite.Group,
                                      plants: pygame.sprite.Group) -> List[tuple]:
        """
        检测僵尸与植物的碰撞

        Args:
            zombies: 僵尸精灵组
            plants: 植物精灵组

        Returns:
            碰撞对列表 [(zombie, plant), ...]
        """
        collisions = []
        for zombie in zombies:
            if zombie.is_eating:
                continue
            hit_plants = pygame.sprite.spritecollide(zombie, plants, False)
            for plant in hit_plants:
                if zombie.row == plant.row:
                    collisions.append((zombie, plant))
        return collisions

    def check_sun_click_collision(self, suns: pygame.sprite.Group,
                                  click_pos: tuple) -> List[pygame.sprite.Sprite]:
        """
        检测点击是否命中阳光

        Args:
            suns: 阳光精灵组
            click_pos: 点击位置 (x, y)

        Returns:
            被点击的阳光列表
        """
        clicked_suns = []
        for sun in suns:
            if sun.rect.collidepoint(click_pos):
                clicked_suns.append(sun)
        return clicked_suns

    def check_zombie_reach_house(self, zombies: pygame.sprite.Group,
                                 house_x: int) -> List[pygame.sprite.Sprite]:
        """
        检测僵尸是否到达房子

        Args:
            zombies: 僵尸精灵组
            house_x: 房子的X坐标

        Returns:
            到达房子的僵尸列表
        """
        reached = []
        for zombie in zombies:
            if zombie.x <= house_x:
                reached.append(zombie)
        return reached
