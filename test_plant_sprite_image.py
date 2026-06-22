"""
测试植物精灵是否正确加载对应图片（而非占位图）
"""

import pygame
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from res.config import GameConfig
from res.loader import ResourceLoader
from sprites.plants.sunflower import Sunflower
from sprites.plants.peashooter import Peashooter
from sprites.plants.wallnut import WallNut


def test_plant_sprite_images():
    """测试植物精灵是否正确加载对应图片"""
    pygame.init()
    pygame.display.set_mode((100, 100))

    config = GameConfig()
    resource_loader = ResourceLoader(config)

    print("=" * 60)
    print("【植物精灵图片加载测试】")
    print("=" * 60)

    plant_classes = [
        ("向日葵", "sunflower", Sunflower),
        ("豌豆射手", "peashooter", Peashooter),
        ("坚果墙", "wallnut", WallNut),
    ]

    all_passed = True

    for name_cn, name_en, plant_class in plant_classes:
        print(f"\n  植物: {name_cn} ({name_en})")

        plant = plant_class(
            row=0, col=0,
            grid_offset_x=config.GRID_OFFSET_X,
            grid_offset_y=config.GRID_OFFSET_Y,
            cell_width=config.CELL_WIDTH,
            cell_height=config.CELL_HEIGHT,
            resource_loader=resource_loader
        )

        print(f"    植物名称属性: {plant.name}")

        cache_key = name_en
        is_cached = cache_key in resource_loader._image_cache
        print(f"    图片缓存键存在: {is_cached}")

        if is_cached:
            cached_img = resource_loader._image_cache[cache_key]
            img_size = cached_img.get_size()
            print(f"    缓存图片尺寸: {img_size}")

            placeholder_size_map = {
                "sunflower": (70, 70),
                "peashooter": (70, 70),
                "wallnut": (70, 70),
            }
            placeholder_size = placeholder_size_map.get(name_en, (60, 60))

            is_placeholder = (img_size == placeholder_size)
            if is_placeholder:
                print(f"    ❌ 警告: 图片可能是占位图 (尺寸与占位图一致)")
                all_passed = False
            else:
                print(f"    ✓ 图片尺寸正常 (不是占位图)")

            sprite_size = plant.image.get_size()
            print(f"    精灵显示尺寸: {sprite_size}")
            print(f"    ✓ 精灵创建成功")

    print("\n" + "=" * 60)
    if all_passed:
        print("✓ 所有植物精灵图片加载测试通过！")
    else:
        print("✗ 部分测试失败，请检查图片加载逻辑")
    print("=" * 60)

    pygame.quit()
    return all_passed


if __name__ == "__main__":
    success = test_plant_sprite_images()
    sys.exit(0 if success else 1)
