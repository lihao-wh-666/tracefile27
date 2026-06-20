"""
关卡系统模块
管理关卡配置、波次生成和游戏进度
"""

import random
from typing import List, Dict, Tuple, Optional


class WaveConfig:
    """波次配置"""

    def __init__(self, wave_num: int, zombie_count: int, zombie_types: List[str],
                 spawn_interval: int = 5000):
        """
        初始化波次配置

        Args:
            wave_num: 波次编号
            zombie_count: 僵尸总数
            zombie_types: 僵尸类型列表
            spawn_interval: 生成间隔（毫秒）
        """
        self.wave_num = wave_num
        self.zombie_count = zombie_count
        self.zombie_types = zombie_types
        self.spawn_interval = spawn_interval


class LevelConfig:
    """关卡配置"""

    def __init__(self, level_num: int, name: str, waves: List[WaveConfig],
                 rows: int = 5, cols: int = 9):
        """
        初始化关卡配置

        Args:
            level_num: 关卡编号
            name: 关卡名称
            waves: 波次列表
            rows: 行数
            cols: 列数
        """
        self.level_num = level_num
        self.name = name
        self.waves = waves
        self.rows = rows
        self.cols = cols


class LevelManager:
    """关卡管理器"""

    def __init__(self):
        """初始化关卡管理器"""
        self.levels: Dict[int, LevelConfig] = {}
        self.current_level: Optional[LevelConfig] = None
        self.current_wave_index: int = 0
        self.zombies_spawned_in_wave: int = 0
        self.total_zombies_killed: int = 0
        self.level_complete: bool = False
        self.game_over: bool = False

        self._init_default_levels()

    def _init_default_levels(self):
        """初始化默认关卡"""
        waves = [
            WaveConfig(1, 5, ["normal_zombie"], 8000),
            WaveConfig(2, 8, ["normal_zombie"], 6000),
            WaveConfig(3, 10, ["normal_zombie", "cone_zombie"], 5000),
            WaveConfig(4, 12, ["normal_zombie", "cone_zombie"], 4500),
            WaveConfig(5, 15, ["normal_zombie", "cone_zombie"], 4000),
        ]

        level1 = LevelConfig(1, "第一关：草坪", waves)
        self.levels[1] = level1

    def start_level(self, level_num: int) -> bool:
        """
        开始关卡

        Args:
            level_num: 关卡编号

        Returns:
            是否成功开始
        """
        if level_num not in self.levels:
            return False

        self.current_level = self.levels[level_num]
        self.current_wave_index = 0
        self.zombies_spawned_in_wave = 0
        self.total_zombies_killed = 0
        self.level_complete = False
        self.game_over = False
        return True

    def get_current_wave(self) -> Optional[WaveConfig]:
        """获取当前波次配置"""
        if not self.current_level:
            return None
        if self.current_wave_index >= len(self.current_level.waves):
            return None
        return self.current_level.waves[self.current_wave_index]

    def get_next_zombie_type(self) -> Optional[str]:
        """
        获取下一个要生成的僵尸类型

        Returns:
            僵尸类型名称
        """
        wave = self.get_current_wave()
        if not wave:
            return None

        if self.zombies_spawned_in_wave >= wave.zombie_count:
            return None

        return random.choice(wave.zombie_types)

    def zombie_spawned(self):
        """记录一个僵尸已生成"""
        self.zombies_spawned_in_wave += 1

    def zombie_killed(self):
        """记录一个僵尸被消灭"""
        self.total_zombies_killed += 1

    def check_wave_complete(self) -> bool:
        """
        检查当前波次是否完成

        Returns:
            是否完成
        """
        wave = self.get_current_wave()
        if not wave:
            return False
        return self.zombies_spawned_in_wave >= wave.zombie_count

    def next_wave(self) -> bool:
        """
        进入下一波

        Returns:
            是否成功进入下一波
        """
        if not self.current_level:
            return False

        self.current_wave_index += 1
        self.zombies_spawned_in_wave = 0

        if self.current_wave_index >= len(self.current_level.waves):
            self.level_complete = True
            return False

        return True

    def is_level_complete(self) -> bool:
        """检查关卡是否完成"""
        return self.level_complete

    def is_game_over(self) -> bool:
        """检查游戏是否失败"""
        return self.game_over

    def set_game_over(self):
        """设置游戏失败"""
        self.game_over = True

    def get_level_info(self) -> Tuple[int, int, int]:
        """
        获取关卡信息

        Returns:
            (关卡编号, 当前波次, 总波次)
        """
        if not self.current_level:
            return (0, 0, 0)
        return (self.current_level.level_num,
                self.current_wave_index + 1,
                len(self.current_level.waves))

    def get_progress(self) -> float:
        """
        获取关卡进度

        Returns:
            进度值 0.0 - 1.0
        """
        if not self.current_level:
            return 0.0

        total_waves = len(self.current_level.waves)
        if total_waves == 0:
            return 0.0

        wave_progress = self.current_wave_index / total_waves
        return min(1.0, wave_progress)

    def reset(self):
        """重置关卡状态"""
        self.current_level = None
        self.current_wave_index = 0
        self.zombies_spawned_in_wave = 0
        self.total_zombies_killed = 0
        self.level_complete = False
        self.game_over = False
