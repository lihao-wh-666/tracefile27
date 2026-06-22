import os
from PIL import Image, ImageDraw, ImageFilter
import math
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "assets", "images")
PLANTS_DIR = os.path.join(IMAGES_DIR, "plants")
PREVIEW_DIR = os.path.join(IMAGES_DIR, "plants_preview")

def add_shadow(img, center_x, center_y, radius):
    """添加柔和阴影"""
    shadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow)
    for i in range(5):
        alpha = 30 - i * 5
        offset = i * 8
        draw.ellipse([center_x - radius - offset, center_y - radius//2 - offset,
                     center_x + radius + offset, center_y + radius//2 + offset],
                    fill=(0, 0, 0, alpha))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=10))
    return Image.alpha_composite(shadow, img)

def create_sunflower(size=(1832, 1832), view='front'):
    """创建向日葵角色"""
    img = Image.new('RGBA', size, (255, 255, 255, 0))
    center_x, center_y = size[0] // 2, size[1] // 2
    
    if view == 'front':
        head_radius = 500
        petal_count = 16
        petal_length = 320
        petal_width = 110
    elif view == 'side':
        head_radius = 450
        center_x -= 100
        petal_count = 10
        petal_length = 280
        petal_width = 100
    else:  # top
        head_radius = 450
        petal_count = 20
        petal_length = 300
        petal_width = 100
    
    if view == 'top':
        for i in range(petal_count):
            angle = (i * 360 / petal_count) * math.pi / 180
            px = center_x + math.cos(angle) * (head_radius + petal_length // 2 - 50)
            py = center_y + math.sin(angle) * (head_radius + petal_length // 2 - 50)
            
            petal_img = Image.new('RGBA', size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(petal_img)
            color = (255, 200 + random.randint(0, 30), 0, 255)
            draw.ellipse([px - petal_width//2, py - petal_length//2, 
                         px + petal_width//2, py + petal_length//2], 
                        fill=color)
            petal_img = petal_img.rotate(i * 360 / petal_count, center=(center_x, center_y))
            img = Image.alpha_composite(img, petal_img)
        
        draw = ImageDraw.Draw(img)
        draw.ellipse([center_x - head_radius, center_y - head_radius,
                     center_x + head_radius, center_y + head_radius],
                    fill=(120, 60, 15, 255))
        
        for i in range(30):
            rx = center_x + random.randint(-head_radius + 50, head_radius - 50)
            ry = center_y + random.randint(-head_radius + 50, head_radius - 50)
            seed_size = random.randint(20, 40)
            draw.ellipse([rx - seed_size, ry - seed_size,
                         rx + seed_size, ry + seed_size],
                        fill=(60, 30, 10, 255))
    else:
        for i in range(petal_count):
            angle = (i * 360 / petal_count) * math.pi / 180
            px = center_x + math.cos(angle) * (head_radius + petal_length // 2 - 80)
            py = center_y + math.sin(angle) * (head_radius + petal_length // 2 - 80)
            
            if view == 'side' and (math.cos(angle) < -0.3):
                continue
            
            petal_img = Image.new('RGBA', size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(petal_img)
            brightness = 200 + random.randint(0, 55)
            color = (255, brightness, 0, 255)
            draw.ellipse([px - petal_width//2, py - petal_length//2, 
                         px + petal_width//2, py + petal_length//2], 
                        fill=color)
            petal_img = petal_img.rotate(i * 360 / petal_count, center=(center_x, center_y))
            img = Image.alpha_composite(img, petal_img)
        
        img = add_shadow(img, center_x, center_y, head_radius)
        draw = ImageDraw.Draw(img)
        
        draw.ellipse([center_x - head_radius, center_y - head_radius,
                     center_x + head_radius, center_y + head_radius],
                    fill=(139, 69, 19, 255))
        
        if view == 'front':
            eye_radius = 70
            eye_y = center_y - 80
            eye_offset = 180
            
            draw.ellipse([center_x - eye_offset - eye_radius, eye_y - eye_radius,
                         center_x - eye_offset + eye_radius, eye_y + eye_radius],
                        fill=(255, 255, 255, 255))
            draw.ellipse([center_x + eye_offset - eye_radius, eye_y - eye_radius,
                         center_x + eye_offset + eye_radius, eye_y + eye_radius],
                        fill=(255, 255, 255, 255))
            
            pupil_radius = 35
            draw.ellipse([center_x - eye_offset - pupil_radius + 15, eye_y - pupil_radius + 15,
                         center_x - eye_offset + pupil_radius + 15, eye_y + pupil_radius + 15],
                        fill=(0, 0, 0, 255))
            draw.ellipse([center_x + eye_offset - pupil_radius + 15, eye_y - pupil_radius + 15,
                         center_x + eye_offset + pupil_radius + 15, eye_y + pupil_radius + 15],
                        fill=(0, 0, 0, 255))
            
            highlight_radius = 12
            draw.ellipse([center_x - eye_offset - highlight_radius + 5, eye_y - highlight_radius + 5,
                         center_x - eye_offset + highlight_radius + 5, eye_y + highlight_radius + 5],
                        fill=(255, 255, 255, 255))
            draw.ellipse([center_x + eye_offset - highlight_radius + 5, eye_y - highlight_radius + 5,
                         center_x + eye_offset + highlight_radius + 5, eye_y + highlight_radius + 5],
                        fill=(255, 255, 255, 255))
            
            draw.arc([center_x - 150, center_y + 20, 
                     center_x + 150, center_y + 250],
                    start=20, end=160, fill=(40, 20, 0, 255), width=18)
            
            cheek_radius = 45
            draw.ellipse([center_x - eye_offset - 80 - cheek_radius, center_y + 50 - cheek_radius,
                         center_x - eye_offset - 80 + cheek_radius, center_y + 50 + cheek_radius],
                        fill=(255, 150, 150, 100))
            draw.ellipse([center_x + eye_offset + 80 - cheek_radius, center_y + 50 - cheek_radius,
                         center_x + eye_offset + 80 + cheek_radius, center_y + 50 + cheek_radius],
                        fill=(255, 150, 150, 100))
        
        elif view == 'side':
            eye_radius = 60
            eye_y = center_y - 80
            eye_x = center_x + 80
            
            draw.ellipse([eye_x - eye_radius, eye_y - eye_radius,
                         eye_x + eye_radius, eye_y + eye_radius],
                        fill=(255, 255, 255, 255))
            
            pupil_radius = 30
            draw.ellipse([eye_x - pupil_radius + 20, eye_y - pupil_radius + 10,
                         eye_x + pupil_radius + 20, eye_y + pupil_radius + 10],
                        fill=(0, 0, 0, 255))
            
            draw.arc([center_x - 50, center_y + 50, 
                     center_x + 150, center_y + 200],
                    start=0, end=180, fill=(40, 20, 0, 255), width=15)
        
        stem_start_y = center_y + head_radius
        stem_height = 200
        stem_width = 80
        draw.rectangle([center_x - stem_width//2, stem_start_y,
                       center_x + stem_width//2, stem_start_y + stem_height],
                      fill=(34, 139, 34, 255))
        
        leaf_y = stem_start_y + 50
        leaf_width = 150
        leaf_height = 80
        draw.ellipse([center_x - stem_width//2 - leaf_width, leaf_y - leaf_height//2,
                     center_x - stem_width//2, leaf_y + leaf_height//2],
                    fill=(50, 180, 50, 255))
        draw.ellipse([center_x + stem_width//2, leaf_y - leaf_height//2,
                     center_x + stem_width//2 + leaf_width, leaf_y + leaf_height//2],
                    fill=(50, 180, 50, 255))
    
    return img

def create_peashooter(size=(1832, 1832), view='front'):
    """创建豌豆射手角色"""
    img = Image.new('RGBA', size, (255, 255, 255, 0))
    center_x, center_y = size[0] // 2, size[1] // 2
    
    if view == 'front':
        head_radius = 520
    elif view == 'side':
        head_radius = 480
        center_x -= 150
    else:  # top
        head_radius = 450
    
    if view == 'top':
        draw = ImageDraw.Draw(img)
        draw.ellipse([center_x - head_radius, center_y - head_radius,
                     center_x + head_radius, center_y + head_radius],
                    fill=(34, 139, 34, 255))
        
        cannon_width = 200
        cannon_height = 150
        cannon_x = center_x 
        cannon_y = center_y - head_radius + 50
        draw.ellipse([cannon_x - cannon_width//2, cannon_y - cannon_height//2,
                     cannon_x + cannon_width//2, cannon_y + cannon_height//2],
                    fill=(50, 205, 50, 255))
        draw.ellipse([cannon_x - 60, cannon_y - cannon_height//2 - 20,
                     cannon_x + 60, cannon_y - cannon_height//2 + 20],
                    fill=(0, 100, 0, 255))
    else:
        img = add_shadow(img, center_x, center_y + 50, head_radius)
        draw = ImageDraw.Draw(img)
        
        draw.ellipse([center_x - head_radius, center_y - head_radius,
                     center_x + head_radius, center_y + head_radius],
                    fill=(34, 139, 34, 255))
        
        if view == 'front':
            cannon_width = 280
            cannon_height = 180
            cannon_x = center_x + head_radius - 50
            cannon_y = center_y - 20
            
            draw.ellipse([cannon_x - cannon_width//2, cannon_y - cannon_height//2,
                         cannon_x + cannon_width//2, cannon_y + cannon_height//2],
                        fill=(50, 205, 50, 255))
            
            inner_cannon_width = 120
            inner_cannon_height = 100
            draw.ellipse([cannon_x + cannon_width//2 - inner_cannon_width, 
                         cannon_y - inner_cannon_height//2,
                         cannon_x + cannon_width//2 + 20, 
                         cannon_y + inner_cannon_height//2],
                        fill=(0, 80, 0, 255))
            
            draw.ellipse([cannon_x + cannon_width//2 - inner_cannon_width + 20,
                         cannon_y - inner_cannon_height//2 + 20,
                         cannon_x + cannon_width//2 - 20,
                         cannon_y + inner_cannon_height//2 - 20],
                        fill=(0, 50, 0, 255))
            
            eye_radius = 80
            eye_y = center_y - 130
            eye_offset = 150
            
            draw.ellipse([center_x - eye_offset - eye_radius, eye_y - eye_radius,
                         center_x - eye_offset + eye_radius, eye_y + eye_radius],
                        fill=(255, 255, 255, 255))
            draw.ellipse([center_x + eye_offset - eye_radius, eye_y - eye_radius,
                         center_x + eye_offset + eye_radius, eye_y + eye_radius],
                        fill=(255, 255, 255, 255))
            
            pupil_radius = 40
            draw.ellipse([center_x - eye_offset - pupil_radius + 25, eye_y - pupil_radius + 20,
                         center_x - eye_offset + pupil_radius + 25, eye_y + pupil_radius + 20],
                        fill=(0, 0, 0, 255))
            draw.ellipse([center_x + eye_offset - pupil_radius + 25, eye_y - pupil_radius + 20,
                         center_x + eye_offset + pupil_radius + 25, eye_y + pupil_radius + 20],
                        fill=(0, 0, 0, 255))
            
            highlight_radius = 15
            draw.ellipse([center_x - eye_offset - highlight_radius + 15, eye_y - highlight_radius + 10,
                         center_x - eye_offset + highlight_radius + 15, eye_y + highlight_radius + 10],
                        fill=(255, 255, 255, 255))
            draw.ellipse([center_x + eye_offset - highlight_radius + 15, eye_y - highlight_radius + 10,
                         center_x + eye_offset + highlight_radius + 15, eye_y + highlight_radius + 10],
                        fill=(255, 255, 255, 255))
            
            draw.ellipse([center_x - 120, center_y + 80,
                         center_x + 80, center_y + 220],
                        fill=(0, 60, 0, 255))
            
            tongue_width = 60
            tongue_height = 40
            draw.ellipse([center_x - 80, center_y + 120,
                         center_x - 80 + tongue_width, center_y + 120 + tongue_height],
                        fill=(200, 50, 50, 255))
            
            cheek_radius = 40
            draw.ellipse([center_x - eye_offset - 60 - cheek_radius, center_y + 20 - cheek_radius,
                         center_x - eye_offset - 60 + cheek_radius, center_y + 20 + cheek_radius],
                        fill=(100, 200, 100, 80))
            draw.ellipse([center_x + eye_offset + 60 - cheek_radius, center_y + 20 - cheek_radius,
                         center_x + eye_offset + 60 + cheek_radius, center_y + 20 + cheek_radius],
                        fill=(100, 200, 100, 80))
        
        elif view == 'side':
            cannon_width = 350
            cannon_height = 160
            cannon_x = center_x + head_radius + 50
            cannon_y = center_y
            
            draw.ellipse([cannon_x - cannon_width//2, cannon_y - cannon_height//2,
                         cannon_x + cannon_width//2, cannon_y + cannon_height//2],
                        fill=(50, 205, 50, 255))
            
            draw.ellipse([cannon_x + cannon_width//2 - 100, cannon_y - cannon_height//2 - 10,
                         cannon_x + cannon_width//2 + 20, cannon_y + cannon_height//2 + 10],
                        fill=(0, 80, 0, 255))
            
            eye_radius = 70
            eye_y = center_y - 120
            eye_x = center_x + 150
            
            draw.ellipse([eye_x - eye_radius, eye_y - eye_radius,
                         eye_x + eye_radius, eye_y + eye_radius],
                        fill=(255, 255, 255, 255))
            
            pupil_radius = 35
            draw.ellipse([eye_x - pupil_radius + 30, eye_y - pupil_radius + 15,
                         eye_x + pupil_radius + 30, eye_y + pupil_radius + 15],
                        fill=(0, 0, 0, 255))
            
            draw.ellipse([center_x - 50, center_y + 80,
                         center_x + 100, center_y + 200],
                        fill=(0, 60, 0, 255))
        
        stem_width = 100
        stem_height = 150
        stem_start_y = center_y + head_radius
        draw.rectangle([center_x - stem_width//2, stem_start_y,
                       center_x + stem_width//2, stem_start_y + stem_height],
                      fill=(25, 100, 25, 255))
        
        leaf_width = 180
        leaf_height = 90
        leaf_y = stem_start_y + 30
        draw.ellipse([center_x - stem_width//2 - leaf_width, leaf_y - leaf_height//2,
                     center_x - stem_width//2, leaf_y + leaf_height//2],
                    fill=(45, 160, 45, 255))
        draw.ellipse([center_x + stem_width//2, leaf_y - leaf_height//2,
                     center_x + stem_width//2 + leaf_width, leaf_y + leaf_height//2],
                    fill=(45, 160, 45, 255))
    
    return img

def create_wallnut(size=(1832, 1832), view='front'):
    """创建坚果墙角色"""
    img = Image.new('RGBA', size, (255, 255, 255, 0))
    center_x, center_y = size[0] // 2, size[1] // 2
    
    if view == 'front':
        width = 900
        height = 850
    elif view == 'side':
        width = 700
        height = 850
        center_x -= 100
    else:  # top
        width = 800
        height = 600
    
    if view == 'top':
        draw = ImageDraw.Draw(img)
        
        draw.ellipse([center_x - width//2, center_y - height//2,
                     center_x + width//2, center_y + height//2],
                    fill=(139, 90, 43, 255))
        
        for i in range(40):
            rx = center_x + random.randint(-width//2 + 50, width//2 - 50)
            ry = center_y + random.randint(-height//2 + 50, height//2 - 50)
            spot_size = random.randint(30, 80)
            color_variation = random.randint(-30, 30)
            draw.ellipse([rx - spot_size, ry - spot_size,
                         rx + spot_size, ry + spot_size],
                        fill=(101 + color_variation, 67 + color_variation, 33 + color_variation, 255))
        
        draw.ellipse([center_x - width//2, center_y - height//2,
                     center_x + width//2, center_y + height//2],
                    outline=(70, 40, 10, 255), width=25)
        
        draw.ellipse([center_x - 80, center_y - 30,
                     center_x + 80, center_y + 30],
                    fill=(70, 40, 10, 255))
    else:
        img = add_shadow(img, center_x, center_y + 50, width//2)
        draw = ImageDraw.Draw(img)
        
        draw.ellipse([center_x - width//2, center_y - height//2,
                     center_x + width//2, center_y + height//2],
                    fill=(139, 90, 43, 255))
        
        for i in range(50):
            rx = center_x + random.randint(-width//2 + 80, width//2 - 80)
            ry = center_y + random.randint(-height//2 + 80, height//2 - 80)
            spot_size = random.randint(25, 70)
            color_variation = random.randint(-40, 40)
            r = max(0, min(255, 101 + color_variation))
            g = max(0, min(255, 67 + color_variation))
            b = max(0, min(255, 33 + color_variation))
            draw.ellipse([rx - spot_size, ry - spot_size,
                         rx + spot_size, ry + spot_size],
                        fill=(r, g, b, 255))
        
        draw.ellipse([center_x - width//2, center_y - height//2,
                     center_x + width//2, center_y + height//2],
                    outline=(70, 40, 10, 255), width=30)
        
        if view == 'front':
            eye_radius = 65
            eye_y = center_y - 100
            eye_offset = 200
            
            draw.ellipse([center_x - eye_offset - eye_radius, eye_y - eye_radius,
                         center_x - eye_offset + eye_radius, eye_y + eye_radius],
                        fill=(255, 255, 255, 255))
            draw.ellipse([center_x + eye_offset - eye_radius, eye_y - eye_radius,
                         center_x + eye_offset + eye_radius, eye_y + eye_radius],
                        fill=(255, 255, 255, 255))
            
            pupil_radius = 32
            draw.ellipse([center_x - eye_offset - pupil_radius, eye_y - pupil_radius,
                         center_x - eye_offset + pupil_radius, eye_y + pupil_radius],
                        fill=(0, 0, 0, 255))
            draw.ellipse([center_x + eye_offset - pupil_radius, eye_y - pupil_radius,
                         center_x + eye_offset + pupil_radius, eye_y + pupil_radius],
                        fill=(0, 0, 0, 255))
            
            highlight_radius = 12
            draw.ellipse([center_x - eye_offset - highlight_radius - 15, eye_y - highlight_radius - 15,
                         center_x - eye_offset + highlight_radius - 15, eye_y + highlight_radius - 15],
                        fill=(255, 255, 255, 255))
            draw.ellipse([center_x + eye_offset - highlight_radius - 15, eye_y - highlight_radius - 15,
                         center_x + eye_offset + highlight_radius - 15, eye_y + highlight_radius - 15],
                        fill=(255, 255, 255, 255))
            
            brow_width = 120
            brow_height = 25
            draw.rectangle([center_x - eye_offset - brow_width//2, eye_y - eye_radius - 60,
                           center_x - eye_offset + brow_width//2, eye_y - eye_radius - 60 + brow_height],
                          fill=(60, 30, 10, 255))
            draw.rectangle([center_x + eye_offset - brow_width//2, eye_y - eye_radius - 60,
                           center_x + eye_offset + brow_width//2, eye_y - eye_radius - 60 + brow_height],
                          fill=(60, 30, 10, 255))
            
            draw.line([center_x - 180, center_y + 120, center_x + 180, center_y + 120],
                     fill=(40, 20, 5, 255), width=25)
            
            crack_y = center_y + 50
            draw.line([center_x - 50, crack_y - 30, center_x - 20, crack_y + 20,
                      center_x + 30, crack_y - 10, center_x + 60, crack_y + 30],
                     fill=(60, 30, 10, 255), width=8)
        
        elif view == 'side':
            eye_radius = 55
            eye_y = center_y - 100
            eye_x = center_x + 100
            
            draw.ellipse([eye_x - eye_radius, eye_y - eye_radius,
                         eye_x + eye_radius, eye_y + eye_radius],
                        fill=(255, 255, 255, 255))
            
            pupil_radius = 28
            draw.ellipse([eye_x - pupil_radius + 15, eye_y - pupil_radius,
                         eye_x + pupil_radius + 15, eye_y + pupil_radius],
                        fill=(0, 0, 0, 255))
            
            brow_width = 100
            brow_height = 20
            draw.rectangle([eye_x - brow_width//2, eye_y - eye_radius - 50,
                           eye_x + brow_width//2, eye_y - eye_radius - 50 + brow_height],
                          fill=(60, 30, 10, 255))
            
            draw.line([eye_x - 80, center_y + 120, eye_x + 80, center_y + 120],
                     fill=(40, 20, 5, 255), width=20)
    
    return img

def create_styled_character(plant_type, style='classic', size=(1832, 1832)):
    """创建不同风格的角色预览图"""
    if style == 'style1_pvz_classic':
        if plant_type == 'sunflower':
            return create_sunflower(size, 'front')
        elif plant_type == 'peashooter':
            return create_peashooter(size, 'front')
        else:
            return create_wallnut(size, 'front')
    
    elif style == 'style2_chibi':
        img = Image.new('RGBA', size, (255, 255, 255, 0))
        center_x, center_y = size[0] // 2, size[1] // 2
        draw = ImageDraw.Draw(img)
        
        if plant_type == 'sunflower':
            head_radius = 600
            for i in range(12):
                angle = (i * 30) * math.pi / 180
                px = center_x + math.cos(angle) * (head_radius + 200)
                py = center_y + math.sin(angle) * (head_radius + 200)
                draw.ellipse([px - 80, py - 150, px + 80, py + 150],
                            fill=(255, 220, 0, 255))
            
            draw.ellipse([center_x - head_radius, center_y - head_radius,
                         center_x + head_radius, center_y + head_radius],
                        fill=(139, 69, 19, 255))
            
            eye_radius = 100
            draw.ellipse([center_x - 200 - eye_radius, center_y - 50 - eye_radius,
                         center_x - 200 + eye_radius, center_y - 50 + eye_radius],
                        fill=(255, 255, 255, 255))
            draw.ellipse([center_x + 200 - eye_radius, center_y - 50 - eye_radius,
                         center_x + 200 + eye_radius, center_y - 50 + eye_radius],
                        fill=(255, 255, 255, 255))
            
            pupil_radius = 50
            draw.ellipse([center_x - 200 - pupil_radius + 20, center_y - 50 - pupil_radius + 30,
                         center_x - 200 + pupil_radius + 20, center_y - 50 + pupil_radius + 30],
                        fill=(0, 0, 0, 255))
            draw.ellipse([center_x + 200 - pupil_radius + 20, center_y - 50 - pupil_radius + 30,
                         center_x + 200 + pupil_radius + 20, center_y - 50 + pupil_radius + 30],
                        fill=(0, 0, 0, 255))
            
            draw.arc([center_x - 150, center_y + 100, center_x + 150, center_y + 300],
                    start=0, end=180, fill=(0, 0, 0, 255), width=20)
        
        elif plant_type == 'peashooter':
            head_radius = 550
            draw.ellipse([center_x - head_radius, center_y - head_radius,
                         center_x + head_radius, center_y + head_radius],
                        fill=(34, 139, 34, 255))
            
            draw.ellipse([center_x + 200, center_y - 100,
                         center_x + 550, center_y + 100],
                        fill=(50, 205, 50, 255))
            
            eye_radius = 90
            draw.ellipse([center_x - 180 - eye_radius, center_y - 100 - eye_radius,
                         center_x - 180 + eye_radius, center_y - 100 + eye_radius],
                        fill=(255, 255, 255, 255))
            draw.ellipse([center_x + 80 - eye_radius, center_y - 100 - eye_radius,
                         center_x + 80 + eye_radius, center_y - 100 + eye_radius],
                        fill=(255, 255, 255, 255))
            
            pupil_radius = 45
            draw.ellipse([center_x - 180 - pupil_radius + 30, center_y - 100 - pupil_radius + 20,
                         center_x - 180 + pupil_radius + 30, center_y - 100 + pupil_radius + 20],
                        fill=(0, 0, 0, 255))
            draw.ellipse([center_x + 80 - pupil_radius + 30, center_y - 100 - pupil_radius + 20,
                         center_x + 80 + pupil_radius + 30, center_y - 100 + pupil_radius + 20],
                        fill=(0, 0, 0, 255))
            
            draw.ellipse([center_x - 100, center_y + 100,
                         center_x + 100, center_y + 250],
                        fill=(0, 60, 0, 255))
        
        else:  # wallnut
            draw.ellipse([center_x - 450, center_y - 450,
                         center_x + 450, center_y + 450],
                        fill=(139, 90, 43, 255))
            
            for i in range(30):
                rx = center_x + random.randint(-350, 350)
                ry = center_y + random.randint(-350, 350)
                s = random.randint(30, 60)
                draw.ellipse([rx - s, ry - s, rx + s, ry + s],
                            fill=(101, 67, 33, 255))
            
            eye_radius = 80
            draw.ellipse([center_x - 200 - eye_radius, center_y - 80 - eye_radius,
                         center_x - 200 + eye_radius, center_y - 80 + eye_radius],
                        fill=(255, 255, 255, 255))
            draw.ellipse([center_x + 200 - eye_radius, center_y - 80 - eye_radius,
                         center_x + 200 + eye_radius, center_y - 80 + eye_radius],
                        fill=(255, 255, 255, 255))
            
            pupil_radius = 40
            draw.ellipse([center_x - 200 - pupil_radius, center_y - 80 - pupil_radius,
                         center_x - 200 + pupil_radius, center_y - 80 + pupil_radius],
                        fill=(0, 0, 0, 255))
            draw.ellipse([center_x + 200 - pupil_radius, center_y - 80 - pupil_radius,
                         center_x + 200 + pupil_radius, center_y - 80 + pupil_radius],
                        fill=(0, 0, 0, 255))
            
            draw.line([center_x - 180, center_y + 150, center_x + 180, center_y + 150],
                     fill=(40, 20, 5, 255), width=25)
        
        return img
    
    else:  # style3_realistic_cartoon
        img = Image.new('RGBA', size, (255, 255, 255, 0))
        center_x, center_y = size[0] // 2, size[1] // 2
        draw = ImageDraw.Draw(img)
        
        if plant_type == 'sunflower':
            head_radius = 480
            for i in range(14):
                angle = (i * 360 / 14) * math.pi / 180
                px = center_x + math.cos(angle) * (head_radius + 250)
                py = center_y + math.sin(angle) * (head_radius + 250)
                
                petal_color = (255, 200 + random.randint(0, 50), random.randint(0, 50), 255)
                draw.ellipse([px - 70, py - 130, px + 70, py + 130],
                            fill=petal_color)
            
            draw.ellipse([center_x - head_radius, center_y - head_radius,
                         center_x + head_radius, center_y + head_radius],
                        fill=(120, 60, 15, 255))
            
            for i in range(25):
                rx = center_x + random.randint(-head_radius + 50, head_radius - 50)
                ry = center_y + random.randint(-head_radius + 50, head_radius - 50)
                s = random.randint(20, 40)
                draw.ellipse([rx - s, ry - s, rx + s, ry + s],
                            fill=(60, 30, 10, 255))
            
            eye_radius = 70
            draw.ellipse([center_x - 180 - eye_radius, center_y - 80 - eye_radius,
                         center_x - 180 + eye_radius, center_y - 80 + eye_radius],
                        fill=(255, 255, 255, 255))
            draw.ellipse([center_x + 180 - eye_radius, center_y - 80 - eye_radius,
                         center_x + 180 + eye_radius, center_y - 80 + eye_radius],
                        fill=(255, 255, 255, 255))
            
            pupil_radius = 35
            draw.ellipse([center_x - 180 - pupil_radius + 15, center_y - 80 - pupil_radius + 20,
                         center_x - 180 + pupil_radius + 15, center_y - 80 + pupil_radius + 20],
                        fill=(0, 0, 0, 255))
            draw.ellipse([center_x + 180 - pupil_radius + 15, center_y - 80 - pupil_radius + 20,
                         center_x + 180 + pupil_radius + 15, center_y - 80 + pupil_radius + 20],
                        fill=(0, 0, 0, 255))
            
            draw.arc([center_x - 120, center_y + 50, center_x + 120, center_y + 220],
                    start=10, end=170, fill=(30, 15, 0, 255), width=18)
        
        elif plant_type == 'peashooter':
            head_radius = 450
            draw.ellipse([center_x - head_radius, center_y - head_radius,
                         center_x + head_radius, center_y + head_radius],
                        fill=(40, 150, 40, 255))
            
            draw.ellipse([center_x + 250, center_y - 80,
                         center_x + 550, center_y + 80],
                        fill=(60, 180, 60, 255))
            draw.ellipse([center_x + 430, center_y - 50,
                         center_x + 570, center_y + 50],
                        fill=(20, 80, 20, 255))
            
            eye_radius = 65
            draw.ellipse([center_x - 160 - eye_radius, center_y - 120 - eye_radius,
                         center_x - 160 + eye_radius, center_y - 120 + eye_radius],
                        fill=(255, 255, 255, 255))
            draw.ellipse([center_x + 60 - eye_radius, center_y - 120 - eye_radius,
                         center_x + 60 + eye_radius, center_y - 120 + eye_radius],
                        fill=(255, 255, 255, 255))
            
            pupil_radius = 32
            draw.ellipse([center_x - 160 - pupil_radius + 25, center_y - 120 - pupil_radius + 15,
                         center_x - 160 + pupil_radius + 25, center_y - 120 + pupil_radius + 15],
                        fill=(0, 0, 0, 255))
            draw.ellipse([center_x + 60 - pupil_radius + 25, center_y - 120 - pupil_radius + 15,
                         center_x + 60 + pupil_radius + 25, center_y - 120 + pupil_radius + 15],
                        fill=(0, 0, 0, 255))
            
            draw.ellipse([center_x - 80, center_y + 80,
                         center_x + 80, center_y + 200],
                        fill=(0, 50, 0, 255))
        
        else:  # wallnut
            draw.ellipse([center_x - 400, center_y - 380,
                         center_x + 400, center_y + 380],
                        fill=(150, 100, 50, 255))
            
            for i in range(40):
                rx = center_x + random.randint(-320, 320)
                ry = center_y + random.randint(-300, 300)
                s = random.randint(25, 55)
                var = random.randint(-30, 30)
                draw.ellipse([rx - s, ry - s, rx + s, ry + s],
                            fill=(110 + var, 75 + var, 40 + var, 255))
            
            draw.ellipse([center_x - 400, center_y - 380,
                         center_x + 400, center_y + 380],
                        outline=(80, 50, 20, 255), width=25)
            
            eye_radius = 60
            draw.ellipse([center_x - 170 - eye_radius, center_y - 70 - eye_radius,
                         center_x - 170 + eye_radius, center_y - 70 + eye_radius],
                        fill=(255, 255, 255, 255))
            draw.ellipse([center_x + 170 - eye_radius, center_y - 70 - eye_radius,
                         center_x + 170 + eye_radius, center_y - 70 + eye_radius],
                        fill=(255, 255, 255, 255))
            
            pupil_radius = 30
            draw.ellipse([center_x - 170 - pupil_radius, center_y - 70 - pupil_radius,
                         center_x - 170 + pupil_radius, center_y - 70 + pupil_radius],
                        fill=(0, 0, 0, 255))
            draw.ellipse([center_x + 170 - pupil_radius, center_y - 70 - pupil_radius,
                         center_x + 170 + pupil_radius, center_y - 70 + pupil_radius],
                        fill=(0, 0, 0, 255))
            
            draw.line([center_x - 150, center_y + 100, center_x + 150, center_y + 100],
                     fill=(50, 25, 10, 255), width=22)
        
        return img

def save_image(img, path):
    """保存图片"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, 'PNG')
    size_kb = os.path.getsize(path) / 1024
    print(f"  保存: {os.path.basename(path)} ({size_kb:.1f} KB)")

def create_all_characters():
    print("=" * 60)
    print("创建植物大战僵尸游戏角色图片")
    print("=" * 60)
    print()
    
    plants = [
        ('sunflower', '向日葵', create_sunflower),
        ('peashooter', '豌豆射手', create_peashooter),
        ('wallnut', '坚果墙', create_wallnut)
    ]
    
    views = ['front', 'side', 'top']
    view_names = {'front': '正面', 'side': '侧面', 'top': '顶部'}
    
    success_count = 0
    total_count = 0
    
    for plant_name, plant_cn, create_func in plants:
        plant_dir = os.path.join(PLANTS_DIR, plant_name)
        os.makedirs(plant_dir, exist_ok=True)
        print(f"正在创建 {plant_cn} ({plant_name}):")
        
        main_img = create_func(view='front')
        main_path = os.path.join(IMAGES_DIR, f"{plant_name}.png")
        save_image(main_img, main_path)
        success_count += 1
        total_count += 1
        
        for view in views:
            total_count += 1
            view_name = view_names[view]
            print(f"  [{view_name}] ", end='')
            
            img = create_func(view=view)
            save_path = os.path.join(plant_dir, f"{view}_{plant_name}.png")
            save_image(img, save_path)
            success_count += 1
        print()
    
    print(f"\n===== 主图片完成: {success_count}/{total_count} =====")
    print()
    
    print("=" * 60)
    print("创建预览图片")
    print("=" * 60)
    print()
    
    preview_styles = ['style1_pvz_classic', 'style2_chibi', 'style3_realistic_cartoon']
    style_names = {
        'style1_pvz_classic': '经典游戏风格',
        'style2_chibi': 'Q版萌系风格',
        'style3_realistic_cartoon': '写实卡通风格'
    }
    
    preview_plants = ['sunflower', 'peashooter', 'wallnut']
    preview_plant_names = {'sunflower': '向日葵', 'peashooter': '豌豆射手', 'wallnut': '坚果墙'}
    
    preview_success = 0
    preview_total = 0
    
    for style in preview_styles:
        style_path = os.path.join(PREVIEW_DIR, style)
        os.makedirs(style_path, exist_ok=True)
        print(f"正在创建 {style_names[style]} 预览图:")
        
        for plant_name in preview_plants:
            preview_total += 1
            print(f"  {preview_plant_names[plant_name]}: ", end='')
            
            img = create_styled_character(plant_name, style)
            save_path = os.path.join(style_path, f"{plant_name}.png")
            save_image(img, save_path)
            preview_success += 1
        print()
    
    print(f"\n===== 预览图片完成: {preview_success}/{preview_total} =====")
    print(f"\n===== 总计: {success_count + preview_success}/{total_count + preview_total} =====")
    
    return True

if __name__ == "__main__":
    success = create_all_characters()
    exit(0 if success else 1)
