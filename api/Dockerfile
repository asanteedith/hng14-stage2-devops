# Stage 1: Build
FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.9-slim
WORKDIR /app

# Create user 'edith'
RUN useradd -m edith
# Copy only the installed packages from the builder stage
COPY --from=builder /root/.local /home/edith/.local
COPY . .
RUN chown -R edith:edith /app

USER edith
# Ensure the user's local bin is in the PATH
ENV PATH=/home/edith/.local/bin:$PATH

EXPOSE 8000

# ONLY ONE CMD - MUST BE AT THE END
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]