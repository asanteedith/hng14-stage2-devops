# Stage 1: Build
FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.9-slim
WORKDIR /app

# Create a dedicated non-root user named 'hng'
RUN useradd -m hng && chown -R hng:hng /app

# Copy dependencies from builder
COPY --from=builder /root/.local /home/hng/.local
COPY . .

# Secure permissions
RUN chown -R hng:hng /app
USER hng

# Set Path and Environment
ENV PATH=/home/hng/.local/bin:$PATH
EXPOSE 8000

# Healthcheck for the bot
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]