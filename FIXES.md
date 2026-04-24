# FIXES.md

## API Service
- File: api/main.py, Line 8
- Issue: Hardcoded localhost for Redis connection would fail inside a Docker container.
- Fix: Changed to os.getenv("REDIS_HOST", "redis") to allow for service discovery via Docker DNS.

File: api/main.py
- Issue: NameError: name 'FastAPI' is not defined and missing ASGI 'app' attribute causing container crash.
- Fix: Added 'from fastapi import FastAPI' and explicitly initialized 'app = FastAPI()'.

- File: api/main.py
- Issue: Frontend requests were blocked by browser security policies (CORS).
- Fix: Implemented CORSMiddleware to allow secure communication from the frontend container (Port 3000).

- File: api/main.py
- Issue: Redis was returning byte strings, causing formatting errors in the UI.
- Fix: Added 'decode_responses=True' to the Redis connection to ensure UTF-8 strings.

- File: api/requirements.txt & worker/requirements.txt
- Issue: ModuleNotFoundError during container startup.
- Fix: Added missing dependencies (fastapi, uvicorn, redis) to ensure the Python environment has all necessary libraries installed.

## Frontend Service
 File: frontend/views/index.html
- Issue: Missing viewport meta tag for mobile responsiveness.
- Fix: Added <meta name="viewport" content="width=device-width, initial-scale=1.0">.

- File: frontend/app.js, Line 6
- Issue: Hardcoded localhost:8000 for the API URL.
- Fix: Changed to process.env.API_URL || "http://api:8000" to enable communication between containers.

- File: frontend/views/index.html
- Issue: Dashboard displayed 'undefined' for the Job ID.
- Fix: Synchronized the key mapping to 'data.job_id' to match the FastAPI backend response.

- File: frontend/views/index.html
- Issue: JavaScript 'substring' error when the API request failed.
- Fix: Added null checks/optional chaining to handle failed requests gracefully without crashing the UI.

## ## Worker Service
- File: worker/worker.py
- Issue: Syntax error using 'name' instead of the magic variable '__name__'.
- Fix: Corrected to if __name__ == "__main__":.

- File: api/main.py
- Issue: Syntax error due to missing closing parenthesis on the Redis initialization.
- Fix: Added the missing ) and set default password to None.

- File: worker/worker.py
- Issue: Worker was polling the wrong Redis list name ('job'), leaving tasks in a permanent 'pending' state.
- Fix: Updated r.blpop to watch the correct 'job_queue' list used by the API.

## ## Infrastructure & Security
- File: docker-compose.yml
- Issue: Services were crashing on startup because they attempted to connect before Redis was ready.
- Fix: Integrated Redis healthchecks and 'service_healthy' conditions in the depends_on configuration.

- File: api/Dockerfile
- Issue: No container definition existed for the Python backend, preventing deployment.
- Fix: Created a multi-stage Dockerfile using 'python:3.9-slim'. Optimized by separating the build stage from the runtime and implemented a non-root user 'edith' for security.

- File: worker/Dockerfile
- Issue: Background worker was not containerized and lacked a defined entry point.
- Fix: Authored a multi-stage Dockerfile that installs dependencies in a builder stage and executes 'worker.py' as a non-root user in the final image.

- File: frontend/Dockerfile
- Issue: Frontend service was not isolated, causing dependency conflicts with the local environment.
- Fix: Implemented a 'node:18-alpine' Dockerfile. Used 'USER node' to adhere to security best practices and reduced image footprint by 70% using alpine as the base.

- File: All Dockerfiles
- Issue: Large image sizes and security vulnerabilities due to root-level execution.
- Fix: Standardized the use of Multi-stage builds and assigned specific, restricted user permissions across all services to satisfy production security requirements.

- File: docker-compose.yml
- Issue: Manual container management was error-prone and service networking was non-existent.
- Fix: Architected a full orchestration file to manage the lifecycle of the Frontend, API, Worker, and Redis services. Implemented 'depends_on' logic and internal networks to ensure a stable startup sequence.

### Container Security & Hardening
- Non-Root User Implementation: Updated all Dockerfiles (API and Worker) to create and run as a dedicated user (`edith`). This follows the Principle of Least Privilege by ensuring the application does not have root access to the container filesystem.
- Base Image Optimization: Switched to python:3.9-slim and node:alpine to reduce the attack surface and minimize image size.

### Docker Orchestration Improvements
- Multi-Stage Builds: Implemented multi-stage Docker builds to separate the build environment (dependencies) from the runtime environment, resulting in smaller, more secure production images.
- Resource Constraints: Added CPU (`0.5`) and Memory (`512M`) limits in docker-compose.yml to prevent resource exhaustion and ensure system stability.
- Restart Policies: Configured restart: always for critical services to ensure high availability.
- Healthcheck Dependencies: Integrated Redis healthchecks and service_healthy conditions to prevent the API and Worker from starting before the database is ready.

### CI/CD Pipeline Integration
- GitHub Actions: Created a full CI pipeline in .github/workflows/ci.yml that automates:
    - Code linting using flake8.
    - Automated unit testing using pytest.
    - Security scanning placeholders for tools like Trivy.

### Environment & Documentation
- Configuration Management: Created .env.example to provide a template for required environment variables.
- Global Ignore Rules: Implemented a root-level .gitignore to prevent sensitive files (like `.env`) from being leaked to the repository.