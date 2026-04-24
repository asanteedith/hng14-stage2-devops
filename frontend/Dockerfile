# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Stage 2: Production
FROM node:18-alpine
WORKDIR /app
# Rule: Run as non-root user
RUN addgroup -S edith && adduser -S edith -G edith
USER edith
COPY --from=builder /app ./

# Rule: Healthcheck
HEALTHCHECK --interval=30s --timeout=3s CMD wget --spider http://localhost:3000/ || exit 1

EXPOSE 3000
CMD ["node", "app.js"]