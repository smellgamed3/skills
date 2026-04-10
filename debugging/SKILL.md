---
name: debugging
description: Use when troubleshooting bugs, investigating unexpected behavior, or diagnosing system issues. Covers systematic debugging approaches, tools, techniques, and strategies for efficient problem-solving.
---

# Debugging

## Overview

Debugging is the systematic process of identifying and resolving defects or problems in software. This skill provides guidance for effective debugging strategies and tools.

**Core principle:** Understand the problem before fixing it - systematic diagnosis leads to lasting solutions, not quick patches.

## When to Use

```
Need to debug an issue?
│
├─ Error message visible?
│  └─ Read error, search for similar issues
│
├─ Unexpected behavior?
│  └─ Add logging, reproduce issue
│
├─ Performance problem?
│  └─ Profile code, identify bottlenecks
│
├─ Intermittent failure?
│  └─ Check race conditions, timing issues
│
└─ Production issue?
   └─ Check logs, metrics, rollback changes
```

**Use this skill when:**
- Investigating bugs or errors
- Troubleshooting unexpected behavior
- Analyzing performance issues
- Debugging production problems
- Learning unfamiliar codebases

**When NOT to use:**
- For feature development (use TDD)
- When problem is clearly documented (follow docs)

## Quick Reference

### Debugging Levels

| Level | Approach | When |
|-------|----------|------|
| **Logging** | Add print/log statements | Quick investigation |
| **Debugger** | Step through code | Complex logic |
| **Profiler** | Measure performance | Slow code |
| **Rubber duck** | Explain to someone else | Conceptual issues |

### Common Tools

| Tool | Language | Use Case |
|------|----------|----------|
| print/logging | All | Quick debugging |
| pdb/ipdb | Python | Interactive debugging |
| debugger | Node.js | JavaScript debugging |
| gdb | C/C++ | Low-level debugging |
| Chrome DevTools | Browser | Frontend debugging |

## Systematic Debugging Process

### 1. Understand the Problem

```bash
# Ask questions:
- What is the expected behavior?
- What is actually happening?
- What error messages appear?
- When does this occur?
- Can I reproduce this reliably?
```

### 2. Reproduce the Issue

```python
# Create minimal reproduction
def reproduce_bug():
    # Setup minimal state
    data = {"key": "value"}

    # Execute code that triggers bug
    result = process_data(data)

    # Verify bug occurs
    assert result == expected, f"Bug: got {result}"
```

### 3. Form Hypothesis

```bash
# Possible causes:
- Variable has wrong value
- Function returns unexpected result
- API call fails silently
- Race condition in async code
- Missing error handling
```

### 4. Test Hypothesis

```python
# Add logging to test hypothesis
def process_data(data):
    logger.debug(f"Input: {data}")  # Log input
    result = transform(data)
    logger.debug(f"Output: {result}")  # Log output
    return result
```

### 5. Fix and Verify

```bash
# After fix:
- Run tests to ensure fix works
- Check for regressions
- Add test case for this bug
- Document the issue and solution
```

## Debugging Techniques

### Binary Search Debugging

```python
# Narrow down problem location
def complex_function(data):
    # Add checkpoint 1
    print("Checkpoint 1: data =", data)

    result1 = step1(data)
    print("Checkpoint 2: result1 =", result1)

    result2 = step2(result1)
    print("Checkpoint 3: result2 =", result2)

    return step3(result2)
```

### Rubber Duck Debugging

```
1. Get a rubber duck (or imaginary listener)
2. Explain your code line by line
3. Describe what you expect at each step
4. Compare with what actually happens
5. Often the problem becomes obvious during explanation
```

### Minimal Reproduction

```python
# Start with complex code that fails
def complex_bug():
    # 1000 lines of code...
    pass

# Reduce to minimal case
def minimal_reproduction():
    input_data = {"key": "value"}  # Minimal input
    result = process(input_data)  # Single function
    assert result == "expected"  # Fails
```

## Language-Specific Tools

### Python Debugging

**Using pdb:**
```python
import pdb

def buggy_function(x, y):
    result = x + y
    pdb.set_trace()  # Breakpoint here
    result = result / 0  # Bug
    return result

# Or use from command line
python -m pdb script.py
```

**Common pdb commands:**
```
n(ext)    - Execute next line
s(tep)    - Step into function
c(ontinue) - Continue to next breakpoint
p(rint)   - Print variable
l(ist)    - Show code context
w(here)   - Show stack trace
q(uit)    - Quit debugger
```

**Using ipdb (enhanced pdb):**
```bash
pip install ipdb

# In code
import ipdb; ipdb.set_trace()

# Or use as default debugger
export PYTHONBREAKPOINT=ipdb.set_trace
```

### Node.js Debugging

**Using debugger:**
```javascript
function buggyFunction(x, y) {
    const result = x + y;
    debugger;  // Breakpoint here
    return result / 0;
}
```

**Using Chrome DevTools:**
```bash
# Run with inspect flag
node --inspect script.js

# Or with break on start
node --inspect-brk script.js

# Open Chrome DevTools
# chrome://inspect
```

**Using ndb (improved CLI debugger):**
```bash
npm install -g ndb
ndb script.js
```

### Browser Debugging

**Chrome DevTools:**
```javascript
// Console debugging
console.log('Variable value:', variable);
console.error('Error:', error);
console.table(objectArray);

// Performance timing
console.time('operation');
// ... code ...
console.timeEnd('operation');

// Assert conditions
console.assert(condition, 'Condition failed!');
```

## Common Bug Patterns

### Off-by-One Errors

```python
# ❌ Wrong
for i in range(len(array) - 1):  # Misses last element
    print(array[i])

# ✅ Correct
for i in range(len(array)):
    print(array[i])
```

### Null/Undefined Reference

```javascript
// ❌ Wrong
function getUserEmail(user) {
    return user.email;  // Crashes if user is null
}

// ✅ Correct
function getUserEmail(user) {
    return user?.email ?? '';  // Safe navigation
}
```

### Race Conditions

```python
# ❌ Wrong: Check-then-act
if user.is_admin:
    grant_access()  # User might change between check and action

# ✅ Correct: Atomic operation
grant_access_if_admin(user)
```

### Memory Leaks

```javascript
// ❌ Wrong: Never clears cache
const cache = {};
function memoize(key, value) {
    cache[key] = value;
}

// ✅ Correct: Limits cache size
const cache = new Map();
function memoize(key, value) {
    if (cache.size > 1000) {
        const firstKey = cache.keys().next().value;
        cache.delete(firstKey);
    }
    cache.set(key, value);
}
```

## Logging Best Practices

### Log Levels

```python
import logging

logging.basicConfig(level=logging.DEBUG)

logger.debug("Detailed diagnostic information")  # For debugging
logger.info("General informational messages")    # Normal operation
logger.warning("Warning about potential issues") # Something unexpected
logger.error("Error occurred")                   # Error in operation
logger.critical("Critical system failure")       # Serious problem
```

### Structured Logging

```python
import json
import logging

def log_structured(level, message, **kwargs):
    log_data = {
        "message": message,
        "level": level,
        **kwargs
    }
    logger.log(level, json.dumps(log_data))

# Usage
log_structured(
    logging.INFO,
    "User logged in",
    user_id=123,
    ip="192.168.1.1",
    timestamp=time.time()
)
```

### Contextual Logging

```python
# ❌ Bad: No context
logger.error("Error occurred")

# ✅ Good: Full context
logger.error(
    "Failed to process payment",
    extra={
        "user_id": user.id,
        "amount": amount,
        "error": str(e),
        "traceback": traceback.format_exc()
    }
)
```

## Performance Debugging

### Profiling Python

```python
import cProfile

def profile_code():
    pr = cProfile.Profile()
    pr.enable()

    # Code to profile
    your_function()

    pr.disable()
    pr.print_stats(sort='cumulative')

profile_code()
```

### Profiling Node.js

```javascript
const profiler = require('v8-profiler-node8');

profiler.startProfiling('profile', true);
// Your code here
const profile = profiler.stopProfiling('profile');
profile.export((error, result) => {
    fs.writeFileSync('./profile.cpuprofile', result);
    profiler.deleteProfile(profile);
});
```

### Memory Profiling

```python
# Check memory usage
import psutil
import os

process = psutil.Process(os.getpid())
print(f"Memory: {process.memory_info().rss / 1024 / 1024} MB")

# Track memory leaks
import tracemalloc
tracemalloc.start()

# Your code here

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
```

## Production Debugging

### Log Analysis

```bash
# Search for errors
grep "ERROR" /var/log/app.log

# Find specific time range
grep "2024-01-01 10:" /var/log/app.log

# Count occurrences
grep -c "ERROR" /var/log/app.log

# Follow logs in real-time
tail -f /var/log/app.log
```

### Health Checks

```python
@app.route('/health')
def health_check():
    checks = {
        'database': check_database(),
        'redis': check_redis(),
        'api': check_external_api()
    }

    if all(checks.values()):
        return jsonify({'status': 'healthy'}), 200
    else:
        return jsonify({
            'status': 'unhealthy',
            'checks': checks
        }), 503
```

### Rollback Strategy

```bash
# Quick rollback steps
1. Identify bad commit
2. Revert commit
3. Deploy previous version
4. Verify fix
5. Investigate root cause post-mortem
```

## Debugging Checklist

### Before Debugging

- [ ] Can I reproduce the issue reliably?
- [ ] Do I understand the expected behavior?
- [ ] Do I have error messages or stack traces?
- [ ] Are there recent changes that could cause this?
- [ ] Can I create a minimal reproduction?

### During Debugging

- [ ] Have I formed a hypothesis?
- [ ] Am I testing one hypothesis at a time?
- [ ] Am I documenting my findings?
- [ ] Am I using appropriate tools?
- [ ] Am I checking assumptions?

### After Debugging

- [ ] Did I fix the root cause?
- [ ] Did I add tests for this bug?
- [ ] Did I document the issue?
- [ ] Did I check for similar issues?
- [ ] Can I prevent this class of bugs?

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Fixing without understanding | Investigate root cause first |
| Changing too many things | Change one thing at a time |
| Not reproducing locally | Add more logging |
| Ignoring error messages | Read and understand errors |
| Premature optimization | Profile before optimizing |

## Tools and Resources

### Debugging Tools

- **Visual Studio Code**: Built-in debugger for many languages
- **Chrome DevTools**: Browser debugging
- **GDB**: C/C++ debugging
- **Valgrind**: Memory leak detection
- **Wireshark**: Network debugging

### Monitoring Tools

- **Sentry**: Error tracking
- **Datadog**: APM and monitoring
- **Prometheus**: Metrics collection
- **Grafana**: Visualization

## Resources

- **Debugging Rules**: https://www.youtube.com/watch?v=6o9v6yQgY-Q
- **Python Debugging**: https://docs.python.org/3/library/pdb.html
- **Chrome DevTools**: https://developers.google.com/web/tools/chrome-devtools

**Remember:** Debugging is a skill that improves with practice. Stay calm, be systematic, and document your findings. The best fix is understanding the root cause, not just patching symptoms.
