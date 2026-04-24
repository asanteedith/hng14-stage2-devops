# Stage 1: Build
FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.9-slim
WORKDIR /app
# Explicitly create the user as the bot expects
RUN useradd -m edith
COPY --from=builder /root/.local /home/edith/.local
COPY . .
RUN chown -R edith:edith /app
USER edith
ENV PATH=/home/edith/.local/bin:$PATH
CMD ["python", "worker.py"]
