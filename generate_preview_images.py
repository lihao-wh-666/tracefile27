import urllib.request
import urllib.parse
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PREVIEW_DIR = os.path.join(BASE_DIR, "assets", "images", "plants_preview")
os.makedirs(PREVIEW_DIR, exist_ok=True)

API_URL = "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image"

def download_image(prompt, save_path, image_size="square_hd"):
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"{API_URL}?prompt={encoded_prompt}&image_size={image_size}"
    print(f"  正在生成: {os.path.basename(save_path)}")
    try:
        urllib.request.urlretrieve(url, save_path)
        size_kb = os.path.getsize(save_path) / 1024
        print(f"    ✓ 完成 ({size_kb:.1f} KB)")
        return True
    except Exception as e:
        print(f"    ✗ 失败: {e}")
        return False

def generate_style_variants():
    print("=" * 60)
    print("正在生成多种风格的植物图片供您选择...")
    print("=" * 60)

    styles = {
        "style1_pvz_classic": {
            "label": "风格1: 经典PvZ卡通风格",
            "desc": "明亮色彩、圆润造型、黑色粗轮廓线",
            "plants": {
                "sunflower": "Plants vs Zombies style sunflower, cartoon game character, bright yellow petals, brown center with cute smiling face, green stem and leaves, bold black outline, vibrant colors, isolated on white background, game art style",
                "peashooter": "Plants vs Zombies style peashooter, cartoon game character, green pea pod plant with head that shoots peas, cute eyes, green leaves, bold black outline, vibrant green colors, isolated on white background, game art style",
                "wallnut": "Plants vs Zombies style wall-nut, cartoon game character, brown walnut with tough shell, cute determined face, thick brown shell texture, bold black outline, warm brown colors, isolated on white background, game art style",
            }
        },
        "style2_chibi": {
            "label": "风格2: Q版萌系风格",
            "desc": "大头小身、可爱表情、柔和色彩",
            "plants": {
                "sunflower": "Chibi style sunflower character, super cute, big head small body, large shiny eyes, happy smiling face, yellow flower with green leaves, soft colors, kawaii, isolated on white background, digital illustration",
                "peashooter": "Chibi style pea shooter plant character, super cute, big head small body, large shiny eyes, green pea plant with little mouth, soft green colors, kawaii, isolated on white background, digital illustration",
                "wallnut": "Chibi style walnut character, super cute, big round head, large shiny eyes, tough but adorable expression, brown walnut shell, soft warm colors, kawaii, isolated on white background, digital illustration",
            }
        },
        "style3_realistic_cartoon": {
            "label": "风格3: 写实卡通风格",
            "desc": "细腻纹理、立体感强、半写实",
            "plants": {
                "sunflower": "Realistic cartoon sunflower plant character, semi-realistic style, detailed yellow petals with texture, 3d rendering, green stem with leaves, soft shading, natural lighting, high quality, isolated on white background",
                "peashooter": "Realistic cartoon pea shooter plant, semi-realistic style, detailed green pea pod head, 3d rendering, realistic plant texture, soft shading, natural lighting, high quality, isolated on white background",
                "wallnut": "Realistic cartoon walnut, semi-realistic style, detailed brown walnut shell texture, 3d rendering, realistic nut surface with grooves, soft shading, natural lighting, high quality, isolated on white background",
            }
        },
    }

    total = sum(len(v["plants"]) for v in styles.values())
    count = 0

    for style_key, style_info in styles.items():
        print(f"\n{style_info['label']}")
        print(f"  {style_info['desc']}")

        style_dir = os.path.join(PREVIEW_DIR, style_key)
        os.makedirs(style_dir, exist_ok=True)

        for plant_name, prompt in style_info["plants"].items():
            count += 1
            save_path = os.path.join(style_dir, f"{plant_name}.png")
            download_image(prompt, save_path)
            time.sleep(1)

    print(f"\n完成! 共生成 {count} 张预览图，保存在 {PREVIEW_DIR}")
    print("请选择您喜欢的风格，我将替换游戏中的图片资源。")

if __name__ == "__main__":
    generate_style_variants()
