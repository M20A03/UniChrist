# Redis Architecture, RediSearch Indices & RedisJSON Specification
## High-Throughput In-Memory Caching & Real-Time Streams Specification

### 1. Redis Stack Topology
The cluster runs `redis/redis-stack-server:latest` exposing RediSearch, RedisJSON, RedisGraph, and TimeSeries modules over port 6379 with ACL security.

### 2. Redis Data Structures & Key Namespaces

| Namespace Pattern | Redis Type | Purpose | TTL |
| :--- | :--- | :--- | :--- |
| `unichrist:faculty:loc:{faculty_id}` | HASH | Sub-millisecond lookup of faculty presence | 300s (refresh on override) |
| `unichrist:timetable:{faculty_id}:{day}` | JSON | Full day schedule structure (periods, rooms, sections) | 86400s (1 day) |
| `unichrist:parking:slot:{slot_code}` | HASH | Real-time sensor state, vehicle registration, EV charging | Infinite (updated on event) |
| `unichrist:cart:{user_id}` | JSON | User cafeteria shopping cart with RedisJSON schema | 1800s (30 mins) |
| `unichrist:stream:campus_telemetry` | STREAM | Log stream for biometric scans, parking changes, alerts | Capped at 10,000 entries |
| `unichrist:rate_limit:{ip}` | STRING / INCR | Leaky bucket rate limiter (120 req / 60s) | 60s |

### 3. RediSearch Schema Definition

```redis
FT.CREATE idx:faculty ON HASH PREFIX 1 "unichrist:faculty:loc:" SCHEMA
    faculty_id NUMERIC SORTABLE
    faculty_name TEXT WEIGHT 2.0
    department TEXT
    status TAG
    current_room TEXT
    last_updated NUMERIC

FT.CREATE idx:library_books ON JSON PREFIX 1 "unichrist:book:" SCHEMA
    $.isbn AS isbn TAG
    $.title AS title TEXT WEIGHT 2.0
    $.author AS author TEXT
    $.category AS category TAG
    $.available_copies AS available NUMERIC SORTABLE
```

### 4. Redis Stream Workflow for Spatial Presence
```
Producer (.NET / Simulated Biometric Node)
   │
   ▼ XADD unichrist:stream:campus_telemetry * event_type "PRESENCE_SCAN" faculty_id 3 room_id 2 status "IN_CLASS"
   │
Redis Stream Consumer Group: `cg:presence_workers`
   │
   ├─► Worker 1: Updates HASH `unichrist:faculty:loc:3`
   ├─► Worker 2: Invalidates edge Vercel ISR cache tag `faculty-3`
   └─► Worker 3: Dispatches SSE / WebSocket payload to connected browsers
```

