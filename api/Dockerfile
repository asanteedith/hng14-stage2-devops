# Stage 1: Build (Installs dependencies)
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Final Runtime
FROM python:3.11-slim
WORKDIR /app

# Rule: Run as non-root user
RUN useradd -m edith
USER edith

# Copy only the installed packages and code
COPY --from=builder /root/.local /home/edith/.local
COPY . .

# Set environment path for the user
ENV PATH=/home/edith/.local/bin:$PATH

# Rule: Working HEALTHCHECK
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/docs || exit 1

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]