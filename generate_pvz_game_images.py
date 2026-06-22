import urllib.request
import urllib.parse
import os
import time
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "assets", "images")
PLANTS_DIR = os.path.join(IMAGES_DIR, "plants")
PREVIEW_DIR = os.path.join(IMAGES_DIR, "plants_preview")

API_URL = "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image"

def download_image(prompt, save_path, image_size="square_hd"):
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"{API_URL}?prompt={encoded_prompt}&image_size={image_size}"
    print(f"正在生成: {os.path.basename(save_path)}")
    try:
        urllib.request.urlretrieve(url, save_path)
        size_kb = os.path.getsize(save_path) / 1024
        with Image.open(save_path) as img:
            original_size = img.size
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            target_size = (1832, 1832)
            if img.size != target_size:
                img = img.resize(target_size, Image.LANCZOS)
                img.save(save_path, 'PNG')
        print(f"  完成! 原始尺寸: {original_size}, 调整后: {target_size}, 文件大小: {size_kb:.1f} KB")
        return True
    except Exception as e:
        print(f"  失败: {e}")
        return False

def process_downloaded_image(image_url, save_path):
    print(f"正在下载: {os.path.basename(save_path)}")
    try:
        urllib.request.urlretrieve(image_url, save_path)
        with Image.open(save_path) as img:
            original_size = img.size
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            bg = Image.new('RGBA', img.size, (255, 255, 255, 0))
            bg.paste(img, (0, 0), img)
            img = bg
            
            target_size = (1832, 1832)
            if img.size != target_size:
                ratio = min(target_size[0] / img.size[0], target_size[1] / img.size[1])
                new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                img = img.resize(new_size, Image.LANCZOS)
                
                final_img = Image.new('RGBA', target_size, (255, 255, 255, 0))
                offset = ((target_size[0] - new_size[0]) // 2, 
                         (target_size[1] - new_size[1]) // 2)
                final_img.paste(img, offset)
                final_img.save(save_path, 'PNG')
        
        size_kb = os.path.getsize(save_path) / 1024
        print(f"  完成! 原始尺寸: {original_size}, 调整后: {target_size}, 文件大小: {size_kb:.1f} KB")
        return True
    except Exception as e:
        print(f"  失败: {e}")
        return False

def generate_all_pvz_images():
    tasks = []

    sunflower_prompts = {
        "main": "Sunflower from Plants vs Zombies game, cartoon character, bright yellow flower with green stem and leaves, cute smiling face, game art style, high quality, detailed, transparent background, isolated",
        "front": "Front view of Sunflower from Plants vs Zombies, cartoon game character, bright yellow petals, smiling face, green leaves, PvZ game art style, high resolution, detailed, transparent background",
        "side": "Side view profile of Sunflower from Plants vs Zombies, cartoon game character, showing yellow flower head from side, green stem and leaves, PvZ art style, transparent background",
        "top": "Top view of Sunflower from Plants vs Zombies, looking down at the yellow flower head, cartoon game art, green leaves around, PvZ style, transparent background"
    }

    tasks.append({
        "plant": "sunflower",
        "prompts": sunflower_prompts
    })

    peashooter_prompts = {
        "main": "Peashooter from Plants vs Zombies game, cartoon character, green plant with big head, eyes and mouth, pea shooter cannon on top, cute game art style, high quality, detailed, transparent background, isolated",
        "front": "Front view of Peashooter from Plants vs Zombies, cartoon game character, green plant with big eyes and smiling mouth, pea shooter on top, PvZ game art style, high resolution, detailed, transparent background",
        "side": "Side view profile of Peashooter from Plants vs Zombies, cartoon game character, showing the pea shooter cannon from side, green plant body, PvZ art style, transparent background",
        "top": "Top view of Peashooter from Plants vs Zombies, looking down at the green plant head with pea shooter cannon, cartoon game art, PvZ style, transparent background"
    }

    tasks.append({
        "plant": "peashooter",
        "prompts": peashooter_prompts
    })

    wallnut_prompts = {
        "main": "Wall-nut from Plants vs Zombies game, cartoon character, brown walnut with tough expression, hard shell texture, cute defensive plant, game art style, high quality, detailed, transparent background, isolated",
        "front": "Front view of Wall-nut from Plants vs Zombies, cartoon game character, brown walnut shell with eyes and tough expression, detailed shell texture, PvZ game art style, high resolution, transparent background",
        "side": "Side view profile of Wall-nut from Plants vs Zombies, cartoon game character, showing the brown walnut shell from side, tough expression, PvZ art style, transparent background",
        "top": "Top view of Wall-nut from Plants vs Zombies, looking down at the brown walnut shell top, cartoon game art, PvZ style, transparent background"
    }

    tasks.append({
        "plant": "wallnut",
        "prompts": wallnut_prompts
    })

    success_count = 0
    total_count = 0

    print("=" * 60)
    print("开始生成植物大战僵尸游戏风格图片")
    print("=" * 60)
    print()

    for task in tasks:
        plant_name = task["plant"]
        plant_dir = os.path.join(PLANTS_DIR, plant_name)
        os.makedirs(plant_dir, exist_ok=True)

        for view, prompt in task["prompts"].items():
            total_count += 1
            if view == "main":
                save_path = os.path.join(IMAGES_DIR, f"{plant_name}.png")
            else:
                save_path = os.path.join(plant_dir, f"{view}_{plant_name}.png")

            if download_image(prompt, save_path, "square_hd"):
                success_count += 1
            time.sleep(2)
        print()

    print(f"\n===== 主图片生成完成: {success_count}/{total_count} =====")
    print()

    print("=" * 60)
    print("开始生成预览图片")
    print("=" * 60)
    print()

    preview_styles = [
        ("style1_pvz_classic", "Plants vs Zombies classic game art style"),
        ("style2_chibi", "cute chibi anime style, Plants vs Zombies characters"),
        ("style3_realistic_cartoon", "realistic cartoon style, Plants vs Zombies characters")
    ]

    preview_plants = [
        ("sunflower", "Sunflower from Plants vs Zombies, yellow flower with smiling face"),
        ("peashooter", "Peashooter from Plants vs Zombies, green plant with pea shooter"),
        ("wallnut", "Wall-nut from Plants vs Zombies, brown walnut with tough expression")
    ]

    preview_success = 0
    preview_total = 0

    for style_dir, style_desc in preview_styles:
        style_path = os.path.join(PREVIEW_DIR, style_dir)
        os.makedirs(style_path, exist_ok=True)
        
        for plant_name, plant_desc in preview_plants:
            preview_total += 1
            save_path = os.path.join(style_path, f"{plant_name}.png")
            prompt = f"{plant_desc}, {style_desc}, high quality, detailed, transparent background, square composition"
            
            if download_image(prompt, save_path, "square_hd"):
                preview_success += 1
            time.sleep(2)
        print()

    print(f"\n===== 预览图片生成完成: {preview_success}/{preview_total} =====")
    print(f"\n===== 总计: {success_count + preview_success}/{total_count + preview_total} =====")

if __name__ == "__main__":
    generate_all_pvz_images()
