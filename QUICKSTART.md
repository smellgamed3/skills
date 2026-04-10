# Skills 快速使用指南

## 📦 仓库信息

- **仓库地址**: https://github.com/smellgamed3/skills
- **本地路径**: `~/skills`
- **许可证**: MIT License

## 🚀 快速开始

### 1. 添加新的 Skill

```bash
cd ~/skills

# 创建新的 skill 目录
mkdir -p your-skill-name

# 创建 SKILL.md 文件
cat > your-skill-name/SKILL.md << 'EOF'
---
name: your-skill-name
description: Use when [具体触发条件]
---

# Your Skill Name

## Overview
[简短描述 1-2 句话]

## When to Use
[使用场景说明]

## Quick Reference
[快速参考表格]

## Implementation
[实现细节]
EOF

# 提交到仓库
git add your-skill-name/SKILL.md
git commit -m "Add your-skill-name skill"
git push
```

### 2. 安装 Skill 到 Claude Code

```bash
# 创建符号链接
ln -s ~/skills/your-skill-name/SKILL.md ~/.claude/skills/your-skill-name-SKILL.md

# 验证安装
ls -lh ~/.claude/skills/your-skill-name-SKILL.md
```

### 3. 使用 Skill

在 Claude Code 中直接描述你的需求，Claude 会自动加载相关的 skill：

```
"帮我创建一个 Outline 文档"
"搜索包含 API 的文档"
"列出所有集合"
```

## 📁 当前可用的 Skills

### outline-cli ✅

**功能**: Outline API 交互指南

**特性**:
- 文档 CRUD 操作
- 集合管理
- 搜索功能
- 认证（API Key + OAuth）
- 错误处理和安全最佳实践

**使用示例**:
```bash
# 通过 CLI 工具
outline collections
outline search "关键词"
outline create "标题" -c "内容"

# 通过 API 调用
curl https://app.getoutline.com/api/documents.list \
  -X 'POST' \
  -H 'authorization: Bearer YOUR_API_KEY' \
  -H 'content-type: application/json' \
  -d '{"limit": 50}'
```

## 🛠️ 维护工作流

### 更新现有 Skill

```bash
cd ~/skills

# 编辑 skill 文件
vim outline-cli/SKILL.md

# 提交更改
git add outline-cli/SKILL.md
git commit -m "Update outline-cli skill: add new feature"
git push
```

### 批量更新

```bash
cd ~/skills

# 查看修改状态
git status

# 添加所有更改
git add -A

# 提交更改
git commit -m "Batch update skills"

# 推送到 GitHub
git push
```

### 同步到其他机器

```bash
# 克隆仓库
git clone https://github.com/smellgamed3/skills.git ~/skills

# 或者如果已存在，拉取最新更改
cd ~/skills
git pull
```

## 📋 Skill 创建检查清单

创建新 skill 时，确保包含以下内容：

### ✅ 必需项

- [ ] Frontmatter（name, description）
- [ ] Description 以 "Use when..." 开头
- [ ] Description 使用第三人称
- [ ] 清晰的概述（Overview）
- [ ] 使用场景说明（When to Use）

### ✅ 推荐项

- [ ] 快速参考表格（Quick Reference）
- [ ] 实现代码示例
- [ ] 常见错误说明（Common Mistakes）
- [ ] 最佳实践说明

### ✅ 质量检查

- [ ] 字数控制在合理范围（reference skills < 500 词）
- [ ] 包含搜索关键词
- [ ] 代码示例完整可运行
- [ ] 没有叙事性内容

## 🔍 有用的 Git 命令

```bash
# 查看仓库状态
git status

# 查看提交历史
git log --oneline

# 查看远程仓库
git remote -v

# 创建新分支
git checkout -b feature/new-skill

# 合并分支
git merge feature/new-skill

# 查看文件变更
git diff

# 撤销未提交的更改
git checkout -- filename

# 查看最近的提交
git log -1 --stat
```

## 📚 资源链接

- **Claude Code 文档**: https://claude.ai/code
- **Skill 规范**: https://agentskills.io/specification
- **GitHub 仓库**: https://github.com/smellgamed3/skills

## 🤝 贡献指南

如果你觉得某个 skill 对你有帮助，欢迎：

1. ⭐ 给仓库点星
2. 🍴 Fork 并改进
3. 🐛 提交 Issue 报告问题
4. 💡 提出改进建议

## 📝 更新日志

### 2026-04-11
- ✅ 创建仓库
- ✅ 添加 outline-cli skill
- ✅ 添加 MIT License
- ✅ 配置 .gitignore

---

**最后更新**: 2026-04-11
**维护者**: smellgamed3
