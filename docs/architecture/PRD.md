# Product Requirements Document (PRD)
## Project Title: UniChrist — Enterprise Autonomous Campus Operating & Intelligence System (COIS)

### 1. Executive Summary & Vision
UniChrist transitions from an ad-hoc timetable/counter logger into an enterprise-grade, distributed Autonomous Campus Operating and Intelligence System (COIS). The system orchestrates schedule-derived spatial presence, automated high-throughput cafeteria order batching, auditable decentralized grievance redressal, smart parking telemetry, and multimodal AI inference with zero-latency edge delivery.

### 2. Personas & Stakeholder Matrix
- **Student (Undergraduate/Postgraduate):** Consumes schedule location services, executes cashless cafeteria orders, claims lost & found items, files grievances with verifiable SLA logs.
- **Faculty & Academic Staff:** Maintains consultation hours, issues automated temporary venue overrides, inspects student grievance logs.
- **Facility & Security Operator:** Inspects smart parking slot telemetries, verifies gate access, monitors ClamAV sanitization reports.
- **System Administrator & Security Officer (CSO):** Audits Nginx reverse proxy policies, STIX-compliant threat streams, Redis cache consistency, and AI inference latency budgets.

### 3. Core Functional Requirements
#### 3.1 Faculty Schedule & Spatial Presence Engine (FR-1)
- The system shall determine faculty location algorithmically by querying the weekly institutional timetable against wall-clock time and active `FacultyStatusOverride` directives.
- When an active period matches, the engine emits the verified room vector (Block, Floor, Room Number, Capacity). If no lecture exists, the system automatically routes to the primary faculty cabin.
- Real-time presence states must be streamed to edge consumers via Redis Streams (`stream:faculty:presence`).

#### 3.2 High-Concurrency Cafeteria Engine with Token Batching (FR-2)
- Cart items must be validated with RedisJSON inventory schemas and locked using Redis distributed locks (`Redlock`) before database commit.
- Integration with YouPI-PG (Unified Payment Gateway) handling mock and production webhooks (UPI, Campus Wallet, NetBanking).
- Token generator generates cyclic daily tokens (101 to 999) without race conditions.

#### 3.3 SLA-Enforced Grievance Redressal (FR-3)
- Cryptographically signed submission of grievances with automatic assignment to staff coordinators.
- Every state transition (`PENDING` -> `ASSIGNED` -> `IN_PROGRESS` -> `RESOLVED` -> `CLOSED`) generates an immutable audit record in `grievance_audit_logs`.
- Attachments (images/logs) pass through ClamAV anti-malware pipeline before persistence.

#### 3.4 Multi-Slot Parking Telemetry (FR-4)
- Live slot occupancy polling and sensor simulation via Redis key-value cache and WebSocket pub-sub.
- EV charging station wattage & bay allocation tracking.

#### 3.5 AI Routing & Multimodal Dispatch (FR-5)
- OmniRoute proxy layer abstracting free inference providers (Lightning.ai, Hugging Face Spaces, Saturn Cloud, Kaggle, Colab, Replicate) with fallbacks.

### 4. Non-Functional Requirements & DevSecOps SLOs
- **P99 Response Time:** < 45ms for cached edge endpoints; < 220ms for full-stack database transactions.
- **Availability Target:** 99.95% uptime orchestrating through Coolify multi-container clusters and Vercel edge CDN.
- **Security & Compliance:** Zero critical CVEs in Sherlock vulnerability scans; strict Content Security Policy (CSP); STIX 2.1 threat event serialization; Sentry real-time tracing.

