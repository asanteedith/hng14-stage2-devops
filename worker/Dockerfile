FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
RUN useradd -m edith
USER edith
COPY --from=builder /root/.local /home/edith/.local
COPY . .
ENV PATH=/home/edith/.local/bin:$PATH
# Rule: Healthcheck for background process
HEALTHCHECK --interval=30s --timeout=3s CMD pgrep python || exit 1

CMD ["python", "worker.py"]