"""
游戏场景模块
主游戏场景
"""

import pygame
import random

from scene.base_scene import BaseScene
from sprites.plants.sunflower import Sunflower
from sprites.plants.peashooter import Peashooter
from sprites.plants.wallnut import WallNut
from sprites.zombies.normal_zombie import NormalZombie
from sprites.zombies.cone_zombie import ConeZombie
from sprites.bullet import PeaBullet
from sprites.sun import Sun
from ui.font_utils import get_font


class GameScene(BaseScene):
    """游戏场景"""

    def __init__(self, game_controller=None):
        super().__init__(game_controller)
        self.name = "game"

        self.plants = pygame.sprite.Group()
        self.zombies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.suns = pygame.sprite.Group()

        self.selected_plant = None
        self.grid_plants = {}

        self.dragging = False
        self.drag_plant_type = None
        self.drag_mouse_pos = (0, 0)
        self.drag_ghost_image = None
        self.hover_grid_pos = None
        self.hover_grid_valid = False

        self.last_zombie_spawn = 0
        self.last_sun_fall = 0
        self.game_start_time = 0

        self.font = None
        self.small_font = None

    def _on_enter(self):
        """进入游戏场景"""
        self._init_fonts()

        is_restart = self.scene_data.get("restart", False)
        from_pause = self.scene_data.get("from_pause", False)

        if not from_pause or is_restart:
            self._reset_game()
            self._start_game()

        self.scene_data = {}

    def _init_fonts(self):
        """初始化字体"""
        self.font = get_font(24)
        self.small_font = get_font(16)

    def _reset_game(self):
        """重置游戏状态"""
        self.plants.empty()
        self.zombies.empty()
        self.bullets.empty()
        self.suns.empty()
        self.grid_plants.clear()
        self.selected_plant = None
        self.dragging = False
        self.drag_plant_type = None
        self.drag_ghost_image = None
        self.hover_grid_pos = None
        self.hover_grid_valid = False

    def _start_game(self):
        """开始游戏"""
        if self.game_controller:
            self.game_controller.economy.reset(self.game_controller.config.INITIAL_SUN)
            self.game_controller.level_manager.start_level(1)

    def handle_event(self, event: pygame.event.Event):
        """处理游戏事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.set_next_scene("pause")
            elif event.key == pygame.K_1:
                self._start_drag("sunflower", pygame.mouse.get_pos())
            elif event.key == pygame.K_2:
                self._start_drag("peashooter", pygame.mouse.get_pos())
            elif event.key == pygame.K_3:
                self._start_drag("wallnut", pygame.mouse.get_pos())

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._handle_mouse_down(event.pos)
            elif event.button == 3:
                self._cancel_drag()

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self._handle_mouse_motion(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragging:
                self._handle_mouse_up(event.pos)

    def _start_drag(self, plant_type: str, mouse_pos=None):
        """开始拖拽植物"""
        if not self.game_controller:
            return
        cost = self.game_controller.config.PLANT_COSTS.get(plant_type, 0)
        if not self.game_controller.economy.can_afford(cost):
            return

        self.dragging = True
        self.drag_plant_type = plant_type
        self.selected_plant = plant_type
        self.drag_ghost_image = self._create_ghost_image(plant_type)
        if mouse_pos:
            self.drag_mouse_pos = mouse_pos

    def _cancel_drag(self):
        """取消拖拽"""
        self.dragging = False
        self.drag_plant_type = None
        self.selected_plant = None
        self.drag_ghost_image = None
        self.hover_grid_pos = None
        self.hover_grid_valid = False

    def _create_ghost_image(self, plant_type: str):
        """创建拖拽时的半透明预览图像"""
        if not self.game_controller:
            return None

        config = self.game_controller.config
        args = (0, 0, config.GRID_OFFSET_X, config.GRID_OFFSET_Y,
                config.CELL_WIDTH, config.CELL_HEIGHT,
                self.game_controller.resource_loader)

        if plant_type == "sunflower":
            from sprites.plants.sunflower import Sunflower
            plant = Sunflower(*args)
        elif plant_type == "peashooter":
            from sprites.plants.peashooter import Peashooter
            plant = Peashooter(*args)
        elif plant_type == "wallnut":
            from sprites.plants.wallnut import WallNut
            plant = WallNut(*args)
        else:
            return None

        ghost_image = plant.image.copy()
        ghost_image.set_alpha(150)
        return ghost_image

    def _handle_mouse_down(self, pos):
        """处理鼠标按下"""
        if self.game_controller:
            clicked_suns = self.game_controller.collision_manager.check_sun_click_collision(
                self.suns, pos
            )
            for sun in clicked_suns:
                sun.collect()
                return

        plant_type = self._get_plant_card_at_pos(pos)
        if plant_type:
            self._start_drag(plant_type, pos)
            return

        if self.selected_plant and not self.dragging:
            grid_pos = self._pixel_to_grid(pos)
            if grid_pos:
                self._try_plant(grid_pos[0], grid_pos[1])

    def _handle_mouse_motion(self, pos):
        """处理鼠标移动（拖拽中）"""
        self.drag_mouse_pos = pos
        grid_pos = self._pixel_to_grid(pos)
        if grid_pos:
            self.hover_grid_pos = grid_pos
            self.hover_grid_valid = self._is_grid_valid(grid_pos[0], grid_pos[1])
        else:
            self.hover_grid_pos = None
            self.hover_grid_valid = False

    def _handle_mouse_up(self, pos):
        """处理鼠标释放"""
        if not self.dragging or not self.drag_plant_type:
            return

        grid_pos = self._pixel_to_grid(pos)
        if grid_pos and self._is_grid_valid(grid_pos[0], grid_pos[1]):
            self._try_plant(grid_pos[0], grid_pos[1])

        self._cancel_drag()

    def _get_plant_card_at_pos(self, pos):
        """获取点击位置的植物卡片类型"""
        if not self.game_controller:
            return None

        x, y = pos
        if y > 70:
            return None

        plant_types = [
            ("sunflower", 50),
            ("peashooter", 100),
            ("wallnut", 50),
        ]

        x_start = 150
        card_width = 100
        card_height = 50
        card_y = 10

        for i, (name, cost) in enumerate(plant_types):
            card_x = x_start + i * 120
            if (card_x <= x <= card_x + card_width and
                card_y <= y <= card_y + card_height):
                if self.game_controller.economy.can_afford(cost):
                    return name
        return None

    def _is_grid_valid(self, row: int, col: int) -> bool:
        """检查网格位置是否有效（可种植）"""
        if not self.game_controller:
            return False

        config = self.game_controller.config
        if row < 0 or row >= config.GRID_ROWS:
            return False
        if col < 0 or col >= config.GRID_COLS:
            return False

        grid_key = (row, col)
        if grid_key in self.grid_plants:
            return False

        return True

    def _select_plant(self, plant_type: str):
        """选择植物"""
        if not self.game_controller:
            return
        cost = self.game_controller.config.PLANT_COSTS.get(plant_type, 0)
        if self.game_controller.economy.can_afford(cost):
            self.selected_plant = plant_type
        else:
            self.selected_plant = None

    def _pixel_to_grid(self, pos):
        """像素转网格坐标"""
        if not self.game_controller:
            return None

        x, y = pos
        config = self.game_controller.config
        col = int((x - config.GRID_OFFSET_X) / config.CELL_WIDTH)
        row = int((y - config.GRID_OFFSET_Y) / config.CELL_HEIGHT)

        if 0 <= row < config.GRID_ROWS and 0 <= col < config.GRID_COLS:
            if (x >= config.GRID_OFFSET_X and
                x < config.GRID_OFFSET_X + config.GRID_COLS * config.CELL_WIDTH and
                y >= config.GRID_OFFSET_Y and
                y < config.GRID_OFFSET_Y + config.GRID_ROWS * config.CELL_HEIGHT):
                return row, col
        return None

    def _try_plant(self, row: int, col: int):
        """尝试种植植物"""
        if not self.selected_plant or not self.game_controller:
            return False

        grid_key = (row, col)
        if grid_key in self.grid_plants:
            return False

        cost = self.game_controller.config.PLANT_COSTS.get(self.selected_plant, 0)
        if not self.game_controller.economy.spend_sun(cost):
            return False

        plant = self._create_plant(self.selected_plant, row, col)
        if plant:
            self.plants.add(plant)
            self.grid_plants[grid_key] = plant
            self.selected_plant = None
            return True

        return False

    def _create_plant(self, plant_type: str, row: int, col: int):
        """创建植物"""
        if not self.game_controller:
            return None

        config = self.game_controller.config
        args = (row, col, config.GRID_OFFSET_X, config.GRID_OFFSET_Y,
                config.CELL_WIDTH, config.CELL_HEIGHT,
                self.game_controller.resource_loader)

        if plant_type == "sunflower":
            plant = Sunflower(*args)
            plant.set_sun_spawn_callback(self._on_sun_spawn)
        elif plant_type == "peashooter":
            plant = Peashooter(*args)
            plant.set_bullet_spawn_callback(self._on_bullet_spawn)
        elif plant_type == "wallnut":
            plant = WallNut(*args)
        else:
            return None

        return plant

    def _on_sun_spawn(self, x: float, y: float, from_plant: bool = False):
        """阳光生成回调"""
        if not self.game_controller:
            return
        sun = Sun(x, y, self.game_controller.config.SUN_VALUE,
                  from_plant=from_plant,
                  resource_loader=self.game_controller.resource_loader)
        sun.set_collect_callback(self._on_sun_collect)
        self.suns.add(sun)

    def _on_sun_collect(self, value: int):
        """阳光收集回调"""
        if self.game_controller:
            self.game_controller.economy.add_sun(value)

    def _on_bullet_spawn(self, x: float, y: float, row: int,
                         speed: float, damage: int):
        """子弹生成回调"""
        if not self.game_controller:
            return
        bullet = PeaBullet(x, y, row, speed, damage,
                           self.game_controller.resource_loader)
        self.bullets.add(bullet)

    def update(self, current_time: int, *args, **kwargs):
        """更新游戏逻辑"""
        if self.game_start_time == 0:
            self.game_start_time = current_time
            self.last_zombie_spawn = current_time
            self.last_sun_fall = current_time

        self._update_sun_fall(current_time)
        self._update_zombie_spawn(current_time)
        self._update_entities(current_time)
        self._check_collisions()
        self._check_game_end()

    def _update_sun_fall(self, current_time: int):
        """更新天降阳光"""
        if not self.game_controller:
            return

        config = self.game_controller.config
        if current_time - self.last_sun_fall >= config.SUN_FALL_INTERVAL:
            x = random.randint(config.GRID_OFFSET_X,
                               config.SCREEN_WIDTH - 100)
            y = -50
            self._on_sun_spawn(x, y, from_plant=False)
            self.last_sun_fall = current_time

    def _update_zombie_spawn(self, current_time: int):
        """更新僵尸生成"""
        if not self.game_controller:
            return

        wave = self.game_controller.level_manager.get_current_wave()
        if not wave:
            return

        if self.game_controller.level_manager.check_wave_complete():
            if len(self.zombies) == 0:
                self.game_controller.level_manager.next_wave()
            return

        if current_time - self.last_zombie_spawn >= wave.spawn_interval:
            zombie_type = self.game_controller.level_manager.get_next_zombie_type()
            if zombie_type:
                self._spawn_zombie(zombie_type)
                self.game_controller.level_manager.zombie_spawned()
                self.last_zombie_spawn = current_time

    def _spawn_zombie(self, zombie_type: str):
        """生成僵尸"""
        if not self.game_controller:
            return

        config = self.game_controller.config
        row = random.randint(0, config.GRID_ROWS - 1)
        x = config.SCREEN_WIDTH + 50

        args = (row, x, config.GRID_OFFSET_X, config.GRID_OFFSET_Y,
                config.CELL_WIDTH, config.CELL_HEIGHT,
                self.game_controller.resource_loader)

        if zombie_type == "normal_zombie":
            zombie = NormalZombie(*args)
        elif zombie_type == "cone_zombie":
            zombie = ConeZombie(*args)
        else:
            zombie = NormalZombie(*args)

        self.zombies.add(zombie)

    def _update_entities(self, current_time: int):
        """更新所有实体"""
        self.plants.update(current_time, zombies_group=self.zombies)
        self.zombies.update(current_time, plants_group=self.plants)
        self.bullets.update(screen_width=self.game_controller.config.SCREEN_WIDTH
                           if self.game_controller else 900)
        self.suns.update(current_time)

        for zombie in self.zombies:
            zombie.check_collision_with_plant(self.plants)

        dead_plants = []
        for plant in self.plants:
            if not plant.alive():
                dead_plants.append(plant)

        for plant in dead_plants:
            grid_key = (plant.row, plant.col)
            if grid_key in self.grid_plants:
                del self.grid_plants[grid_key]

    def _check_collisions(self):
        """检测碰撞"""
        if not self.game_controller:
            return

        bullet_zombie_hits = self.game_controller.collision_manager.check_bullet_zombie_collisions(
            self.bullets, self.zombies
        )
        for bullet, zombie in bullet_zombie_hits:
            damage = bullet.get_damage()
            zombie.take_damage(damage)
            bullet.hit_zombie()
            if not zombie.alive():
                self.game_controller.level_manager.zombie_killed()

    def _check_game_end(self):
        """检查游戏结束"""
        if not self.game_controller:
            return

        config = self.game_controller.config
        house_x = config.GRID_OFFSET_X - 30

        reached_zombies = self.game_controller.collision_manager.check_zombie_reach_house(
            self.zombies, house_x
        )
        if reached_zombies:
            self.game_controller.level_manager.set_game_over()
            self.set_next_scene("lose", {"is_win": False})
            return

        if (self.game_controller.level_manager.is_level_complete() and
            len(self.zombies) == 0):
            self.set_next_scene("win", {"is_win": True})

    def render(self, surface: pygame.Surface):
        """渲染游戏场景"""
        if not self.game_controller:
            return

        config = self.game_controller.config

        self._render_background(surface, config)
        self._render_grid(surface, config)
        self._render_grid_highlight(surface, config)
        self.plants.draw(surface)
        self.zombies.draw(surface)
        self.bullets.draw(surface)
        self.suns.draw(surface)
        self._draw_hp_bars(surface)
        self._render_ui(surface, config)
        self._render_drag_ghost(surface)

    def _render_background(self, surface: pygame.Surface, config):
        """渲染背景"""
        surface.fill((120, 180, 120))

        lawn_left = config.GRID_OFFSET_X
        lawn_top = config.GRID_OFFSET_Y
        lawn_width = config.GRID_COLS * config.CELL_WIDTH
        lawn_height = config.GRID_ROWS * config.CELL_HEIGHT

        pygame.draw.rect(surface, (80, 160, 80),
                         (lawn_left, lawn_top, lawn_width, lawn_height))

    def _render_grid(self, surface: pygame.Surface, config):
        """渲染网格"""
        grid_color = (60, 140, 60)

        for row in range(config.GRID_ROWS + 1):
            y = config.GRID_OFFSET_Y + row * config.CELL_HEIGHT
            start_x = config.GRID_OFFSET_X
            end_x = config.GRID_OFFSET_X + config.GRID_COLS * config.CELL_WIDTH
            pygame.draw.line(surface, grid_color, (start_x, y), (end_x, y), 2)

        for col in range(config.GRID_COLS + 1):
            x = config.GRID_OFFSET_X + col * config.CELL_WIDTH
            start_y = config.GRID_OFFSET_Y
            end_y = config.GRID_OFFSET_Y + config.GRID_ROWS * config.CELL_HEIGHT
            pygame.draw.line(surface, grid_color, (x, start_y), (x, end_y), 2)

    def _render_grid_highlight(self, surface: pygame.Surface, config):
        """渲染网格高亮"""
        if not self.hover_grid_pos or not self.dragging:
            return

        row, col = self.hover_grid_pos
        cell_x = config.GRID_OFFSET_X + col * config.CELL_WIDTH
        cell_y = config.GRID_OFFSET_Y + row * config.CELL_HEIGHT

        if self.hover_grid_valid:
            highlight_color = (0, 255, 0, 80)
        else:
            highlight_color = (255, 0, 0, 80)

        highlight_surface = pygame.Surface(
            (config.CELL_WIDTH, config.CELL_HEIGHT), pygame.SRCALPHA
        )
        highlight_surface.fill(highlight_color)
        surface.blit(highlight_surface, (cell_x, cell_y))

    def _render_drag_ghost(self, surface: pygame.Surface):
        """渲染拖拽时的幽灵植物"""
        if not self.dragging or not self.drag_ghost_image:
            return

        ghost_rect = self.drag_ghost_image.get_rect()
        ghost_rect.center = self.drag_mouse_pos
        surface.blit(self.drag_ghost_image, ghost_rect)

    def _draw_hp_bars(self, surface: pygame.Surface):
        """绘制血条"""
        for plant in self.plants:
            plant.draw_hp_bar(surface)
        for zombie in self.zombies:
            zombie.draw_hp_bar(surface)

    def _render_ui(self, surface: pygame.Surface, config):
        """渲染UI"""
        ui_bg = pygame.Surface((config.SCREEN_WIDTH, 70))
        ui_bg.fill((139, 90, 43))
        surface.blit(ui_bg, (0, 0))

        sun_text = self.font.render(
            f"☀ {self.game_controller.economy.get_sun_count()}",
            True, (255, 255, 0)
        )
        surface.blit(sun_text, (20, 20))

        plant_types = [
            ("1", "sunflower", 50, (255, 215, 0)),
            ("2", "peashooter", 100, (34, 139, 34)),
            ("3", "wallnut", 50, (139, 90, 43)),
        ]

        x_start = 150
        for i, (key, name, cost, color) in enumerate(plant_types):
            x = x_start + i * 120
            can_afford = self.game_controller.economy.can_afford(cost)
            is_selected = self.selected_plant == name

            box_color = (200, 200, 200) if can_afford else (100, 100, 100)
            if is_selected:
                box_color = (255, 255, 100)

            pygame.draw.rect(surface, box_color, (x, 10, 100, 50))
            pygame.draw.rect(surface, (0, 0, 0), (x, 10, 100, 50), 2)

            pygame.draw.circle(surface, color, (x + 25, 35), 15)

            cost_color = (0, 0, 0) if can_afford else (255, 0, 0)
            cost_text = self.small_font.render(f"[{key}] {cost}", True, cost_color)
            surface.blit(cost_text, (x + 45, 28))

        level_info = self.game_controller.level_manager.get_level_info()
        level_text = self.small_font.render(
            f"第{level_info[0]}关 波次{level_info[1]}/{level_info[2]}",
            True, (255, 255, 255)
        )
        level_rect = level_text.get_rect(right=config.SCREEN_WIDTH - 20, top=25)
        surface.blit(level_text, level_rect)
