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

#### 方式一：使用启动脚本（推荐）

项目提供了跨平台启动脚本，自动检测环境、验证依赖并启动游戏。

**Windows 系统：**

```cmd
:: 默认配置启动
start.bat

:: 全屏模式启动
start.bat --fullscreen

:: 自定义分辨率和帧率
start.bat --width 1280 --height 720 --fps 30

:: 禁用音频 + 调试模式
start.bat --no-audio --debug

:: 查看帮助
start.bat --help

:: 停止游戏（正常退出）
stop.bat

:: 强制停止游戏（立即终止）
stop.bat --force
```

**Linux / macOS 系统：**

```bash
# 首次使用需添加执行权限
chmod +x start.sh stop.sh

# 默认配置启动
./start.sh

# 全屏模式启动
./start.sh --fullscreen

# 自定义分辨率和帧率
./start.sh --width 1280 --height 720 --fps 30

# 禁用音频 + 调试模式
./start.sh --no-audio --debug

# 查看帮助
./start.sh --help

# 停止游戏（正常退出，发送 SIGTERM）
./stop.sh

# 强制停止游戏（立即终止，发送 SIGKILL）
./stop.sh --force
```

#### 方式二：直接使用 Python

```bash
python main.py [选项]
```

### 启动参数说明

| 参数 | 缩写 | 说明 | 默认值 |
|------|------|------|--------|
| `--fullscreen` | `-f` | 以全屏模式启动 | 窗口模式 |
| `--fps <数值>` | - | 设置目标帧率 | 60 |
| `--width <数值>` | - | 设置窗口宽度（像素） | 900 |
| `--height <数值>` | - | 设置窗口高度（像素） | 600 |
| `--bgm-volume <数值>` | - | 背景音乐音量（0.0-1.0） | 0.5 |
| `--sfx-volume <数值>` | - | 音效音量（0.0-1.0） | 0.7 |
| `--no-audio` | - | 禁用所有音频 | 音频开启 |
| `--debug` | - | 启用调试模式，输出详细日志 | 调试关闭 |
| `--help` | `-h` | 显示帮助信息 | - |

### 启动脚本功能说明

两个启动脚本（`start.bat` / `start.sh`）功能完全对等，执行以下检查流程：

1. **环境检测** — 检测 Python 是否安装、版本是否 ≥ 3.8
2. **文件完整性检查** — 验证 `main.py`、`game_core/`、`res/`、`scene/`、`sprites/` 等核心文件是否存在
3. **依赖验证** — 检查 pygame 是否已安装，缺失时自动安装
4. **虚拟环境检测** — 检测是否在虚拟环境中运行，未使用时给出建议
5. **参数解析** — 解析命令行参数并传递给游戏
6. **启动游戏** — 执行 `python main.py` 并传递参数
7. **日志记录** — 全程记录到 `game_launch.log` 文件

### 停止脚本功能说明

两个停止脚本（`stop.bat` / `stop.sh`）功能完全对等：

1. **进程搜索** — 使用 `psutil` 库搜索所有运行 `main.py` 的 Python 进程
2. **自动安装依赖** — 如未安装 `psutil`，自动尝试安装
3. **基本检测模式** — 如 `psutil` 安装失败，降级为列出所有 Python 进程供用户确认
4. **优雅终止 / 强制终止** — 默认发送 `SIGTERM`（Windows 下 `taskkill`），使用 `--force` 则发送 `SIGKILL`（`taskkill /F`）
5. **日志记录** — 全程记录到 `game_launch.log` 文件

### 常见问题排查

| 问题 | 可能原因 | 解决方法 |
|------|----------|----------|
| 提示"未找到 Python" | Python 未安装或未加入 PATH | 安装 Python 3.8+ 并勾选"Add to PATH" |
| 提示"Python 版本过低" | Python 版本 < 3.8 | 升级 Python 至 3.8 或更高版本 |
| 提示"缺少 pygame 依赖" | 依赖未安装 | 运行 `pip install -r requirements.txt` |
| 游戏启动后黑屏 | 资源文件缺失 | 确认 `assets/` 目录存在，游戏会自动使用占位图形 |
| Linux 下无法运行脚本 | 缺少执行权限 | 运行 `chmod +x start.sh stop.sh` |
| Linux 下提示无图形环境 | SSH 远程连接无 X11 | 使用 `ssh -X` 启用 X11 转发，或在本地终端运行 |
| 音频无法播放 | 音频驱动或 pygame.mixer 问题 | 使用 `--no-audio` 参数禁用音频启动 |
| 游戏卡顿 | 帧率设置过高或硬件性能不足 | 使用 `--fps 30` 降低帧率 |
| 未知参数报错 | 参数格式不正确 | 使用 `--help` 查看支持的参数列表 |
| start.bat 运行出现乱码 | 脚本编码问题 | 重新下载 start.bat，确保文件编码正确 |
| start.bat 提示"不是内部或外部命令" | 命令兼容性问题 | 更新至最新版本脚本，已移除 wmic/where 等不兼容命令 |
| stop.bat 无法找到进程 | 缺少 psutil 库 | 运行 `pip install psutil` 或使用任务管理器手动结束 |
| stop.bat 无法终止进程 | 进程占用或权限不足 | 使用 `stop.bat --force` 强制终止 |

如遇其他问题，请查看 `game_launch.log` 日志文件，或使用 `--debug` 参数启动以获取详细日志。

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
├── start.bat                  # Windows 启动脚本
├── start.sh                   # Linux/macOS 启动脚本
├── stop.bat                   # Windows 停止脚本
├── stop.sh                    # Linux/macOS 停止脚本
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
