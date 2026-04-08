# Hermes Agent 示例配置

本目录包含 Hermes Agent 的示例配置文件，供橙皮书读者参考。

## 文件说明

| 文件 | 用途 | 适用场景 |
|-----|------|---------|
| `config.minimal.yaml` | 最简配置 | 首次安装、快速体验 |
| `config.developer.yaml` | 开发者配置 | 代码开发、自动化任务 |
| `config.gateway.yaml` | Gateway 配置 | Telegram/Discord/Slack 部署 |
| `.env.example` | 环境变量模板 | 所有 API Key 配置参考 |

## 使用方法

### 1. 复制配置文件

```bash
# 创建 Hermes 配置目录
mkdir -p ~/.hermes

# 复制配置（选择一个）
cp config.minimal.yaml ~/.hermes/config.yaml
# 或
cp config.developer.yaml ~/.hermes/config.yaml
# 或
cp config.gateway.yaml ~/.hermes/config.yaml

# 复制环境变量模板
cp .env.example ~/.hermes/.env
```

### 2. 编辑 .env 文件

```bash
# 用编辑器打开
nano ~/.hermes/.env

# 至少配置一个 Provider API Key
# 例如：OPENROUTER_API_KEY="sk-or-..."
```

### 3. 运行 Setup Wizard

```bash
hermes setup
```

Wizard 会检测你的配置并引导完成剩余设置。

## Skills 示例

`skills/` 目录包含一个技能模板：

```bash
# 复制到你的 Skills 目录
cp -r skills/my-first-skill ~/.hermes/skills/

# 编辑 SKILL.md 定义你自己的技能
nano ~/.hermes/skills/my-first-skill/SKILL.md
```

## 配置层级

Hermes 配置采用三层合并：

1. **默认配置** (`DEFAULT_CONFIG` in code) — 内置默认值
2. **用户配置** (`~/.hermes/config.yaml`) — 用户覆盖
3. **环境变量** (`~/.hermes/.env`) — 密钥和敏感值

合并顺序：默认 < config.yaml < .env（后者覆盖前者）

## Profile 多配置

Hermes 支持多个 Profile（配置切换）：

```bash
# 创建 Profile
hermes profile create coder

# 使用 Profile 运行
hermes -p coder

# Profile 配置目录
~/.hermes/profiles/coder/config.yaml
~/.hermes/profiles/coder/.env
```

## 官方文档

- Hermes 官方文档: https://hermes-agent.nousresearch.com/docs/
- 橙皮书下载: https://github.com/alchaincyf/hermes-agent-orange-book
- 花叔主页: https://huasheng.ai/

## 更新日志

- v0.7.0 示例（2026-04-08）—— 首版发布