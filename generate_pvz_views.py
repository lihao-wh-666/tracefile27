import urllib.request
import urllib.parse
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLANTS_DIR = os.path.join(BASE_DIR, "assets", "images", "plants")

API_URL = "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image"

def download_image(prompt, save_path, image_size="square_hd"):
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"{API_URL}?prompt={encoded_prompt}&image_size={image_size}"
    print(f"  生成中: {os.path.basename(save_path)}", end="", flush=True)
    try:
        urllib.request.urlretrieve(url, save_path)
        size_kb = os.path.getsize(save_path) / 1024
        print(f" ✓ ({size_kb:.1f} KB)")
        return True
    except Exception as e:
        print(f" ✗ 失败: {e}")
        return False

def generate_pvz_multi_views():
    print("=" * 60)
    print("生成经典PvZ风格多视图植物图片")
    print("=" * 60)

    plants_config = {
        "sunflower": {
            "cn_name": "向日葵",
            "base_style": "Plants vs Zombies cartoon style, bold black outline, vibrant colors, game art",
            "views": {
                "front": "Front view of a cute cartoon sunflower character, bright yellow petals, brown center with smiling face, green stem with leaves, Plants vs Zombies style, bold black outline, vibrant colors, game art, isolated on white background",
                "side": "Side view profile of a cute cartoon sunflower character, yellow flower head facing right, green stem and leaves from side, Plants vs Zombies style, bold black outline, vibrant colors, game art, isolated on white background",
                "top": "Top view looking down on a cute cartoon sunflower, yellow radial petals surrounding brown center disk, Plants vs Zombies style, bold black outline, vibrant colors, game art, isolated on white background, flat lay view from above",
            }
        },
        "peashooter": {
            "cn_name": "豌豆射手",
            "base_style": "Plants vs Zombies cartoon style, bold black outline, vibrant colors, game art",
            "views": {
                "front": "Front view of a cute cartoon pea shooter plant character, green pea pod head with eyes, green leaves and stem, Plants vs Zombies style, bold black outline, vibrant green colors, game art, isolated on white background",
                "side": "Side view profile of a cute cartoon pea shooter plant character, green pea pod head facing right ready to shoot, green leaves, Plants vs Zombies style, bold black outline, vibrant green colors, game art, isolated on white background",
                "top": "Top view looking down on a cute cartoon pea shooter plant, green pea head with surrounding leaves, Plants vs Zombies style, bold black outline, vibrant green colors, game art, isolated on white background, overhead view",
            }
        },
        "wallnut": {
            "cn_name": "坚果墙",
            "base_style": "Plants vs Zombies cartoon style, bold black outline, vibrant colors, game art",
            "views": {
                "front": "Front view of a cute cartoon walnut wall-nut character, brown tough shell with determined face, thick brown texture, Plants vs Zombies style, bold black outline, warm brown colors, game art, isolated on white background",
                "side": "Side view profile of a cute cartoon walnut wall-nut character, brown round shell from side, tough expression, Plants vs Zombies style, bold black outline, warm brown colors, game art, isolated on white background",
                "top": "Top view looking down on a cute cartoon walnut wall-nut, brown round shell with texture from above, Plants vs Zombies style, bold black outline, warm brown colors, game art, isolated on white background, overhead view",
            }
        },
    }

    total = sum(len(p["views"]) for p in plants_config.values())
    count = 0

    for plant_key, plant_info in plants_config.items():
        print(f"\n📌 {plant_info['cn_name']} ({plant_key})")

        plant_dir = os.path.join(PLANTS_DIR, plant_key)
        os.makedirs(plant_dir, exist_ok=True)

        for view_name, prompt in plant_info["views"].items():
            count += 1
            save_path = os.path.join(plant_dir, f"{view_name}_{plant_key}.png")
            download_image(prompt, save_path)
            time.sleep(1)

    print(f"\n完成! 共生成 {count} 张多视图图片")
    print("目录: " + PLANTS_DIR)

if __name__ == "__main__":
    generate_pvz_multi_views()
