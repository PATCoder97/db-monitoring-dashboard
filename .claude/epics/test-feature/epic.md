---
name: test-feature
status: backlog
created: 2026-01-02T03:31:41Z
progress: 0%
prd: .claude/prds/test-feature.md
github: null
---

# Epic: PostgreSQL Database Monitoring Dashboard

## Overview

Build a lightweight web-based monitoring dashboard for PostgreSQL databases by wrapping existing Python monitoring scripts (main.py) with a FastAPI backend and React frontend. This MVP focuses on real-time visibility into database health, table statistics, and connection metrics - enabling quick troubleshooting and proactive capacity planning.

**Core Value:** Transform manual script execution into a self-service monitoring tool accessible to the entire team.

## Architecture Decisions

### 1. Leverage Existing Code
**Decision:** Reuse main.py functions as-is, wrap them with FastAPI
**Rationale:**
- Existing `list_all_databases()` and `check_database_details()` already work
- Faster delivery - no rewrite needed
- Proven reliability with ktxn258.duckdns.org:6543

### 2. Minimal Tech Stack
**Decision:** FastAPI + React (no Redis, no complex state management initially)
**Rationale:**
- Redis adds deployment complexity - defer to v2 if needed
- Simple polling (30s refresh) sufficient for MVP
- WebSockets only if user feedback demands it

### 3. Embedded Metrics Storage
**Decision:** Store historical metrics in same PostgreSQL server being monitored
**Rationale:**
- No additional database infrastructure
- Use existing `casaos` database or create `monitoring` schema
- Simplifies deployment to single Docker container

### 4. Static Credentials (MVP)
**Decision:** Single config file for database connections, environment variables for secrets
**Rationale:**
- Multi-database credential management deferred to v2
- Faster to ship, sufficient for 2-5 databases
- Still uses encrypted environment variables

### 5. Server-Side Rendering for Exports
**Decision:** Backend generates CSV/JSON exports, not client-side
**Rationale:**
- Handles large datasets without browser memory limits
- Enables future scheduled reports
- Simpler than implementing client-side download logic

## Technical Approach

### Backend Services (Python FastAPI)

**Core API Endpoints:**
```
GET  /api/databases              # List all databases (wraps list_all_databases())
GET  /api/databases/{name}       # Database details (wraps check_database_details())
GET  /api/databases/{name}/tables # Table-level metrics
GET  /api/health                 # API health check
GET  /api/export/csv             # Export current metrics
```

**Data Models:**
- Reuse existing dict structures from main.py functions
- Add Pydantic models only for API responses (validation layer)

**Historical Metrics (Simplified):**
- Single table: `metrics_history` with columns: timestamp, db_name, metric_type, value
- Background scheduler (APScheduler) runs every 5 minutes
- Retention: Simple DELETE query for data > 90 days

**Configuration:**
- `config.yaml` for database connection list
- Environment variables for passwords (`DB_PASSWORD_CASAOS`, etc.)

### Frontend Components (React + TypeScript)

**Pages:**
1. **Dashboard Overview** (`/`)
   - Grid of database cards showing: name, size, table count, status badge
   - Search bar for filtering
   - Auto-refresh toggle (30s default)

2. **Database Detail** (`/database/:name`)
   - Header: DB version, collation, connection limit
   - Table: All tables with row counts and sizes
   - Basic line chart: Database size over last 7 days

**UI Components:**
- StatusBadge: Green (OK) / Yellow (Warning >80% connections) / Red (Error)
- DatabaseCard: Reusable card component
- MetricChart: Simple Chart.js wrapper

**State Management:**
- TanStack Query for API caching and auto-refetch
- No Redux/Context needed for MVP

**Styling:**
- Tailwind CSS for rapid development
- Mobile-responsive grid (1 col on mobile, 3 cols on desktop)

### Infrastructure

**Deployment (Docker Compose):**
```yaml
services:
  api:
    build: ./backend
    env_file: .env
    ports: ["8000:8000"]

  frontend:
    build: ./frontend
    ports: ["3000:80"]
    depends_on: [api]
```

**Environment Variables:**
```
POSTGRES_HOST=ktxn258.duckdns.org
POSTGRES_PORT=6543
DB_PASSWORD_CASAOS=casaos
METRICS_RETENTION_DAYS=90
```

**Monitoring:**
- FastAPI built-in `/docs` for API testing
- Simple logging to stdout (Docker captures)
- Health check endpoint for uptime monitoring

## Implementation Strategy

### Phase 1: Backend Foundation (Days 1-5)
1. Extract main.py functions into `db_client.py` module
2. Create FastAPI app with 4 core endpoints
3. Add Pydantic response models
4. Implement basic error handling (connection timeouts, invalid DB names)
5. Create metrics_history table and background scheduler

### Phase 2: Frontend Dashboard (Days 6-10)
1. Create React app with TypeScript template
2. Build DatabaseCard and StatusBadge components
3. Implement Dashboard Overview page with TanStack Query
4. Add search/filter functionality
5. Integrate Chart.js for basic metrics visualization

### Phase 3: Database Detail & Export (Days 11-15)
1. Build Database Detail page with table listing
2. Add historical metrics chart (7-day view)
3. Implement CSV export endpoint
4. Add configuration page (view connection list)
5. Polish UI responsiveness

### Phase 4: Testing & Deployment (Days 16-20)
1. Integration testing (API + Frontend)
2. Load testing (simulate 10 databases, 100 tables each)
3. Create Docker Compose setup
4. Write deployment documentation
5. User acceptance testing with DevOps team

### Risk Mitigation
- **Risk:** Existing main.py functions fail in production
  - **Mitigation:** Add comprehensive error handling and logging early
- **Risk:** Performance degrades with many databases
  - **Mitigation:** Implement query timeouts (5s), concurrent requests limit
- **Risk:** Historical data grows unbounded
  - **Mitigation:** Automated retention policy from day 1

## Task Breakdown Preview

The implementation will be divided into these 8 tasks:

- [ ] **T1: Backend API Foundation** - FastAPI setup, extract main.py logic, create core endpoints
- [ ] **T2: Metrics Storage & Scheduler** - Historical metrics table, background job for data collection
- [ ] **T3: API Error Handling & Security** - Timeout handling, credential management, input validation
- [ ] **T4: Frontend Dashboard Overview** - React app, database cards, search/filter, auto-refresh
- [ ] **T5: Database Detail Page** - Table listing, metrics charts, navigation
- [ ] **T6: Data Export & Configuration** - CSV export, config management UI
- [ ] **T7: Docker Deployment Setup** - Dockerfile, docker-compose, environment config
- [ ] **T8: Testing & Documentation** - Integration tests, deployment guide, user manual

## Dependencies

### External Dependencies
- **PostgreSQL Server:** ktxn258.duckdns.org:6543 must remain accessible
- **Network:** Firewall rules allow connections from deployment server
- **Credentials:** Database passwords provided securely (not committed to git)

### Internal Dependencies
- **Security Review:** Config file encryption approach (Week 2)
- **DevOps Support:** Docker host provisioning (Week 3)

### Technology Dependencies
- Python 3.11+ (already available)
- Node.js 18+ for React build
- Docker & Docker Compose for deployment
- PostgreSQL 17.4+ (already deployed)

## Success Criteria (Technical)

### Performance Benchmarks
- [ ] API response time: < 500ms per endpoint (p95)
- [ ] Dashboard initial load: < 2 seconds
- [ ] Support monitoring 10 databases with 50 tables each
- [ ] Metrics collection completes within 1 minute for all databases

### Quality Gates
- [ ] Zero errors when database temporarily unreachable (graceful degradation)
- [ ] 95%+ test coverage on critical backend functions
- [ ] All API endpoints documented in OpenAPI (auto-generated by FastAPI)
- [ ] Mobile-responsive design verified on iPhone and Android

### Acceptance Criteria
- [ ] DevOps team can view all databases without running scripts
- [ ] Database detail page shows accurate table counts (verified vs psql)
- [ ] Historical metrics chart displays last 7 days of database size
- [ ] CSV export downloads within 3 seconds for current metrics

## Estimated Effort

**Total Duration:** 4 weeks (20 working days)

**Resource Requirements:**
- 1 Backend Developer (Python/FastAPI): 12 days
- 1 Frontend Developer (React/TypeScript): 10 days
- Shared DevOps Support: 3 days (deployment, testing)

**Critical Path:**
1. Backend API (Days 1-5) - BLOCKING frontend work
2. Frontend Dashboard (Days 6-10) - BLOCKING integration testing
3. Testing & Deployment (Days 16-20) - Final validation

**Buffer:** 1 week built into 6-week PRD timeline for unexpected issues

## Tasks Created

- [ ] 001.md - Backend API Foundation (parallel: false)
- [ ] 002.md - Metrics Storage & Scheduler (parallel: false, depends on 001)
- [ ] 003.md - API Error Handling & Security (parallel: true, depends on 001)
- [ ] 004.md - Frontend Dashboard Overview (parallel: true, depends on 001)
- [ ] 005.md - Database Detail Page (parallel: false, depends on 002, 004)
- [ ] 006.md - Data Export & Configuration (parallel: true, depends on 001, 004)
- [ ] 007.md - Docker Deployment Setup (parallel: false, depends on 001, 004)
- [ ] 008.md - Testing & Documentation (parallel: false, depends on all)

**Total tasks:** 8
**Parallel tasks:** 3 (003, 004, 006)
**Sequential tasks:** 5 (001, 002, 005, 007, 008)
**Estimated total effort:** 94 hours (~12 working days)

---

**Next Steps:**
1. Review task breakdown
2. Sync to GitHub with `/pm:epic-sync test-feature` to create issues
3. Start with Task 001 (Backend API Foundation)
