# hng14-stage2-devops

A containerized microservices application featuring a Node.js frontend, a FastAPI backend, and a Python background worker, all coordinated via Redis.

##  Architecture Overview

The system is composed of four main services:
- Frontend: A Node.js application serving the user dashboard.
- API: A Python FastAPI service that handles job submissions and status reporting.
- Redis: An in-memory data store used for the job queue and status tracking.
- Worker: A Python background process that pulls jobs from Redis and processes them asynchronously.

## 🛡️ DevOps & Security Hardening
- Principle of Least Privilege: All services run as dedicated non-root users (`edith` for Python, node for Node.js) to mitigate security risks.
- Multi-stage Builds: Optimized Docker images to ensure small footprints and faster deployment times by separating build dependencies from the runtime environment.
- Service Orchestration: Implemented Redis healthchecks in docker-compose.yml to ensure stable startup sequences and prevent connection race conditions.
- Networking: Isolated internal communication between the API, Worker, and Redis using a dedicated Docker bridge network.

## Getting Started

### Prerequisites
- Docker and Docker Desktop installed.
- Git.

### Local Setup
1. Clone the repository:
   ```bash
   git clone <https://github.com/asanteedith/hng14-stage2-devops>
   cd hng14-stage2-devops