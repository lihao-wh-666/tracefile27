import urllib.request
import urllib.parse
import os
import time
from PIL import Image
import io

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "assets", "images")
PLANTS_DIR = os.path.join(IMAGES_DIR, "plants")
PREVIEW_DIR = os.path.join(IMAGES_DIR, "plants_preview")

API_URL = "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image"

def generate_image_with_api(prompt, save_path, image_size="square_hd", max_retries=3, wait_time=10):
    """使用API生成图片，带有重试机制"""
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"{API_URL}?prompt={encoded_prompt}&image_size={image_size}"
    
    for attempt in range(max_retries):
        print(f"  尝试 {attempt + 1}/{max_retries}: 生成 {os.path.basename(save_path)}")
        try:
            urllib.request.urlretrieve(url, save_path)
            
            with Image.open(save_path) as img:
                extrema = img.convert('L').getextrema()
                content_range = extrema[1] - extrema[0]
                
                if content_range < 50:
                    print(f"    图片内容不足，等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                    continue
                
                original_size = img.size
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                target_size = (1832, 1832)
                if img.size != target_size:
                    img = img.resize(target_size, Image.LANCZOS)
                    img.save(save_path, 'PNG')
            
            size_kb = os.path.getsize(save_path) / 1024
            print(f"  完成! 原始尺寸: {original_size}, 调整后: {target_size}, 文件大小: {size_kb:.1f} KB")
            return True
            
        except Exception as e:
            print(f"  失败: {e}")
            if attempt < max_retries - 1:
                print(f"  等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
    
    return False

def download_image_with_retry(url, save_path, max_retries=3):
    """下载图片，带有重试机制"""
    for attempt in range(max_retries):
        print(f"  尝试 {attempt + 1}/{max_retries}: 下载 {os.path.basename(save_path)}")
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'image/png,image/jpeg,image/*;q=0.8',
            }
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read()
            
            with Image.open(io.BytesIO(data)) as img:
                original_size = img.size
                
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                target_size = (1832, 1832)
                ratio = min(target_size[0] / img.size[0], target_size[1] / img.size[1])
                new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                img = img.resize(new_size, Image.LANCZOS)
                
                final_img = Image.new('RGBA', target_size, (255, 255, 255, 0))
                offset = ((target_size[0] - new_size[0]) // 2, 
                         (target_size[1] - new_size[1]) // 2)
                final_img.paste(img, offset, img)
                final_img.save(save_path, 'PNG')
            
            size_kb = os.path.getsize(save_path) / 1024
            print(f"  完成! 原始尺寸: {original_size}, 调整后: {target_size}, 文件大小: {size_kb:.1f} KB")
            return True
            
        except Exception as e:
            print(f"  失败: {e}")
            if attempt < max_retries - 1:
                print(f"  等待 5 秒后重试...")
                time.sleep(5)
    
    return False

def download_all_pvz_images():
    print("=" * 60)
    print("使用图片生成API创建植物大战僵尸游戏图片")
    print("=" * 60)
    print()

    tasks = []

    sunflower_prompts = {
        "main": "Sunflower from Plants vs Zombies, cartoon game character, bright yellow flower head with green stem and leaves, cute smiling face, classic PvZ game art style, high quality, detailed, transparent background, isolated character, full body view",
        "front": "Front view of Sunflower from Plants vs Zombies, classic PvZ game art, bright yellow petals, happy smiling face, green leaves, high quality, transparent background",
        "side": "Side view profile of Sunflower from Plants vs Zombies, classic PvZ game art style, yellow flower head from side angle, green stem, transparent background",
        "top": "Top view of Sunflower from Plants vs Zombies, looking down at yellow flower head, green leaves around, classic PvZ style, transparent background"
    }

    tasks.append({
        "plant": "sunflower",
        "prompts": sunflower_prompts
    })

    peashooter_prompts = {
        "main": "Peashooter from Plants vs Zombies, cartoon game character, green plant with big round head, two eyes, smiling mouth, pea shooter cannon on top, classic PvZ game art style, high quality, detailed, transparent background, isolated character",
        "front": "Front view of Peashooter from Plants vs Zombies, classic PvZ game art, green plant body, big eyes, pea shooter, high quality, transparent background",
        "side": "Side view profile of Peashooter from Plants vs Zombies, classic PvZ game art, showing pea shooter cannon from side, green body, transparent background",
        "top": "Top view of Peashooter from Plants vs Zombies, looking down at green plant head with pea shooter, classic PvZ style, transparent background"
    }

    tasks.append({
        "plant": "peashooter",
        "prompts": peashooter_prompts
    })

    wallnut_prompts = {
        "main": "Wall-nut from Plants vs Zombies, cartoon game character, brown walnut with tough serious expression, hard textured shell, classic PvZ game art style, high quality, detailed, transparent background, isolated character",
        "front": "Front view of Wall-nut from Plants vs Zombies, classic PvZ game art, brown walnut shell, eyes, tough expression, high quality, transparent background",
        "side": "Side view profile of Wall-nut from Plants vs Zombies, classic PvZ game art, showing walnut shell from side, tough expression, transparent background",
        "top": "Top view of Wall-nut from Plants vs Zombies, looking down at brown walnut shell top, classic PvZ style, transparent background"
    }

    tasks.append({
        "plant": "wallnut",
        "prompts": wallnut_prompts
    })

    success_count = 0
    total_count = 0

    for task in tasks:
        plant_name = task["plant"]
        plant_dir = os.path.join(PLANTS_DIR, plant_name)
        os.makedirs(plant_dir, exist_ok=True)
        print(f"正在生成 {plant_name} 图片:")

        for view, prompt in task["prompts"].items():
            total_count += 1
            if view == "main":
                save_path = os.path.join(IMAGES_DIR, f"{plant_name}.png")
            else:
                save_path = os.path.join(plant_dir, f"{view}_{plant_name}.png")

            if generate_image_with_api(prompt, save_path, "square_hd", max_retries=3, wait_time=15):
                success_count += 1
            else:
                print(f"  API生成失败，使用备用方案...")
                backup_prompt = f"{prompt}, simple cartoon style"
                if generate_image_with_api(backup_prompt, save_path, "square_hd", max_retries=2, wait_time=10):
                    success_count += 1
            time.sleep(3)
        print()

    print(f"\n===== 主图片生成完成: {success_count}/{total_count} =====")
    print()

    print("=" * 60)
    print("开始生成预览图片")
    print("=" * 60)
    print()

    preview_styles = [
        ("style1_pvz_classic", "Plants vs Zombies classic game art style, clean and simple"),
        ("style2_chibi", "cute chibi anime style, big head, small body, Plants vs Zombies characters, super deformed"),
        ("style3_realistic_cartoon", "realistic cartoon style, 3D rendered look, Plants vs Zombies characters, detailed shading")
    ]

    preview_plants = [
        ("sunflower", "Sunflower from Plants vs Zombies, yellow flower with smiling happy face, green leaves"),
        ("peashooter", "Peashooter from Plants vs Zombies, green plant with pea shooter cannon on head"),
        ("wallnut", "Wall-nut from Plants vs Zombies, brown walnut with tough serious expression")
    ]

    preview_success = 0
    preview_total = 0

    for style_dir, style_desc in preview_styles:
        style_path = os.path.join(PREVIEW_DIR, style_dir)
        os.makedirs(style_path, exist_ok=True)
        print(f"正在生成 {style_dir} 预览图:")
        
        for plant_name, plant_desc in preview_plants:
            preview_total += 1
            save_path = os.path.join(style_path, f"{plant_name}.png")
            prompt = f"{plant_desc}, {style_desc}, high quality, detailed, transparent background, centered composition"
            
            if generate_image_with_api(prompt, save_path, "square_hd", max_retries=3, wait_time=15):
                preview_success += 1
            time.sleep(3)
        print()

    print(f"\n===== 预览图片生成完成: {preview_success}/{preview_total} =====")
    print(f"\n===== 总计: {success_count + preview_success}/{total_count + preview_total} =====")
    
    return success_count + preview_success == total_count + preview_total

if __name__ == "__main__":
    success = download_all_pvz_images()
    exit(0 if success else 1)
