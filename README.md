# 植物大战僵尸 (Plants vs Zombies)

基于 Pygame 框架开发的2D塔防小游戏，采用模块化分层设计架构。

## 项目简介

本项目是《植物大战僵尸》游戏的 Pygame 实现版本，采用高度解耦的模块化设计，
包含5大核心模块：资源模块、场景模块、实体角色模块、游戏核心逻辑模块和UI交互模块。

## 系统要求

- Python 3.8+
- Pygame 2.0+

## 安装与运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行游戏

```bash
python main.py
```

## 游戏操作

| 按键 | 功能 |
|------|------|
| 1 | 选择向日葵 |
| 2 | 选择豌豆射手 |
| 3 | 选择坚果墙 |
| 鼠标左键 | 种植植物 / 收集阳光 |
| 鼠标右键 | 取消植物选择 |
| ESC | 暂停游戏 / 返回菜单 |
| F | 切换全屏模式 |
| Enter / Space | 开始游戏 |
| R | 重新开始 |
| M | 返回主菜单 |

## 项目架构

项目采用模块化分层设计，共分为5个核心模块：

### 1. 资源模块 (res)
**职责**：统一管理游戏内所有资源

- `config.py` - 游戏配置类，管理所有游戏参数
- `loader.py` - 资源加载器，负责图片、音频、字体的加载与缓存

**特性**：
- 资源缓存机制，避免重复加载
- 自动降级：资源文件缺失时自动生成占位图形
- 统一资源路径管理

### 2. 场景模块 (scene)
**职责**：管理游戏场景的切换与生命周期

- `base_scene.py` - 场景基类，定义场景接口
- `scene_manager.py` - 场景管理器，负责场景切换
- `menu_scene.py` - 主菜单场景
- `game_scene.py` - 游戏主场景
- `pause_scene.py` - 暂停场景
- `end_scene.py` - 胜利/失败结束场景

**特性**：
- 场景间数据传递机制
- 清晰的进入/退出生命周期
- 支持暂停后恢复游戏状态

### 3. 实体角色模块 (sprites)
**职责**：封装所有游戏实体的属性与行为

**植物**：
- `base/plant.py` - 植物基类
- `plants/sunflower.py` - 向日葵（产生阳光）
- `plants/peashooter.py` - 豌豆射手（攻击僵尸）
- `plants/wallnut.py` - 坚果墙（高血量防御）

**僵尸**：
- `base/zombie.py` - 僵尸基类
- `zombies/normal_zombie.py` - 普通僵尸
- `zombies/cone_zombie.py` - 路障僵尸（高血量）

**其他**：
- `bullet.py` - 豌豆子弹
- `sun.py` - 阳光道具

**特性**：
- 面向对象设计，继承层次清晰
- 回调机制实现实体间解耦
- 统一的碰撞检测接口

### 4. 游戏核心逻辑模块 (game_core)
**职责**：作为游戏主控制器，协调各模块交互

- `game_controller.py` - 游戏主控制器
- `level.py` - 关卡系统，波次管理
- `economy.py` - 经济系统，阳光资源管理
- `collision.py` - 碰撞检测管理器

**特性**：
- 关卡波次系统，难度递进
- 经济平衡系统
- 统一的碰撞检测

### 5. UI交互模块 (ui)
**职责**：所有用户界面元素的绘制与交互

- `button.py` - 通用按钮组件
- `sun_display.py` - 阳光数量显示
- `plant_selector.py` - 植物选择栏
- `progress_bar.py` - 进度条组件

**特性**：
- 可复用的UI组件
- 事件驱动的交互机制
- 独立的绘制与更新逻辑

## 扩展开发指南

### 添加新植物

1. 在 `sprites/plants/` 下创建新的植物类，继承 `PlantBase`
2. 在 `res/config.py` 中添加植物配置（花费、冷却等）
3. 在 `game_scene.py` 中注册植物创建逻辑
4. 在 `ui/plant_selector.py` 中添加植物卡片

### 添加新僵尸

1. 在 `sprites/zombies/` 下创建新的僵尸类，继承 `ZombieBase`
2. 在 `game_core/level.py` 的波次配置中添加僵尸类型
3. 在 `game_scene.py` 中注册僵尸创建逻辑

### 添加新场景

1. 在 `scene/` 下创建新的场景类，继承 `BaseScene`
2. 实现 `_on_enter()`、`handle_event()`、`update()`、`render()` 方法
3. 在 `game_controller.py` 中注册场景

## 目录结构

```
plants_vs_zombies/
├── main.py                    # 游戏入口
├── requirements.txt           # 依赖列表
├── README.md                  # 开发文档
├── .gitignore                 # Git忽略配置
├── res/                       # 资源模块
│   ├── __init__.py
│   ├── config.py              # 游戏配置
│   └── loader.py              # 资源加载器
├── scene/                     # 场景模块
│   ├── __init__.py
│   ├── base_scene.py          # 场景基类
│   ├── scene_manager.py       # 场景管理器
│   ├── menu_scene.py          # 主菜单场景
│   ├── game_scene.py          # 游戏场景
│   ├── pause_scene.py         # 暂停场景
│   └── end_scene.py           # 结束场景
├── sprites/                   # 实体角色模块
│   ├── __init__.py
│   ├── base/
│   │   ├── plant.py           # 植物基类
│   │   └── zombie.py          # 僵尸基类
│   ├── plants/
│   │   ├── sunflower.py       # 向日葵
│   │   ├── peashooter.py      # 豌豆射手
│   │   └── wallnut.py         # 坚果墙
│   ├── zombies/
│   │   ├── normal_zombie.py   # 普通僵尸
│   │   └── cone_zombie.py     # 路障僵尸
│   ├── bullet.py              # 豌豆子弹
│   └── sun.py                 # 阳光
├── game_core/                 # 游戏核心逻辑模块
│   ├── __init__.py
│   ├── game_controller.py     # 游戏控制器
│   ├── level.py               # 关卡系统
│   ├── economy.py             # 经济系统
│   └── collision.py           # 碰撞检测
├── ui/                        # UI交互模块
│   ├── __init__.py
│   ├── button.py              # 按钮
│   ├── sun_display.py         # 阳光显示
│   ├── plant_selector.py      # 植物选择栏
│   └── progress_bar.py        # 进度条
└── assets/                    # 资源文件
    ├── images/                # 图片资源
    ├── audio/                 # 音频资源
    └── fonts/                 # 字体资源
```

## 技术规范

- 代码符合 PEP 8 规范
- Python 3.8+
- Pygame 2.0+
- 面向对象设计
- 模块化分层架构
- 异常处理机制

## 已知问题与未来计划

- 暂无实际美术资源，使用占位图形
- 音效系统框架已搭建，但需要实际音频文件
- 计划添加更多植物类型（寒冰射手、樱桃炸弹等）
- 计划添加更多僵尸类型（铁桶僵尸、橄榄球僵尸等）
- 计划添加更多关卡和地图

## License

仅供学习交流使用。
