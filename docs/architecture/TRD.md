# Technical Requirements Document (TRD)
## UniChrist Architecture, Protocols, and Systems Engineering Specification

### 1. Architectural Overview
UniChrist utilizes a hybrid edge-and-cloud architecture:
- **Edge Layer (Vercel):** Hosts the static web client, edge rewrites, cache revalidation, and static asset distribution.
- **Compute Cluster (Coolify on Self-Hosted VM/Bare Metal):** Houses the containerized C# .NET 8 Web API, Redis Stack (RediSearch + RedisJSON), OmniRoute AI Proxy, YouPI-PG Mock Payment Gateway, ClamAV Daemon, and Nginx Hardened Proxy.
- **Persistence Layer:** MySQL 8.0+ for relational integrity with BCNF-normalized schema; Redis for distributed caching, sub-millisecond timetable indexing, and Pub/Sub streams.

### 2. Microservice & Layer Topology
```
[Client / Edge Browser]
         │ (HTTPS / TLS 1.3)
         ▼
[Vercel Edge Network / Nginx Hardened Ingress]
         │
         ├───> [Nginx Reverse Proxy & ModSecurity]
         │         │
         │         ├───> [C# .NET 8 UniChrist Core API] ───> [MySQL 8.0 Cluster]
         │         │         │
         │         │         ├───> [Redis Stack: RediSearch + RedisJSON + Streams]
         │         │         │
         │         │         └───> [YouPI-PG Payment Gateway Microservice]
         │         │
         │         ├───> [OmniRoute AI Proxy] ───> [Free Inference Providers]
         │         │         (Lightning.ai / Hugging Face Spaces / Kaggle / Colab)
         │         │
         │         └───> [ClamAV Scan Engine Daemon] (File Upload Pipeline)
         │
         └───> [Sentry Tracing & STIX 2.1 Threat Auditing Engine]
```

### 3. Data Storage & Schema Design
- **Relational Integrity (MySQL):** InnoDB engine, UTF8MB4 charset, foreign key cascades, transaction isolation level `READ COMMITTED`.
- **Redis High-Performance Layer:**
  - `redis:faculty:timetable:{id}`: Hash containing serialized weekly periods.
  - `redis:parking:slots:state`: RediSearch document for fast geospatial and occupancy querying.
  - `redis:cart:session:{id}`: RedisJSON document storing user basket state with TTL of 900s.
  - `stream:campus:events`: Redis Stream receiving live campus notifications.

### 4. OmniRoute Proxy Specification
- **Path:** `/api/v1/omniroute/chat` and `/api/v1/omniroute/embeddings`.
- **Behavior:** Dynamic model cascading across tier-0 free cloud GPUs (Lightning.ai Studio API, Hugging Face Spaces, Saturn Cloud endpoints). Automatic fallback to local simulated fallback if upstream is down.

### 5. YouPI-PG Gateway Specification
- **Endpoints:**
  - `POST /api/v1/youpi/order/create`: Generates unique transaction payload and signature.
  - `POST /api/v1/youpi/order/verify`: Validates HMAC-SHA256 signature and returns payment settlement.
  - `POST /api/v1/youpi/webhook`: Idempotent webhook receiver verifying order fulfillment.

