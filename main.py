"""
植物大战僵尸 - 主入口文件
基于 Pygame 的2D塔防游戏
采用模块化分层设计架构
"""

import sys
import pygame

from game_core.game_controller import GameController
from res.config import GameConfig


def main():
    """游戏主入口函数"""
    try:
        pygame.init()
        pygame.mixer.init()
        
        config = GameConfig()
        game = GameController(config)
        game.run()
        
    except Exception as e:
        print(f"游戏启动失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
