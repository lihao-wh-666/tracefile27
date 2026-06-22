import urllib.request
import urllib.parse
import os
import time
from PIL import Image
import io
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "assets", "images")
PLANTS_DIR = os.path.join(IMAGES_DIR, "plants")
PREVIEW_DIR = os.path.join(IMAGES_DIR, "plants_preview")

def process_and_save_image(img_data, save_path):
    """处理并保存图片到指定路径"""
    try:
        with Image.open(io.BytesIO(img_data)) as img:
            original_size = img.size
            
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            datas = img.getdata()
            new_data = []
            for item in datas:
                if item[0] > 250 and item[1] > 250 and item[2] > 250:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            img.putdata(new_data)
            
            target_size = (1832, 1832)
            ratio = min(target_size[0] / img.size[0], target_size[1] / img.size[1])
            new_size = (max(1, int(img.size[0] * ratio)), max(1, int(img.size[1] * ratio)))
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
        print(f"  处理图片失败: {e}")
        return False

def download_image(url, save_path, max_retries=3):
    """从URL下载图片"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'image/png,image/jpeg,image/*;q=0.8,*/*;q=0.5',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    for attempt in range(max_retries):
        print(f"  尝试 {attempt + 1}/{max_retries}: 下载 {os.path.basename(save_path)}")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read()
            
            if len(data) < 1000:
                print(f"  文件太小，可能无效")
                if attempt < max_retries - 1:
                    time.sleep(3)
                    continue
            
            if process_and_save_image(data, save_path):
                return True
                
        except Exception as e:
            print(f"  下载失败: {e}")
            if attempt < max_retries - 1:
                time.sleep(3)
    
    return False

def generate_with_text_to_image(prompt, save_path, max_retries=5):
    """使用text_to_image API生成图片"""
    API_URL = "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image"
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"{API_URL}?prompt={encoded_prompt}&image_size=square_hd"
    
    for attempt in range(max_retries):
        print(f"  尝试 {attempt + 1}/{max_retries}: 生成 {os.path.basename(save_path)}")
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            }
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as response:
                data = response.read()
            
            with Image.open(io.BytesIO(data)) as img:
                extrema = img.convert('L').getextrema()
                content_range = extrema[1] - extrema[0]
                
                if content_range < 100:
                    print(f"    图片内容不足（范围:{content_range}），等待后重试...")
                    time.sleep(5 + attempt * 5)
                    continue
            
            if process_and_save_image(data, save_path):
                return True
                
        except Exception as e:
            print(f"  生成失败: {e}")
            if attempt < max_retries - 1:
                time.sleep(5 + attempt * 5)
    
    return False

def create_simple_pvz_character(save_path, character_type):
    """创建简单的植物大战僵尸风格角色图片（备用方案）"""
    print(f"  使用备用方案创建 {os.path.basename(save_path)}")
    
    size = (1832, 1832)
    img = Image.new('RGBA', size, (255, 255, 255, 0))
    
    center_x, center_y = size[0] // 2, size[1] // 2
    head_radius = 600
    
    from PIL import ImageDraw
    
    if character_type == 'sunflower':
        for i in range(12):
            import math
            angle = (i * 30) * math.pi / 180
            petal_length = 350
            petal_width = 120
            
            px = center_x + math.cos(angle) * (head_radius + petal_length // 2)
            py = center_y + math.sin(angle) * (head_radius + petal_length // 2)
            
            petal_img = Image.new('RGBA', size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(petal_img)
            draw.ellipse([px - petal_width//2, py - petal_length//2, 
                         px + petal_width//2, py + petal_length//2], 
                        fill=(255, 215, 0, 255))
            petal_img = petal_img.rotate(i * 30, center=(center_x, center_y))
            img = Image.alpha_composite(img, petal_img)
        
        draw = ImageDraw.Draw(img)
        draw.ellipse([center_x - head_radius, center_y - head_radius,
                     center_x + head_radius, center_y + head_radius],
                    fill=(139, 69, 19, 255))
        
        eye_radius = 80
        eye_y = center_y - 100
        draw.ellipse([center_x - 250 - eye_radius, eye_y - eye_radius,
                     center_x - 250 + eye_radius, eye_y + eye_radius],
                    fill=(255, 255, 255, 255))
        draw.ellipse([center_x + 250 - eye_radius, eye_y - eye_radius,
                     center_x + 250 + eye_radius, eye_y + eye_radius],
                    fill=(255, 255, 255, 255))
        
        pupil_radius = 40
        draw.ellipse([center_x - 250 - pupil_radius, eye_y - pupil_radius + 20,
                     center_x - 250 + pupil_radius, eye_y + pupil_radius + 20],
                    fill=(0, 0, 0, 255))
        draw.ellipse([center_x + 250 - pupil_radius, eye_y - pupil_radius + 20,
                     center_x + 250 + pupil_radius, eye_y + pupil_radius + 20],
                    fill=(0, 0, 0, 255))
        
        draw.arc([center_x - 200, center_y, 
                 center_x + 200, center_y + 300],
                start=0, end=180, fill=(0, 0, 0, 255), width=15)
        
    elif character_type == 'peashooter':
        draw = ImageDraw.Draw(img)
        
        draw.ellipse([center_x - head_radius, center_y - head_radius,
                     center_x + head_radius, center_y + head_radius],
                    fill=(34, 139, 34, 255))
        
        cannon_width = 300
        cannon_height = 200
        cannon_x = center_x + head_radius - 100
        cannon_y = center_y - cannon_height // 2
        draw.ellipse([cannon_x, cannon_y, 
                     cannon_x + cannon_width, cannon_y + cannon_height],
                    fill=(50, 205, 50, 255))
        draw.ellipse([cannon_x + cannon_width - 80, cannon_y + 20,
                     cannon_x + cannon_width + 20, cannon_y + cannon_height - 20],
                    fill=(0, 100, 0, 255))
        
        eye_radius = 90
        eye_y = center_y - 150
        draw.ellipse([center_x - 200 - eye_radius, eye_y - eye_radius,
                     center_x - 200 + eye_radius, eye_y + eye_radius],
                    fill=(255, 255, 255, 255))
        draw.ellipse([center_x + 100 - eye_radius, eye_y - eye_radius,
                     center_x + 100 + eye_radius, eye_y + eye_radius],
                    fill=(255, 255, 255, 255))
        
        pupil_radius = 45
        draw.ellipse([center_x - 200 - pupil_radius + 30, eye_y - pupil_radius + 20,
                     center_x - 200 + pupil_radius + 30, eye_y + pupil_radius + 20],
                    fill=(0, 0, 0, 255))
        draw.ellipse([center_x + 100 - pupil_radius + 30, eye_y - pupil_radius + 20,
                     center_x + 100 + pupil_radius + 30, eye_y + pupil_radius + 20],
                    fill=(0, 0, 0, 255))
        
        draw.ellipse([center_x - 150, center_y + 100,
                     center_x + 100, center_y + 250],
                    fill=(0, 80, 0, 255))
        
    elif character_type == 'wallnut':
        draw = ImageDraw.Draw(img)
        
        for i in range(10):
            import random
            random.seed(i)
            x = center_x + random.randint(-head_radius + 100, head_radius - 100)
            y = center_y + random.randint(-head_radius + 100, head_radius - 100)
            spot_size = random.randint(50, 120)
            draw.ellipse([x - spot_size//2, y - spot_size//2,
                         x + spot_size//2, y + spot_size//2],
                        fill=(101, 67, 33, 255))
        
        draw.ellipse([center_x - head_radius, center_y - head_radius,
                     center_x + head_radius, center_y + head_radius],
                    fill=(139, 90, 43, 255), outline=(80, 50, 20, 255), width=20)
        
        eye_radius = 70
        eye_y = center_y - 120
        draw.ellipse([center_x - 220 - eye_radius, eye_y - eye_radius,
                     center_x - 220 + eye_radius, eye_y + eye_radius],
                    fill=(255, 255, 255, 255))
        draw.ellipse([center_x + 220 - eye_radius, eye_y - eye_radius,
                     center_x + 220 + eye_radius, eye_y + eye_radius],
                    fill=(255, 255, 255, 255))
        
        pupil_radius = 35
        draw.ellipse([center_x - 220 - pupil_radius, eye_y - pupil_radius,
                     center_x - 220 + pupil_radius, eye_y + pupil_radius],
                    fill=(0, 0, 0, 255))
        draw.ellipse([center_x + 220 - pupil_radius, eye_y - pupil_radius,
                     center_x + 220 + pupil_radius, eye_y + pupil_radius],
                    fill=(0, 0, 0, 255))
        
        draw.line([center_x - 200, center_y + 150, center_x + 200, center_y + 150],
                 fill=(60, 30, 10, 255), width=20)
    
    img.save(save_path, 'PNG')
    size_kb = os.path.getsize(save_path) / 1024
    print(f"  备用方案完成! 尺寸: {size}, 文件大小: {size_kb:.1f} KB")
    return True

def download_all_images():
    print("=" * 60)
    print("下载/生成植物大战僵尸游戏图片")
    print("=" * 60)
    print()

    plants = [
        ('sunflower', '向日葵'),
        ('peashooter', '豌豆射手'),
        ('wallnut', '坚果墙')
    ]
    
    views = [None, 'front', 'side', 'top']
    view_names = {'front': '正面', 'side': '侧面', 'top': '顶部', None: '主视图'}
    
    prompts = {
        'sunflower': {
            None: 'Sunflower from Plants vs Zombies game, yellow flower head with smiling face, green stem and leaves, classic PvZ cartoon style, transparent background, high quality',
            'front': 'Sunflower from Plants vs Zombies, front view, smiling face, yellow petals, classic game art, transparent background',
            'side': 'Sunflower from Plants vs Zombies, side view profile, yellow flower, green stem, transparent background',
            'top': 'Sunflower from Plants vs Zombies, top view, looking down at yellow flower head, transparent background'
        },
        'peashooter': {
            None: 'Peashooter from Plants vs Zombies game, green plant character, big head with eyes, pea shooter cannon, classic PvZ cartoon style, transparent background, high quality',
            'front': 'Peashooter from Plants vs Zombies, front view, green plant with pea shooter, big eyes, transparent background',
            'side': 'Peashooter from Plants vs Zombies, side view profile, showing pea shooter cannon, transparent background',
            'top': 'Peashooter from Plants vs Zombies, top view, looking down at green plant head, transparent background'
        },
        'wallnut': {
            None: 'Wall-nut from Plants vs Zombies game, brown walnut character, tough expression, hard shell, classic PvZ cartoon style, transparent background, high quality',
            'front': 'Wall-nut from Plants vs Zombies, front view, brown walnut with eyes, tough expression, transparent background',
            'side': 'Wall-nut from Plants vs Zombies, side view profile, brown walnut shell, transparent background',
            'top': 'Wall-nut from Plants vs Zombies, top view, looking down at walnut shell, transparent background'
        }
    }

    success_count = 0
    total_count = 0

    for plant_name, plant_cn in plants:
        plant_dir = os.path.join(PLANTS_DIR, plant_name)
        os.makedirs(plant_dir, exist_ok=True)
        print(f"正在处理 {plant_cn} ({plant_name}):")

        for view in views:
            total_count += 1
            view_name = view_names.get(view, 'main')
            
            if view is None:
                save_path = os.path.join(IMAGES_DIR, f"{plant_name}.png")
            else:
                save_path = os.path.join(plant_dir, f"{view}_{plant_name}.png")
            
            print(f"  [{view_name}] {os.path.basename(save_path)}")
            
            prompt = prompts[plant_name][view]
            success = generate_with_text_to_image(prompt, save_path, max_retries=3)
            
            if not success:
                print(f"  API生成失败，使用备用方案...")
                success = create_simple_pvz_character(save_path, plant_name)
            
            if success:
                success_count += 1
            time.sleep(2)
        print()

    print(f"\n===== 主图片完成: {success_count}/{total_count} =====")
    print()

    print("=" * 60)
    print("开始处理预览图片")
    print("=" * 60)
    print()

    preview_styles = [
        ('style1_pvz_classic', 'Plants vs Zombies classic game art style'),
        ('style2_chibi', 'cute chibi anime style, big head'),
        ('style3_realistic_cartoon', 'realistic cartoon style, 3D rendered look')
    ]

    preview_plants = [
        ('sunflower', 'Sunflower from Plants vs Zombies, yellow flower with smiling face'),
        ('peashooter', 'Peashooter from Plants vs Zombies, green plant with pea shooter'),
        ('wallnut', 'Wall-nut from Plants vs Zombies, brown walnut with tough expression')
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
            prompt = f"{plant_desc}, {style_desc}, high quality, transparent background"
            
            print(f"  {plant_name}")
            success = generate_with_text_to_image(prompt, save_path, max_retries=3)
            
            if not success:
                print(f"  API生成失败，使用备用方案...")
                success = create_simple_pvz_character(save_path, plant_name)
            
            if success:
                preview_success += 1
            time.sleep(2)
        print()

    print(f"\n===== 预览图片完成: {preview_success}/{preview_total} =====")
    print(f"\n===== 总计: {success_count + preview_success}/{total_count + preview_total} =====")
    
    return success_count + preview_success == total_count + preview_total

if __name__ == "__main__":
    success = download_all_images()
    exit(0 if success else 1)
