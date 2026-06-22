import os
import sys
import pygame

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from res.config import GameConfig
from res.loader import ResourceLoader
from sprites.plants.sunflower import Sunflower
from sprites.plants.peashooter import Peashooter
from sprites.plants.wallnut import WallNut


class PlantDisplayTest:
    def __init__(self):
        pygame.init()
        self.WIDTH = 1100
        self.HEIGHT = 750
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("植物图片资源加载与显示测试")
        self.clock = pygame.time.Clock()

        self.config = GameConfig()
        self.loader = ResourceLoader(self.config)

        try:
            self.title_font = pygame.font.SysFont("simhei,microsoftyahei,arial", 28, bold=True)
            self.header_font = pygame.font.SysFont("simhei,microsoftyahei,arial", 20, bold=True)
            self.text_font = pygame.font.SysFont("simhei,microsoftyahei,arial", 14)
        except Exception:
            self.title_font = pygame.font.Font(None, 28)
            self.header_font = pygame.font.Font(None, 20)
            self.text_font = pygame.font.Font(None, 14)

        self.test_results = {
            "files_exist": [],
            "images_loaded": [],
            "sprites_created": [],
            "rendered": False
        }

    def test_file_existence(self):
        print("\n" + "=" * 60)
        print("【步骤 1/4】检查文件存在性与完整性")
        print("=" * 60)

        plants = ["sunflower", "peashooter", "wallnut"]
        views = [None, "front", "side", "top"]
        all_ok = True

        for plant in plants:
            species = self.config.PLANT_SPECIES.get(plant, {})
            cn_name = species.get("common_name_cn", plant)
            sci_name = species.get("scientific_name", "N/A")
            print(f"\n  植物: {cn_name} ({sci_name})")

            for view in views:
                filepath = self.config.get_plant_image_path(plant, view)
                label = "主视图" if view is None else f"{view}视图"

                if os.path.exists(filepath):
                    size_kb = os.path.getsize(filepath) / 1024
                    status = "✓" if size_kb < 2048 else "⚠"
                    print(f"    [{status}] {label}: {os.path.basename(filepath)} ({size_kb:.1f} KB)")
                    self.test_results["files_exist"].append((plant, view, True, size_kb))
                    if size_kb >= 2048:
                        all_ok = False
                else:
                    print(f"    [✗] {label}: 文件不存在 - {filepath}")
                    self.test_results["files_exist"].append((plant, view, False, 0))
                    all_ok = False

        return all_ok

    def test_image_loading(self):
        print("\n" + "=" * 60)
        print("【步骤 2/4】测试图片加载与分辨率")
        print("=" * 60)

        plants = ["sunflower", "peashooter", "wallnut"]
        views = [None, "front", "side", "top"]
        all_ok = True

        for plant in plants:
            species = self.config.PLANT_SPECIES.get(plant, {})
            cn_name = species.get("common_name_cn", plant)
            print(f"\n  植物: {cn_name}")

            for view in views:
                label = "主视图" if view is None else f"{view}视图"
                try:
                    if view is None:
                        img = self.loader.load_image(plant)
                    else:
                        img = self.loader.load_plant_image(plant, view)

                    w, h = img.get_size()
                    alpha_ok = img.get_bitsize() >= 24

                    status_res = "✓" if (w >= 1920 or h >= 1080) else "⚠"
                    status_alpha = "✓" if alpha_ok else "!"
                    print(f"    [{status_res}] {label}: {w}x{h} 像素 [Alpha:{status_alpha}]")

                    self.test_results["images_loaded"].append((plant, view, True, w, h))
                    if w < 1920 and h < 1080:
                        all_ok = False
                except Exception as e:
                    print(f"    [✗] {label}: 加载失败 - {e}")
                    self.test_results["images_loaded"].append((plant, view, False, 0, 0))
                    all_ok = False

        return all_ok

    def test_sprite_creation(self):
        print("\n" + "=" * 60)
        print("【步骤 3/4】测试植物精灵创建与图片集成")
        print("=" * 60)

        plant_classes = [
            ("sunflower", "向日葵", Sunflower),
            ("peashooter", "豌豆射手", Peashooter),
            ("wallnut", "坚果墙", WallNut),
        ]
        all_ok = True
        self.sprites = []

        for i, (plant_key, cn_name, PlantClass) in enumerate(plant_classes):
            try:
                row, col = i, 0
                args = (row, col, self.config.GRID_OFFSET_X, self.config.GRID_OFFSET_Y,
                        self.config.CELL_WIDTH, self.config.CELL_HEIGHT, self.loader)
                plant = PlantClass(*args)

                expected_w = int(self.config.CELL_WIDTH * 0.75)
                expected_h = int(self.config.CELL_HEIGHT * 0.75)
                actual_w, actual_h = plant.image.get_size()

                size_ok = (abs(actual_w - expected_w) <= 2 and abs(actual_h - expected_h) <= 2)
                status_size = "✓" if size_ok else "⚠"

                print(f"\n  {cn_name} ({plant_key}):")
                print(f"    [{status_size}] 精灵尺寸: {actual_w}x{actual_h} (期望 ~{expected_w}x{expected_h})")
                print(f"    [✓] 网格位置: 行{row} 列{col}")
                print(f"    [✓] 精灵Rect: {plant.rect}")

                self.sprites.append(plant)
                self.test_results["sprites_created"].append((plant_key, True, actual_w, actual_h))
                if not size_ok:
                    all_ok = False
            except Exception as e:
                print(f"\n  [✗] {cn_name} ({plant_key}) 创建失败: {e}")
                import traceback
                traceback.print_exc()
                self.test_results["sprites_created"].append((plant_key, False, 0, 0))
                all_ok = False

        return all_ok

    def test_render(self):
        print("\n" + "=" * 60)
        print("【步骤 4/4】可视化渲染测试 (显示3秒后自动关闭)")
        print("=" * 60)

        BG_COLOR = (240, 248, 240)
        GRID_LIGHT = (180, 220, 180)
        GRID_DARK = (140, 190, 140)

        start_ticks = pygame.time.get_ticks()
        duration = 3000
        running = True

        while running:
            elapsed = pygame.time.get_ticks() - start_ticks
            remaining = max(0, (duration - elapsed) // 1000)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = False

            self.screen.fill(BG_COLOR)

            title = self.title_font.render("植物图片资源加载与显示测试报告", True, (30, 80, 30))
            self.screen.blit(title, (self.WIDTH // 2 - title.get_width() // 2, 15))

            timer_text = self.text_font.render(f"窗口将在 {remaining} 秒后自动关闭 (按任意键/关闭窗口 提前退出)", True, (100, 100, 100))
            self.screen.blit(timer_text, (self.WIDTH // 2 - timer_text.get_width() // 2, 55))

            self._draw_sprites_section(GRID_LIGHT, GRID_DARK)
            self._draw_views_section()
            self._draw_summary_section()

            pygame.display.flip()
            self.clock.tick(30)

            if elapsed >= duration:
                running = False

        self.test_results["rendered"] = True
        print("  [✓] 可视化渲染完成")
        return True

    def _draw_sprites_section(self, light, dark):
        section_y = 80
        header = self.header_font.render("■ 植物精灵实际显示 (真实植物图片 + 自动缩放)", True, (50, 50, 50))
        self.screen.blit(header, (20, section_y))

        box_x, box_y = 20, section_y + 30
        box_w, box_h = 520, 260
        pygame.draw.rect(self.screen, (255, 255, 255), (box_x, box_y, box_w, box_h), 2)
        pygame.draw.rect(self.screen, (220, 240, 220), (box_x + 2, box_y + 2, box_w - 4, box_h - 4))

        cell_w = self.config.CELL_WIDTH
        cell_h = self.config.CELL_HEIGHT
        offset_x = box_x + 40
        offset_y = box_y + 30

        for r in range(3):
            for c in range(5):
                color = light if (r + c) % 2 == 0 else dark
                pygame.draw.rect(self.screen, color,
                                 (offset_x + c * cell_w, offset_y + r * cell_h, cell_w, cell_h))
                pygame.draw.rect(self.screen, (100, 150, 100),
                                 (offset_x + c * cell_w, offset_y + r * cell_h, cell_w, cell_h), 1)

        positions = [(0, 0), (1, 0), (2, 0)]
        plant_labels = ["向日葵", "豌豆射手", "坚果墙"]

        if hasattr(self, 'sprites'):
            for i, sprite in enumerate(self.sprites):
                if i < len(positions):
                    r, c = positions[i]
                    center_x = offset_x + c * cell_w + cell_w // 2
                    center_y = offset_y + r * cell_h + cell_h // 2
                    sprite.rect.center = (center_x, center_y)
                    self.screen.blit(sprite.image, sprite.rect)

                    label = self.text_font.render(plant_labels[i], True, (50, 50, 50))
                    label_x = offset_x + c * cell_w + cell_w + 10
                    label_y = center_y - label.get_height() // 2
                    self.screen.blit(label, (label_x, label_y))

    def _draw_views_section(self):
        section_x = 560
        section_y = 80
        header = self.header_font.render("■ 多视图参考 (正面/侧面/顶部)", True, (50, 50, 50))
        self.screen.blit(header, (section_x, section_y))

        box_x, box_y = section_x, section_y + 30
        box_w, box_h = 520, 260
        pygame.draw.rect(self.screen, (255, 255, 255), (box_x, box_y, box_w, box_h), 2)
        pygame.draw.rect(self.screen, (245, 245, 255), (box_x + 2, box_y + 2, box_w - 4, box_h - 4))

        plants = ["sunflower", "peashooter", "wallnut"]
        views = ["front", "side", "top"]
        view_labels = ["正面", "侧面", "顶部"]
        thumb_size = 70
        spacing_x = 10
        spacing_y = 10
        start_x = box_x + 10
        start_y = box_y + 10

        col_header_x = start_x + 90
        for vi, vlabel in enumerate(view_labels):
            hdr = self.text_font.render(vlabel, True, (80, 80, 80))
            self.screen.blit(hdr, (col_header_x + vi * (thumb_size + spacing_x) + thumb_size // 2 - hdr.get_width() // 2, start_y))

        row_start_y = start_y + 25
        for pi, plant in enumerate(plants):
            species = self.config.PLANT_SPECIES.get(plant, {})
            cn_name = species.get("common_name_cn", plant)
            name_lbl = self.text_font.render(cn_name, True, (50, 50, 50))
            self.screen.blit(name_lbl, (start_x, row_start_y + pi * (thumb_size + spacing_y) + thumb_size // 2 - name_lbl.get_height() // 2))

            for vi, view in enumerate(views):
                try:
                    img = self.loader.load_plant_image(plant, view)
                    thumb = pygame.transform.smoothscale(img, (thumb_size, thumb_size))
                    tx = col_header_x + vi * (thumb_size + spacing_x)
                    ty = row_start_y + pi * (thumb_size + spacing_y)
                    pygame.draw.rect(self.screen, (255, 255, 255), (tx - 1, ty - 1, thumb_size + 2, thumb_size + 2), 1)
                    self.screen.blit(thumb, (tx, ty))
                except Exception as e:
                    err_rect = pygame.Rect(col_header_x + vi * (thumb_size + spacing_x),
                                           row_start_y + pi * (thumb_size + spacing_y),
                                           thumb_size, thumb_size)
                    pygame.draw.rect(self.screen, (255, 200, 200), err_rect)
                    err_txt = self.text_font.render("ERR", True, (200, 0, 0))
                    self.screen.blit(err_txt, (err_rect.centerx - err_txt.get_width() // 2,
                                               err_rect.centery - err_txt.get_height() // 2))

    def _draw_summary_section(self):
        box_y = 360
        header = self.header_font.render("■ 测试结果汇总", True, (50, 50, 50))
        self.screen.blit(header, (20, box_y))

        summary_y = box_y + 35

        total_files = len(self.test_results["files_exist"])
        passed_files = sum(1 for r in self.test_results["files_exist"] if r[2])
        total_imgs = len(self.test_results["images_loaded"])
        passed_imgs = sum(1 for r in self.test_results["images_loaded"] if r[2])
        total_sprites = len(self.test_results["sprites_created"])
        passed_sprites = sum(1 for r in self.test_results["sprites_created"] if r[1])

        items = [
            ("文件存在性", passed_files, total_files, f"{passed_files}/{total_files} 个文件完整"),
            ("图片可加载", passed_imgs, total_imgs, f"{passed_imgs}/{total_imgs} 张图片加载成功"),
            ("精灵创建", passed_sprites, total_sprites, f"{passed_sprites}/{total_sprites} 个精灵创建成功"),
            ("可视化渲染", 1 if self.test_results["rendered"] else 0, 1, "渲染测试通过" if self.test_results["rendered"] else "渲染测试未完成"),
        ]

        all_pass = True
        for i, (label, passed, total, desc) in enumerate(items):
            y = summary_y + i * 30
            status = "✓  通过" if passed == total else "✗  失败"
            color = (0, 150, 0) if passed == total else (200, 0, 0)
            if passed != total:
                all_pass = False

            status_txt = self.header_font.render(status, True, color)
            label_txt = self.text_font.render(f"{label}:", True, (50, 50, 50))
            desc_txt = self.text_font.render(desc, True, (80, 80, 80))

            self.screen.blit(status_txt, (20, y))
            self.screen.blit(label_txt, (130, y + 5))
            self.screen.blit(desc_txt, (260, y + 5))

        result_y = summary_y + 4 * 30 + 20
        if all_pass:
            result_bg = (200, 255, 200)
            result_text = "全部测试通过! 植物图片资源加载与显示一切正常 ✓"
            result_color = (0, 120, 0)
        else:
            result_bg = (255, 220, 220)
            result_text = "部分测试失败! 请检查上方详细信息 ✗"
            result_color = (180, 0, 0)

        pygame.draw.rect(self.screen, result_bg, (20, result_y, self.WIDTH - 40, 50))
        pygame.draw.rect(self.screen, result_color, (20, result_y, self.WIDTH - 40, 50), 3)
        final = self.title_font.render(result_text, True, result_color)
        self.screen.blit(final, (self.WIDTH // 2 - final.get_width() // 2, result_y + 12))

    def print_final_report(self):
        print("\n" + "=" * 60)
        print("最终测试报告")
        print("=" * 60)

        total = len(self.test_results["files_exist"])
        passed = sum(1 for r in self.test_results["files_exist"] if r[2])
        print(f"  文件存在性: {passed}/{total}")

        total = len(self.test_results["images_loaded"])
        passed = sum(1 for r in self.test_results["images_loaded"] if r[2])
        print(f"  图片加载:   {passed}/{total}")

        total = len(self.test_results["sprites_created"])
        passed = sum(1 for r in self.test_results["sprites_created"] if r[1])
        print(f"  精灵创建:   {passed}/{total}")

        print(f"  渲染测试:   {'通过' if self.test_results['rendered'] else '未完成'}")
        print("=" * 60)

    def run(self):
        try:
            r1 = self.test_file_existence()
            r2 = self.test_image_loading()
            r3 = self.test_sprite_creation()
            r4 = self.test_render()
            self.print_final_report()
            pygame.quit()
            return all([r1, r2, r3, r4])
        except Exception as e:
            print(f"\n测试过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            pygame.quit()
            return False


if __name__ == "__main__":
    test = PlantDisplayTest()
    success = test.run()
    sys.exit(0 if success else 1)
