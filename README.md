# Skills Collection

My collection of useful Claude Code skills for efficient software development workflows.

## What are Skills?

Skills are reference guides for proven techniques, patterns, or tools that help Claude Code instances work more effectively. Each skill provides actionable guidance for specific development tasks.

## Available Skills

### Development Workflows

#### git-workflow
Git version control best practices and workflows.

**Features:**
- Feature branch workflow
- Commit conventions
- Merge vs rebase strategies
- Conflict resolution
- Branching strategies

**Use when:** Working with Git, branching, merging, or managing version control.

---

#### docker-dev
Docker container development and management.

**Features:**
- Dockerfile creation and optimization
- Docker Compose for multi-service apps
- Development vs production setups
- Container debugging
- Security best practices

**Use when:** Building images, running containers, or setting up containerized environments.

---

### Testing & Quality

#### api-testing
REST API testing and debugging techniques.

**Features:**
- curl commands and patterns
- Authentication methods (Bearer, OAuth, API keys)
- Postman workflows
- Automated testing
- Performance testing

**Use when:** Testing APIs, debugging HTTP requests, or validating endpoints.

---

#### code-review
Code review checklist and best practices.

**Features:**
- Comprehensive review checklist
- Common issues to identify
- Effective feedback techniques
- Security and performance checks
- Review metrics and standards

**Use when:** Reviewing pull requests, providing code feedback, or conducting quality checks.

---

#### debugging
Systematic debugging strategies and tools.

**Features:**
- Debugging process and techniques
- Language-specific tools (Python, Node.js, Browser)
- Common bug patterns
- Performance profiling
- Production debugging

**Use when:** Troubleshooting bugs, investigating issues, or diagnosing problems.

---

### Integration & Automation

#### outline-cli
Outline API interaction for knowledge base management.

**Features:**
- Document CRUD operations
- Collection management
- Search functionality
- Authentication (API Key + OAuth)
- Self-hosted instance support

**Use when:** Creating, reading, updating, or deleting Outline documents and collections.

## Installation

Each skill can be installed by creating a symbolic link to your Claude skills directory:

```bash
# Install a skill
ln -s ~/skills/skill-name/SKILL.md ~/.claude/skills/skill-name-SKILL.md

# Verify installation
ls -lh ~/.claude/skills/skill-name-SKILL.md
```

### Install All Skills

```bash
# Create symlinks for all skills
for skill in ~/skills/*/SKILL.md; do
  name=$(basename $(dirname $skill))
  ln -sf $skill ~/.claude/skills/${name}-SKILL.md
done
```

## Usage

### In Claude Code

Simply describe your task, and Claude will automatically load the relevant skill:

```
"帮我创建一个新分支并推送到远程"
"如何在 Docker 中运行多服务应用？"
"测试这个 API 端点"
"审查这个 pull request"
"这个 bug 怎么调试？"
```

### Direct Access

You can also read skill files directly:

```bash
# View skill content
cat ~/skills/git-workflow/SKILL.md

# Or open in your editor
code ~/skills/docker-dev/SKILL.md
```

## Maintenance

### Adding New Skills

```bash
cd ~/skills

# Create new skill directory
mkdir -p your-skill-name

# Create SKILL.md with proper frontmatter
cat > your-skill-name/SKILL.md << 'END'
---
name: your-skill-name
description: Use when [specific triggering conditions]
---

# Your Skill Name

## Overview
[Brief description in 1-2 sentences]

## When to Use
[Describe when to use this skill]

## Quick Reference
[Quick reference table or list]
END

# Commit and push
git add your-skill-name/SKILL.md
git commit -m "Add your-skill-name skill"
git push
```

### Updating Existing Skills

```bash
cd ~/skills

# Edit skill file
vim your-skill-name/SKILL.md

# Commit changes
git add your-skill-name/SKILL.md
git commit -m "Update your-skill-name: describe changes"
git push
```

## Skill Structure

Each skill follows this structure:

```
skill-name/
└── SKILL.md
    ├── Frontmatter (name, description)
    ├── Overview
    ├── When to Use (with flowchart if needed)
    ├── Quick Reference
    ├── Implementation Details
    ├── Common Mistakes
    └── Resources
```

## Contributing

Found a bug or have a suggestion? Feel free to:

1. Star the repository
2. Open an issue
3. Suggest improvements
4. Fork and customize

## Statistics

- **Total Skills**: 6
- **Categories**: Development, Testing, Integration
- **Total Content**: ~3,000 lines
- **Languages**: Multi-language support

## License

MIT License - Feel free to use and modify for your needs.

## Links

- **GitHub Repository**: https://github.com/smellgamed3/skills
- **Claude Code**: https://claude.ai/code
- **Issue Tracker**: https://github.com/smellgamed3/skills/issues

---

**Last updated**: 2026-04-11
**Maintainer**: smellgamed3
