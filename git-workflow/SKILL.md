---
name: git-workflow
description: Use when working with Git version control, including branching, merging, committing, resolving conflicts, or managing Git history. Covers common workflows like feature branches, pull requests, and release management.
---

# Git Workflow

## Overview

Git is a distributed version control system. This skill provides guidance for common Git workflows, branching strategies, and best practices for team collaboration.

**Core principle:** Think before you commit - clear commit messages and atomic commits make history readable and reversible.

## When to Use

```
Need to manage code version control?
│
├─ Start new work?
│  └─ Create feature branch from main/develop
│
├─ Save work progress?
│  └─ Commit with clear message (atomic changes)
│
├─ Share work with team?
│  └─ Push branch and create pull request
│
├─ Integrate changes?
│  └─ Merge/rebase with conflict resolution
│
└─ Release software?
   └─ Tag commits and manage releases
```

**Use this skill when:**
- Starting new features or fixes
- Committing changes to version control
- Managing branches and merges
- Resolving merge conflicts
- Reviewing Git history
- Creating releases

**When NOT to use:**
- For simple file backup (use cp/rsync)
- For temporary scratch work (use git stash or worktrees)
- When project doesn't use Git

## Quick Reference

### Common Commands

| Command | Description |
|---------|-------------|
| `git status` | Show working tree status |
| `git add .` | Stage all changes |
| `git commit -m "msg"` | Commit staged changes |
| `git push` | Push commits to remote |
| `git pull` | Pull and merge remote changes |
| `git branch` | List branches |
| `git checkout -b name` | Create and switch to branch |
| `git merge branch` | Merge branch into current |
| `git log --oneline` | Show commit history |

### Branch Management

| Command | Description |
|---------|-------------|
| `git branch -a` | List all branches |
| `git branch -d branch` | Delete local branch |
| `git push origin --delete branch` | Delete remote branch |
| `git branch -m old new` | Rename branch |
| `git checkout -` | Switch to previous branch |

## Core Workflows

### Feature Branch Workflow

```bash
# 1. Start from main branch
git checkout main
git pull

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Make changes and commit
git add .
git commit -m "feat: add user authentication"

# 4. Push to remote
git push -u origin feature/your-feature-name

# 5. Create pull request (GitHub/GitLab/Bitbucket)

# 6. After merge, delete branch
git checkout main
git pull
git branch -d feature/your-feature-name
```

### Commit Conventions

Use conventional commits for clarity:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
git commit -m "feat(auth): add OAuth2 login support"
git commit -m "fix(api): resolve race condition in user fetch"
git commit -m "docs(readme): update installation instructions"
git commit -m "refactor(database): extract query builder"
```

### Merge vs Rebase

**Merge:**
```bash
git checkout main
git merge feature-branch
# Creates merge commit, preserves full history
```

**Rebase:**
```bash
git checkout feature-branch
git rebase main
# Linear history, rewrites feature branch commits
# Use for local cleanup, avoid on shared branches
```

**Rule of thumb:**
- Merge for shared branches (main, develop)
- Rebase for local feature branches before merging

## Common Operations

### Undo Changes

**Discard local changes:**
```bash
# Discard specific file
git checkout -- filename

# Discard all changes
git reset --hard HEAD
```

**Undo commits:**
```bash
# Undo last commit, keep changes
git reset --soft HEAD~1

# Undo last commit, discard changes
git reset --hard HEAD~1

# Undo specific commit (create new commit)
git revert <commit-hash>
```

### Resolve Merge Conflicts

```bash
# 1. Start merge
git merge feature-branch

# 2. If conflicts occur, identify conflicted files
git status

# 3. Edit files to resolve conflicts
# Look for: <<<<<<<, =======, >>>>>>> markers

# 4. Stage resolved files
git add <resolved-files>

# 5. Complete merge
git commit

# 6. If needed, abort merge
git merge --abort
```

### Interactive Rebase

```bash
# Clean up last 5 commits
git rebase -i HEAD~5

# Commands in editor:
# pick = use commit
# reword = edit commit message
# edit = amend commit
# squash = merge into previous commit
# drop = remove commit
```

### Stash Changes

```bash
# Save current work
git stash

# Save with message
git stash push -m "work in progress"

# List stashes
git stash list

# Apply most recent stash
git stash pop

# Apply specific stash
git stash apply stash@{1}

# Drop stash
git stash drop stash@{0}
```

## Branching Strategies

### Git Flow (Release-based)

```
main        ← Production releases
  ↑
develop     ← Integration branch
  ↑
feature/*   ← Feature branches
hotfix/*    ← Emergency fixes
release/*   ← Release preparation
```

### GitHub Flow (Simplified)

```
main        ← Always deployable
  ↑
feature/*   ← Short-lived feature branches
```

**Choose based on:**
- Team size
- Release frequency
- Deployment complexity

## Best Practices

### Commit Messages

✅ **Good:**
```
feat(auth): add JWT token refresh

- Implement automatic token refresh
- Add refresh token storage
- Update API client with retry logic

Closes #123
```

❌ **Bad:**
```
update stuff
fix bug
work
```

### Atomic Commits

✅ **Good:** One logical change per commit
```bash
git commit -m "add user model"
git commit -m "add user repository"
git commit -m "add user service"
```

❌ **Bad:** Multiple unrelated changes
```bash
git commit -m "add user and fix database and update ui"
```

### Branch Naming

Use consistent prefixes:
- `feature/` - New features
- `fix/` - Bug fixes
- `hotfix/` - Emergency production fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation updates
- `test/` - Test additions/updates

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Committing directly to main | Always use feature branches |
| Vague commit messages | Use conventional commits |
| Large commits with many changes | Make atomic commits |
| Not pulling before pushing | Always pull first to avoid conflicts |
| Ignoring .gitignore | Configure .gitignore properly |
| Committing sensitive data | Use git-secrets or pre-commit hooks |
| Force pushing to shared branches | Never force push to main/develop |

## Git Configuration

### Essential Settings

```bash
# Set your identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default branch name
git config --global init.defaultBranch main

# Set default editor
git config --global core.editor "vim"

# Enable colored output
git config --global color.ui auto

# Set pull strategy
git config --global pull.rebase false
```

### Useful Aliases

```bash
# Shorten common commands
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual 'log --graph --oneline --all'
```

## .gitignore Best Practices

```bash
# Dependencies
node_modules/
vendor/
*.egg-info/

# Build outputs
dist/
build/
*.pyc

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local

# Logs
*.log
npm-debug.log*

# Temporary
*.tmp
TEMP.md
```

## Troubleshooting

### Recover Lost Commits

```bash
# Show reflog (history of all movements)
git reflog

# Recover lost commit
git checkout <commit-hash>
git branch recovery-branch
```

### Fix Broken Repository

```bash
# Check repository health
git fsck

# Clean up unreachable objects
git gc --prune=now
```

### Handle Large Files

```bash
# Find large files
git rev-list --objects --all |
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' |
  awk '/^blob/ {print substr($0,6)}' |
  sort -n -k1 |
  tail -10

# Use Git LFS for large files
git lfs track "*.psd"
git lfs track "*.zip"
```

## Advanced Topics

### Cherry-pick Commits

```bash
# Apply specific commit from another branch
git cherry-pick <commit-hash>

# Cherry-pick multiple commits
git cherry-pick <commit1> <commit2>

# Cherry-pick without committing
git cherry-pick -n <commit-hash>
```

### Bisect for Bug Finding

```bash
# Start bisect
git bisect start

# Mark current as bad
git bisect bad

# Mark known good commit
git bisect good <commit-hash>

# Test each commit automatically
git bisect run <test-script>
```

### Worktrees for Parallel Work

```bash
# Create linked working tree
git worktree add ../feature-branch feature-branch

# List worktrees
git worktree list

# Remove worktree
git worktree remove ../feature-branch
```

## Resources

- **Git Documentation**: https://git-scm.com/doc
- **Git Handbook**: https://guides.github.com/introduction/git-handbook/
- **Conventional Commits**: https://www.conventionalcommits.org/
- **Git LFS**: https://git-lfs.github.com/

**Remember:** Git is powerful but complex. When in doubt, create a branch and experiment - you can always delete it if things go wrong.
