# ── Skill 定义模板 ──
# name: 技能名称（小写，短横线分隔）
# description: 简短描述（用于技能列表）
# trigger: 触发条件（可选）
# version: 版本号
# author: 作者
# created: 创建日期
# updated: 更新日期

name: my-first-skill
description: "我的第一个自定义技能"
trigger: "用户说 '帮我做 X' 时自动加载"
version: "1.0.0"
author: "your-name"
created: "2026-04-08"

---

# My First Skill

这是技能的完整说明文档。当用户触发此技能时，这段内容会被注入到对话中。

## 适用场景

- 场景 1
- 场景 2

## 步骤流程

1. 第一步：...
2. 第二步：...
3. ...

## 注意事项

- 需要的环境变量：`EXAMPLE_API_KEY`
- 前置条件：...

## 示例对话

```
用户: 帮我做 X
助手: [执行技能步骤]
```

---

# 技能目录结构

```
my-first-skill/
├── SKILL.md           # 此文件（必需）
├── references/        # 参考文档（可选）
│   └── api-docs.md
├── templates/         # 模板文件（可选）
│   └── config.yaml
├── scripts/           # 执行脚本（可选）
│   └── helper.py
└── assets/            # 静态资源（可选）
    └── diagram.png
```

## 相关技能

- `related-skill-a`
- `related-skill-b`