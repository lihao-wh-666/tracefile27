"""
经济系统模块
管理阳光资源的收集与消耗
"""

from typing import Callable, Optional


class EconomyManager:
    """经济系统管理器"""

    def __init__(self, initial_sun: int = 150):
        """
        初始化经济系统

        Args:
            initial_sun: 初始阳光数量
        """
        self.sun_count: int = initial_sun
        self.sun_change_callback: Optional[Callable[[int], None]] = None

    def add_sun(self, amount: int):
        """
        增加阳光

        Args:
            amount: 增加数量
        """
        self.sun_count += amount
        if self.sun_change_callback:
            self.sun_change_callback(self.sun_count)

    def spend_sun(self, amount: int) -> bool:
        """
        消耗阳光

        Args:
            amount: 消耗数量

        Returns:
            是否消耗成功
        """
        if self.sun_count >= amount:
            self.sun_count -= amount
            if self.sun_change_callback:
                self.sun_change_callback(self.sun_count)
            return True
        return False

    def can_afford(self, amount: int) -> bool:
        """
        检查是否足够支付

        Args:
            amount: 需要消耗的数量

        Returns:
            是否足够
        """
        return self.sun_count >= amount

    def get_sun_count(self) -> int:
        """获取当前阳光数量"""
        return self.sun_count

    def set_sun_change_callback(self, callback: Callable[[int], None]):
        """
        设置阳光变化回调

        Args:
            callback: 回调函数，参数为当前阳光数量
        """
        self.sun_change_callback = callback

    def reset(self, initial_sun: int = 150):
        """
        重置经济系统

        Args:
            initial_sun: 初始阳光数量
        """
        self.sun_count = initial_sun
        if self.sun_change_callback:
            self.sun_change_callback(self.sun_count)
