---
name: code-review
description: Use when reviewing pull requests, providing feedback on code changes, or conducting quality assurance checks. Covers review checklist, best practices, common issues to catch, and effective feedback techniques.
---

# Code Review

## Overview

Code review is systematic examination of source code to find mistakes overlooked in initial development. This skill provides guidance for effective code review practices and common issues to identify.

**Core principle:** Review the code change, not the coder - focus on improving code quality and sharing knowledge, not criticizing individuals.

## When to Use

```
Need to review code changes?
│
├─ New feature implementation?
│  └─ Check logic, edge cases, and requirements
│
├─ Bug fix submitted?
│  └─ Verify fix addresses root cause
│
├─ Refactoring proposed?
│  └─ Ensure behavior preserved
│
├─ Performance concerns?
│  └─ Analyze complexity and resource usage
│
└─ Security implications?
   └─ Check vulnerabilities and best practices
```

**Use this skill when:**
- Reviewing pull requests
- Providing code feedback
- Conducting quality checks
- Onboarding team members
- Establishing coding standards

**When NOT to use:**
- For trivial changes (typos, formatting)
- During emergency hotfixes (review after)
- For style preferences (use linters)

## Quick Reference

### Review Priorities

| Priority | Focus | Time Spent |
|----------|-------|------------|
| **Critical** | Security, bugs, breaking changes | 50% |
| **High** | Performance, error handling | 30% |
| **Medium** | Code clarity, maintainability | 15% |
| **Low** | Style, formatting | 5% |

### Common Issues to Catch

| Category | Issues |
|----------|--------|
| **Logic** | Off-by-one, null handling, race conditions |
| **Security** | Injection, exposed secrets, auth issues |
| **Performance** | N+1 queries, missing indexes, large loops |
| **Error Handling** | Uncaught exceptions, silent failures |
| **Testing** | Missing edge cases, insufficient coverage |

## Review Checklist

### Functionality

- [ ] **Requirements met**: Does code implement what was requested?
- [ ] **Edge cases**: Handles empty/null/invalid inputs?
- [ ] **Error handling**: Proper error messages and recovery?
- [ ] **Backward compatibility**: Breaking changes documented?

### Code Quality

- [ ] **Readability**: Clear variable names and logic flow?
- [ ] **Simplicity**: Could this be simpler?
- [ ] **DRY principle**: No duplicated code?
- [ ] **Functions**: Single responsibility, appropriate size?

### Architecture

- [ ] **Separation of concerns**: Logic in right layer?
- [ ] **Coupling**: Minimal dependencies between components?
- [ ] **Cohesion**: Related code grouped together?
- [ ] **Patterns**: Appropriate design patterns used?

### Security

- [ ] **Input validation**: User input sanitized?
- [ ] **Authentication**: Proper auth checks?
- [ ] **Authorization**: User can only access allowed resources?
- [ ] **Secrets**: No hardcoded credentials or API keys?
- [ ] **SQL Injection**: Parameterized queries used?
- [ ] **XSS**: Output properly escaped?

### Performance

- [ ] **Database**: N+1 queries avoided?
- [ ] **Caching**: Appropriate caching strategy?
- [ ] **Complexity**: Acceptable time/space complexity?
- [ ] **Resources**: Memory/network usage efficient?

### Testing

- [ ] **Unit tests**: Core logic covered?
- [ ] **Integration tests**: API endpoints tested?
- [ ] **Edge cases**: Boundary conditions tested?
- [ ] **Tests pass**: All tests passing?

### Documentation

- [ ] **Comments**: Complex logic explained?
- [ ] **API docs**: Endpoints documented?
- [ ] **README**: Setup/usage instructions?
- [ ] **Changelog**: Changes documented?

## Common Issues to Identify

### Logic Errors

**Off-by-one errors:**
```javascript
// ❌ Wrong: Excludes last element
for (let i = 0; i < array.length - 1; i++) {
  console.log(array[i]);
}

// ✅ Correct: Include last element
for (let i = 0; i < array.length; i++) {
  console.log(array[i]);
}
```

**Null reference:**
```javascript
// ❌ Wrong: No null check
function getUserEmail(user) {
  return user.email;
}

// ✅ Correct: Handle null
function getUserEmail(user) {
  return user?.email ?? '';
}
```

**Race conditions:**
```python
# ❌ Wrong: Check-then-act race condition
if user.is_admin:
    user.delete()  # User might have changed

# ✅ Correct: Atomic operation
user.delete_if_admin()
```

### Security Issues

**SQL Injection:**
```javascript
// ❌ Wrong: String concatenation
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ Correct: Parameterized query
const query = 'SELECT * FROM users WHERE id = ?';
db.execute(query, [userId]);
```

**Hardcoded secrets:**
```javascript
// ❌ Wrong: Exposed API key
const API_KEY = 'sk_live_abc123...';

// ✅ Correct: Environment variable
const API_KEY = process.env.API_KEY;
```

**Missing auth check:**
```python
# ❌ Wrong: No authentication
@app.route('/admin/delete')
def delete_user():
    user_id = request.args.get('id')
    delete_user(user_id)

# ✅ Correct: Check authentication
@app.route('/admin/delete')
@login_required
@admin_required
def delete_user():
    user_id = request.args.get('id')
    delete_user(user_id)
```

### Performance Issues

**N+1 queries:**
```python
# ❌ Wrong: Query in loop
users = User.all()
for user in users:
    posts = user.posts.all()  # N queries

# ✅ Correct: Eager loading
users = User.include('posts').all()
```

**Inefficient algorithm:**
```javascript
// ❌ Wrong: O(n²) complexity
function hasDuplicates(arr) {
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j]) return true;
    }
  }
  return false;
}

// ✅ Correct: O(n) complexity
function hasDuplicates(arr) {
  return new Set(arr).size !== arr.length;
}
```

### Error Handling

**Silent failures:**
```python
# ❌ Wrong: Swallows all errors
try:
    process_data()
except:
    pass

# ✅ Correct: Handle specific errors
try:
    process_data()
except ValueError as e:
    logger.error(f"Invalid data: {e}")
    raise
```

**Generic exceptions:**
```javascript
// ❌ Wrong: Generic error
throw new Error("Something went wrong");

// ✅ Correct: Specific error
throw new ValidationError("Email is required");
```

## Review Process

### 1. Initial Assessment (5 minutes)

- Read the PR description
- Understand the problem being solved
- Check the size of the change
- Identify critical areas to focus on

### 2. Code Walkthrough (15-30 minutes)

- Read through the code diff
- Run tests locally
- Check edge cases
- Verify the solution works

### 3. Detailed Review (30-60 minutes)

- Go through checklist above
- Mark issues with line numbers
- Suggest improvements
- Ask clarifying questions

### 4. Provide Feedback

Start with positives, then address issues:

```markdown
## Great work!

I like how you:
- ✅ Separated business logic from controllers
- ✅ Added comprehensive tests
- ✅ Updated documentation

## Suggestions

### Critical (must fix)
1. **Security**: Line 45 - SQL injection vulnerability. Use parameterized queries.
2. **Error handling**: Line 78 - Missing error handling for network requests.

### Important (should fix)
3. **Performance**: Lines 120-125 - N+1 query issue. Consider eager loading.
4. **Testing**: Missing test case for empty input.

### Nice to have
5. **Code clarity**: Line 92 - Variable name `x` is unclear. Consider `userIndex`.
6. **Documentation**: Add docstring explaining the algorithm.

## Questions
- Why did you choose this approach over [alternative]?
- Have you tested with [edge case]?

Overall, this is good work. Once the critical issues are addressed, I'm happy to approve. 🚀
```

## Effective Feedback Techniques

### BE Constructive

❌ **Bad:**
```
This code is terrible. Rewrite it.
```

✅ **Good:**
```
I'm having trouble understanding this function. Could we:
1. Add a docstring explaining what it does?
2. Break it into smaller functions?
3. Use more descriptive variable names?
```

### BE Specific

❌ **Bad:**
```
Fix the bugs.
```

✅ **Good:**
```
Line 42: Null reference error when `user` is undefined.
Consider: `user?.email ?? ''`
```

### BE Actionable

❌ **Bad:**
```
Improve performance.
```

✅ **Good:**
```
Lines 120-125: This loop is O(n²). For 1000 items, that's 1M operations.
Suggestion: Use a Set for O(1) lookups, reducing to O(n).
```

### Explain Why

❌ **Bad:**
```
Don't use var.
```

✅ **Good:**
```
Line 10: Avoid `var` because it's function-scoped and can lead to bugs.
Use `const` for immutable values, `let` for mutable ones.
```

## Review Metrics

### Quality Indicators

**Good review:**
- Identifies 2-5 critical issues
- Explains reasoning for suggestions
- Provides actionable feedback
- Maintains positive tone
- Responds to clarification questions

**Poor review:**
- Focuses on style over substance
- Uses vague language ("fix this")
- Doesn't explain why changes are needed
- Creates hostile atmosphere
- Blocks PR without clear reason

### Time Spent

| PR Size | Review Time |
|---------|-------------|
| Small (<100 lines) | 15-30 minutes |
| Medium (100-500 lines) | 30-60 minutes |
| Large (500+ lines) | 60+ minutes or split up |

**Tip:** Request PRs be split if too large to review effectively.

## Before Approving

### Final Checks

- [ ] All tests passing
- [ ] Critical issues addressed
- [ ] Documentation updated
- [ ] No regressions introduced
- [ ] Code follows team standards
- [ ] Questions answered

### Approval Options

```markdown
## Approve with changes
Address the critical issues, then I'll approve.

## Approve
Looks good! No changes needed.

## Request changes
Please address these issues before merging.

## Comment
I have questions but don't block merging.
```

## Common Mistakes in Reviews

| Mistake | Impact | Fix |
|---------|--------|-----|
| Focus on style | Wastes time | Use linters/formatters |
| Late feedback | Delays shipping | Review early and often |
| Vague feedback | Causes confusion | Be specific with examples |
| Nitpicking | Demotivates authors | Focus on important issues |
| Rubber stamping | Bugs slip through | Take time to review properly |

## Self-Review Checklist

Before requesting review, authors should:

- [ ] Run all tests locally
- [ ] Check for common issues (linter, security scanner)
- [ ] Add/update tests for new code
- [ ] Update documentation
- [ ] Write clear PR description
- [ ] Self-review the diff
- [ ] Keep PR size manageable

## Tools and Automation

### Automated Checks

```bash
# Linting
npm run lint
flake8 ./src

# Type checking
npm run type-check
mypy ./src

# Security scanning
npm audit
safety check

# Test coverage
npm run test:coverage
pytest --cov=src
```

### Review Tools

- **GitHub/GitLab**: Built-in review features
- **SonarQube**: Automated code quality analysis
- **CodeClimate**: Automated review and tracking
- **LGTM**: Security vulnerability scanning

## Resources

- **Google Code Review Guide**: https://google.github.io/eng-practices/review/
- **Effective Code Review**: https://mtlynch.io/code-review/
- **Pull Request Best Practices**: https://github.blog/2019-04-09-pull-requests-and-the-developer-experience/

**Remember:** The goal of code review is to improve code quality and share knowledge. Be kind, be specific, and focus on what matters most.
