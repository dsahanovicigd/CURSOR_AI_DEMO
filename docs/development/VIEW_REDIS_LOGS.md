# How to View Redis Logs

Complete guide to viewing Redis logs on macOS and other platforms.

## Quick Commands

### View Redis Logs (macOS with Homebrew)
```bash
# View logs in real-time
tail -f ~/Library/Logs/Homebrew/redis.log

# View last 100 lines
tail -n 100 ~/Library/Logs/Homebrew/redis.log

# View all logs
cat ~/Library/Logs/Homebrew/redis.log
```

### Monitor Redis in Real-Time
```bash
# Monitor all Redis commands
redis-cli MONITOR

# Monitor with timestamps
redis-cli --latency-history

# Get Redis server info
redis-cli INFO
```

---

## Methods to View Redis Logs

### Method 1: Homebrew Service Logs (macOS)

If Redis is running via `brew services`:

```bash
# View logs
tail -f ~/Library/Logs/Homebrew/redis.log

# Or use brew's log command
brew services info redis
```

**Log Location:**
- `~/Library/Logs/Homebrew/redis.log` - Main log file
- `~/Library/Logs/Homebrew/redis.err.log` - Error log (if exists)

### Method 2: Redis CLI Monitor

Monitor Redis commands in real-time:

```bash
# Monitor all commands
redis-cli MONITOR

# Monitor with specific pattern
redis-cli MONITOR | grep "SET\|GET"

# Monitor with timestamps (Redis 6.2+)
redis-cli --latency-history
```

**Example Output:**
```
OK
1640995200.123456 [0 127.0.0.1:54321] "PING"
1640995201.234567 [0 127.0.0.1:54321] "SET" "key" "value"
1640995202.345678 [0 127.0.0.1:54321] "GET" "key"
```

### Method 3: Redis Configuration Logs

Check where Redis is configured to log:

```bash
# Connect to Redis
redis-cli

# Check logfile setting
CONFIG GET logfile

# Check loglevel setting
CONFIG GET loglevel

# Set log level (if needed)
CONFIG SET loglevel verbose
```

**Log Levels:**
- `debug` - Very detailed logs
- `verbose` - Detailed logs
- `notice` - Standard logs (default)
- `warning` - Only warnings and errors

### Method 4: System Logs (macOS)

If Redis is running as a system service:

```bash
# View system logs
log show --predicate 'process == "redis-server"' --last 1h

# View with timestamps
log show --predicate 'process == "redis-server"' --info --last 30m

# Follow logs in real-time
log stream --predicate 'process == "redis-server"'
```

### Method 5: Check Redis Configuration File

Find Redis config file:

```bash
# Default locations
cat /usr/local/etc/redis.conf
cat /opt/homebrew/etc/redis.conf
cat ~/.redis/redis.conf

# Or check where Redis is looking
redis-cli CONFIG GET dir
```

---

## Useful Redis Monitoring Commands

### Get Redis Server Information
```bash
# General info
redis-cli INFO

# Server info only
redis-cli INFO server

# Memory info
redis-cli INFO memory

# Stats info
redis-cli INFO stats

# Clients info
redis-cli INFO clients

# Replication info
redis-cli INFO replication
```

### Check Redis Activity
```bash
# Slow log (commands taking > 10ms by default)
redis-cli SLOWLOG GET 10

# Get all keys (use with caution on production)
redis-cli KEYS "*"

# Count keys
redis-cli DBSIZE

# Get memory usage
redis-cli INFO memory | grep used_memory_human
```

### Monitor Performance
```bash
# Latency statistics
redis-cli --latency

# Latency history (every 15 seconds)
redis-cli --latency-history

# Latency distribution
redis-cli --latency-dist

# Real-time stats
redis-cli --stat
```

---

## Enable Verbose Logging

### Temporary (until restart)
```bash
redis-cli CONFIG SET loglevel verbose
redis-cli CONFIG SET logfile /tmp/redis.log
```

### Permanent (edit config file)

1. Find config file:
   ```bash
   brew services info redis
   # Look for "plist" path
   ```

2. Edit config:
   ```bash
   # Usually at:
   /usr/local/etc/redis.conf
   # or
   /opt/homebrew/etc/redis.conf
   ```

3. Set logging:
   ```conf
   loglevel verbose
   logfile /path/to/redis.log
   ```

4. Restart Redis:
   ```bash
   brew services restart redis
   ```

---

## View Logs by Use Case

### Debug Cache Issues
```bash
# Monitor cache operations
redis-cli MONITOR | grep -E "SET|GET|DEL|EXPIRE"

# Check cache keys
redis-cli KEYS "posts:*"
redis-cli KEYS "tasks:*"

# Check TTL of keys
redis-cli TTL "posts:list:abc123"
```

### Debug Celery Issues
```bash
# Monitor Celery queue operations
redis-cli MONITOR | grep -E "celery|task"

# Check Celery queues
redis-cli KEYS "celery*"

# List all Celery keys
redis-cli KEYS "*celery*"
```

### Monitor Connection Issues
```bash
# Check connected clients
redis-cli CLIENT LIST

# Monitor connections
redis-cli MONITOR | grep -E "CLIENT|CONNECT"

# Check client info
redis-cli INFO clients
```

---

## Log Rotation (Production)

For production, configure log rotation:

```conf
# In redis.conf
logfile /var/log/redis/redis.log
loglevel notice

# Use logrotate
# /etc/logrotate.d/redis
/var/log/redis/redis.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 redis redis
    sharedscripts
    postrotate
        redis-cli CONFIG SET logfile ""
        redis-cli CONFIG SET logfile /var/log/redis/redis.log
    endscript
}
```

---

## Quick Reference

| Task | Command |
|------|---------|
| **View logs** | `tail -f ~/Library/Logs/Homebrew/redis.log` |
| **Monitor commands** | `redis-cli MONITOR` |
| **Check status** | `redis-cli PING` |
| **Get info** | `redis-cli INFO` |
| **Slow queries** | `redis-cli SLOWLOG GET 10` |
| **Memory usage** | `redis-cli INFO memory` |
| **List keys** | `redis-cli KEYS "*"` |
| **Count keys** | `redis-cli DBSIZE` |
| **Set log level** | `redis-cli CONFIG SET loglevel verbose` |

---

## Troubleshooting

### Logs Not Found
```bash
# Check if Redis is running
redis-cli PING

# Check Redis process
ps aux | grep redis

# Check where Redis is logging
redis-cli CONFIG GET logfile
```

### Enable Logging to File
```bash
# Set logfile
redis-cli CONFIG SET logfile /tmp/redis.log

# Verify
redis-cli CONFIG GET logfile
```

### View All Redis Configuration
```bash
redis-cli CONFIG GET "*"
```

---

## Summary

**For macOS with Homebrew:**
- Logs: `~/Library/Logs/Homebrew/redis.log`
- View: `tail -f ~/Library/Logs/Homebrew/redis.log`
- Monitor: `redis-cli MONITOR`

**For Real-Time Monitoring:**
- Commands: `redis-cli MONITOR`
- Stats: `redis-cli --stat`
- Latency: `redis-cli --latency`

**For Debugging:**
- Verbose logs: `redis-cli CONFIG SET loglevel verbose`
- Slow queries: `redis-cli SLOWLOG GET 10`
- Info: `redis-cli INFO`
