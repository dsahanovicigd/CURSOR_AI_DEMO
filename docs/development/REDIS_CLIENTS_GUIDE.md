# Redis Clients Guide

Complete guide to Redis clients for connecting to `redis://localhost:6379/0`

---

## Command-Line Clients

### 1. redis-cli (Built-in, Recommended)

**Installation:**
```bash
# macOS
brew install redis

# Linux
sudo apt-get install redis-tools
```

**Usage:**
```bash
# Connect to default (localhost:6379)
redis-cli

# Connect with explicit URL
redis-cli -u redis://localhost:6379/0

# Connect with password (if set)
redis-cli -a yourpassword

# Execute command directly
redis-cli PING
redis-cli GET mykey
redis-cli KEYS "*"
```

**Features:**
- ✅ Built-in with Redis
- ✅ Full Redis command support
- ✅ Interactive mode
- ✅ Batch mode
- ✅ Pipe mode

---

## GUI Applications

### 1. RedisInsight (Official, Free)

**Download:** https://redis.io/insight/

**Features:**
- ✅ Official Redis GUI
- ✅ Free and open-source
- ✅ Cross-platform (macOS, Windows, Linux)
- ✅ Visual data browser
- ✅ Query builder
- ✅ Performance monitoring
- ✅ Memory analysis
- ✅ Slow log viewer

**Connection:**
```
Host: localhost
Port: 6379
Database: 0
```

### 2. Another Redis Desktop Manager (Free)

**Download:** https://github.com/qishibo/AnotherRedisDesktopManager

**Features:**
- ✅ Free and open-source
- ✅ Cross-platform
- ✅ Modern UI
- ✅ Key management
- ✅ Value editor
- ✅ Command execution
- ✅ Connection management

**Connection:**
```
Host: localhost
Port: 6379
Database: 0
```

### 3. Redis Desktop Manager / Redis Insight (Paid)

**Download:** https://resp.app/ (formerly Redis Desktop Manager)

**Features:**
- ✅ Professional GUI
- ✅ Paid (free trial available)
- ✅ Advanced features
- ✅ SSH tunneling
- ✅ SSL/TLS support

### 4. Medis (macOS, Free)

**Download:** https://github.com/luin/medis

**Features:**
- ✅ macOS native app
- ✅ Free and open-source
- ✅ Beautiful UI
- ✅ Key browser
- ✅ Command execution

**Installation:**
```bash
brew install --cask medis
```

---

## Web-Based Clients

### 1. Redis Commander (Web UI)

**Installation:**
```bash
npm install -g redis-commander
```

**Usage:**
```bash
# Start web server
redis-commander

# Access at http://localhost:8081
```

**Connection:**
- Default connects to `localhost:6379`
- Access via browser: http://localhost:8081

### 2. Redis Web Manager

**Installation:**
```bash
docker run -d --name redis-web-manager \
  -p 9987:9987 \
  -e REDIS_HOSTS=local:localhost:6379 \
  erikdubbelboer/redis-web-manager
```

**Access:** http://localhost:9987

---

## IDE Extensions

### 1. VS Code Extensions

**Redis Extension (by cweijan)**
- Extension ID: `cweijan.vscode-redis-client`
- Features: Browse keys, execute commands, view values

**Install:**
```bash
code --install-extension cweijan.vscode-redis-client
```

**Usage:**
1. Open VS Code
2. Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
3. Type "Redis: Connect"
4. Enter connection: `redis://localhost:6379/0`

**Redis Extension (by dunn)**
- Extension ID: `dunn.redis`
- Features: Simple Redis client

### 2. IntelliJ IDEA / PyCharm

**Redis Plugin**
- Plugin: "Redis"
- Features: Database tool window, key browser

**Install:**
1. File → Settings → Plugins
2. Search "Redis"
3. Install and restart

---

## Browser Extensions

### 1. Redis Commander (Chrome Extension)

**Install:** Chrome Web Store → Search "Redis Commander"

**Features:**
- Browser-based
- Quick access
- Basic operations

---

## Programming Language Clients

### Python

**redis-py:**
```bash
pip install redis
```

```python
import redis

r = redis.Redis(host='localhost', port=6379, db=0)
r.set('key', 'value')
print(r.get('key'))
```

### Node.js

**ioredis:**
```bash
npm install ioredis
```

```javascript
const Redis = require('ioredis');
const redis = new Redis('redis://localhost:6379/0');

redis.set('key', 'value');
redis.get('key').then(result => console.log(result));
```

### Java

**Jedis:**
```xml
<dependency>
    <groupId>redis.clients</groupId>
    <artifactId>jedis</artifactId>
    <version>4.3.1</version>
</dependency>
```

```java
Jedis jedis = new Jedis("localhost", 6379);
jedis.select(0);
jedis.set("key", "value");
String value = jedis.get("key");
```

---

## Docker-Based Clients

### Redis Commander (Docker)

```bash
docker run -d \
  --name redis-commander \
  -p 8081:8081 \
  rediscommander/redis-commander:latest \
  --redis-host=host.docker.internal \
  --redis-port=6379
```

Access: http://localhost:8081

### Redis Insight (Docker)

```bash
docker run -d \
  --name redis-insight \
  -p 8001:8001 \
  redis/redisinsight:latest
```

Access: http://localhost:8001

---

## Recommended Clients by Use Case

### For Development (macOS)
1. **Medis** - Native macOS app, beautiful UI
2. **RedisInsight** - Official, feature-rich
3. **VS Code Extension** - Integrated with editor

### For Quick Access
1. **redis-cli** - Command-line, always available
2. **Redis Commander** - Web-based, easy setup

### For Production Monitoring
1. **RedisInsight** - Official monitoring tools
2. **redis-cli** - Scriptable, reliable

### For Teams
1. **RedisInsight** - Shareable dashboards
2. **Another Redis Desktop Manager** - Free, cross-platform

---

## Quick Setup Examples

### RedisInsight (Recommended)

**macOS:**
```bash
brew install --cask redisinsight
```

**Or download:** https://redis.io/insight/

**Connection:**
1. Open RedisInsight
2. Click "Add Redis Database"
3. Enter:
   - Host: `localhost`
   - Port: `6379`
   - Database Alias: `Local Development`
4. Click "Add Redis Database"

### Medis (macOS)

**Install:**
```bash
brew install --cask medis
```

**Connection:**
1. Open Medis
2. Click "+" to add connection
3. Enter:
   - Host: `localhost`
   - Port: `6379`
   - Database: `0`
4. Click "Connect"

### VS Code Extension

**Install:**
```bash
code --install-extension cweijan.vscode-redis-client
```

**Connect:**
1. Open VS Code
2. Press `Cmd+Shift+P`
3. Type "Redis: Connect"
4. Enter: `redis://localhost:6379/0`

---

## Connection String Format

All clients support this format:
```
redis://localhost:6379/0
```

**Breakdown:**
- `redis://` - Protocol
- `localhost` - Host
- `6379` - Port
- `0` - Database number

**With password:**
```
redis://:password@localhost:6379/0
```

**With username and password:**
```
redis://username:password@localhost:6379/0
```

---

## Testing Connection

Before using any client, test connection:

```bash
# Test with redis-cli
redis-cli -u redis://localhost:6379/0 PING
# Should return: PONG

# Test connection
redis-cli -u redis://localhost:6379/0 INFO server
```

---

## Summary

**Best Overall:** RedisInsight (Official, Free, Feature-Rich)
**Best for macOS:** Medis (Native, Beautiful)
**Best for VS Code:** Redis Extension by cweijan
**Best Command-Line:** redis-cli (Built-in)
**Best Web-Based:** Redis Commander

**Quick Start:**
1. Install RedisInsight: `brew install --cask redisinsight`
2. Or use redis-cli: `redis-cli -u redis://localhost:6379/0`
3. Or install VS Code extension: `cweijan.vscode-redis-client`
