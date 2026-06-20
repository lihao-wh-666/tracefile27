"""
植物大战僵尸 - 主入口文件
基于 Pygame 的2D塔防游戏
采用模块化分层设计架构
支持命令行参数配置启动选项
"""

import argparse
import sys
import logging

import pygame

from game_core.game_controller import GameController
from res.config import GameConfig


def parse_args():
    parser = argparse.ArgumentParser(
        description="植物大战僵尸 - 基于Pygame的2D塔防游戏",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  python main.py --fullscreen          以全屏模式启动
  python main.py --fps 30              以30帧率启动
  python main.py --no-audio            禁用音频
  python main.py --debug               启用调试模式
  python main.py --width 1280 --height 720  自定义分辨率"""
    )
    parser.add_argument(
        "--fullscreen", "-f",
        action="store_true",
        help="以全屏模式启动游戏"
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=60,
        help="设置目标帧率 (默认: 60)"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=900,
        help="设置窗口宽度 (默认: 900)"
    )
    parser.add_argument(
        "--height",
        type=int,
        default=600,
        help="设置窗口高度 (默认: 600)"
    )
    parser.add_argument(
        "--bgm-volume",
        type=float,
        default=0.5,
        help="设置背景音乐音量 0.0-1.0 (默认: 0.5)"
    )
    parser.add_argument(
        "--sfx-volume",
        type=float,
        default=0.7,
        help="设置音效音量 0.0-1.0 (默认: 0.7)"
    )
    parser.add_argument(
        "--no-audio",
        action="store_true",
        help="禁用所有音频"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="启用调试模式，输出详细日志信息"
    )
    return parser.parse_args()


def setup_logging(debug=False):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return logging.getLogger("PvZ")


def main():
    logger = setup_logging()
    try:
        args = parse_args()
        if args.debug:
            logger = setup_logging(debug=True)
            logger.debug("调试模式已启用")
            logger.debug("命令行参数: %s", vars(args))

        logger.info("正在初始化游戏...")

        pygame.init()
        if not args.no_audio:
            pygame.mixer.init()
            logger.info("音频系统初始化成功")
        else:
            logger.info("音频已禁用")

        config = GameConfig()
        config.SCREEN_WIDTH = args.width
        config.SCREEN_HEIGHT = args.height
        config.FPS = args.fps
        config.FULLSCREEN = args.fullscreen
        config.BGM_VOLUME = max(0.0, min(1.0, args.bgm_volume))
        config.SFX_VOLUME = max(0.0, min(1.0, args.sfx_volume))

        logger.info(
            "窗口配置: %dx%d, FPS=%d, 全屏=%s",
            config.SCREEN_WIDTH, config.SCREEN_HEIGHT,
            config.FPS, config.FULLSCREEN
        )
        logger.info(
            "音量配置: BGM=%.1f, SFX=%.1f",
            config.BGM_VOLUME, config.SFX_VOLUME
        )

        game = GameController(config)
        logger.info("游戏启动成功")
        game.run()

    except KeyboardInterrupt:
        logger.info("用户中断游戏")
    except ImportError as e:
        logger.error("缺少依赖库: %s", e)
        logger.error("请运行: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        logger.error("游戏启动失败: %s", e)
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        pygame.quit()
        logger.info("游戏已退出")


if __name__ == "__main__":
    main()
