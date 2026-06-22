import urllib.request
import urllib.parse
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "assets", "images")
PLANTS_DIR = os.path.join(IMAGES_DIR, "plants")

API_URL = "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image"

def download_image(prompt, save_path, image_size="square_hd"):
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"{API_URL}?prompt={encoded_prompt}&image_size={image_size}"
    print(f"正在下载: {save_path}")
    print(f"  URL: {url[:100]}...")
    try:
        urllib.request.urlretrieve(url, save_path)
        size_kb = os.path.getsize(save_path) / 1024
        print(f"  完成! 文件大小: {size_kb:.1f} KB")
        return True
    except Exception as e:
        print(f"  失败: {e}")
        return False

def generate_all_plants():
    tasks = []

    sunflower_prompts = {
        "main": "A vibrant sunflower plant with large yellow flower head and green leaves, cartoon game art style, high quality, detailed, transparent background, isolated on white",
        "front": "Front view of a mature sunflower plant, Helianthus annuus, with bright yellow petals, dark brown center disk, green stem and leaves, high resolution botanical photo, detailed texture, natural lighting, white background",
        "side": "Side view profile of a sunflower plant, Helianthus annuus, showing the curved stem, green leaves arrangement, and side of the flower head, botanical photography, natural colors, high detail, white background",
        "top": "Top view overhead shot of a sunflower, Helianthus annuus, looking down at the yellow radial petals and dark center disk with visible seeds, flat lay botanical image, detailed texture, white background"
    }

    tasks.append({
        "plant": "sunflower",
        "prompts": sunflower_prompts
    })

    peashooter_prompts = {
        "main": "A healthy pea plant with green vine, leaves, and pea pods, cartoon game art style, vibrant green, detailed, transparent background, isolated on white",
        "front": "Front view of a sweet pea plant, Pisum sativum, with green compound leaves, curly tendrils, and small white flowers, botanical photograph, fresh green colors, high detail, natural lighting, white background",
        "side": "Side view of a pea vine plant, Pisum sativum, showing climbing tendrils, leaf arrangement along the stem, and developing pea pods, botanical profile photograph, natural green colors, white background",
        "top": "Top view looking down on a pea plant, Pisum sativum, dense green foliage with leaves and tendrils spreading outward, overhead botanical photograph, detailed leaf texture, white background"
    }

    tasks.append({
        "plant": "peashooter",
        "prompts": peashooter_prompts
    })

    wallnut_prompts = {
        "main": "A pile of whole walnuts with brown rough shells, cartoon game art style, detailed texture, warm brown colors, transparent background, isolated on white",
        "front": "Front view of whole walnuts, Juglans regia, with textured brown hard shells, several walnuts grouped together, botanical product photography, detailed shell texture, warm natural lighting, white background",
        "side": "Side view profile of walnuts, Juglans regia, showing the oval shape and textured brown shell surface, single walnut and group arrangement, botanical photograph, natural brown colors, white background",
        "top": "Top view overhead shot of walnuts, Juglans regia, looking down at the circular top of the brown shells with their characteristic seam, flat lay arrangement, detailed texture, white background"
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

        for view, prompt in task["prompts"].items():
            total_count += 1
            if view == "main":
                save_path = os.path.join(IMAGES_DIR, f"{plant_name}.png")
            else:
                save_path = os.path.join(plant_dir, f"{view}_{plant_name}.png")

            if download_image(prompt, save_path):
                success_count += 1
            time.sleep(1)

    print(f"\n===== 生成完成 =====")
    print(f"成功: {success_count}/{total_count}")

if __name__ == "__main__":
    generate_all_plants()
