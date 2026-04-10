---
name: docker-dev
description: Use when working with Docker containers, building images, using docker-compose, or setting up containerized development environments. Covers Dockerfile creation, container management, and common development workflows.
---

# Docker Development

## Overview

Docker is a containerization platform that packages applications with all dependencies into standardized units. This skill provides guidance for Docker-based development workflows.

**Core principle:** Build once, run anywhere - containers ensure consistency across development, testing, and production environments.

## When to Use

```
Need containerized development?
│
├─ Set up development environment?
│  └─ Use docker-compose with multiple services
│
├─ Package application?
│  └─ Create Dockerfile with dependencies
│
├─ Run database/service?
│  └─ Use existing image or create custom image
│
├─ Share development setup?
│  └─ Provide docker-compose.yml for team
│
└─ Deploy to production?
   └─ Build optimized images and deploy containers
```

**Use this skill when:**
- Creating containerized applications
- Setting up development environments
- Managing multi-service applications
- Building custom Docker images
- Debugging containerized services
- Setting up CI/CD pipelines

**When NOT to use:**
- For simple scripts that run directly on host
- When performance overhead is critical
- For applications with complex GUI requirements

## Quick Reference

### Essential Commands

| Command | Description |
|---------|-------------|
| `docker ps` | List running containers |
| `docker ps -a` | List all containers |
| `docker images` | List images |
| `docker build -t name .` | Build image from Dockerfile |
| `docker run -d name` | Run container in background |
| `docker stop <container>` | Stop container |
| `docker rm <container>` | Remove container |
| `docker rmi <image>` | Remove image |
| `docker logs <container>` | Show container logs |
| `docker exec -it <container> sh` | Execute command in container |

### Docker Compose Commands

| Command | Description |
|---------|-------------|
| `docker-compose up` | Create and start services |
| `docker-compose up -d` | Start services in background |
| `docker-compose down` | Stop and remove services |
| `docker-compose logs` | Show service logs |
| `docker-compose exec service cmd` | Execute command in service |
| `docker-compose build` | Build service images |
| `docker-compose pull` | Pull service images |

## Dockerfile Basics

### Simple Node.js Application

```dockerfile
# Use official Node.js image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Start application
CMD ["node", "index.js"]
```

### Python Application

```dockerfile
# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Start application
CMD ["python", "app.py"]
```

### Multi-stage Build

```dockerfile
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

## Docker Compose Examples

### Web Application + Database

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
    depends_on:
      - db
    volumes:
      - .:/app
      - /app/node_modules

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### Microservices Architecture

```yaml
version: '3.8'

services:
  api:
    build: ./api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://db:5432/api
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  worker:
    build: ./worker
    environment:
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api

volumes:
  postgres_data:
  redis_data:
```

## Common Operations

### Running Containers

```bash
# Run interactive container
docker run -it ubuntu:latest bash

# Run with port mapping
docker run -p 8080:80 nginx:alpine

# Run with volume mount
docker run -v $(pwd)/data:/app/data ubuntu:latest

# Run with environment variables
docker run -e API_KEY=secret -e DEBUG=true node:18 node app.js

# Run in background with auto-restart
docker run -d --restart unless-stopped nginx:alpine
```

### Managing Containers

```bash
# View container logs
docker logs <container-id>

# Follow logs in real-time
docker logs -f <container-id>

# Execute command in running container
docker exec -it <container-id> bash

# Inspect container details
docker inspect <container-id>

# View container resource usage
docker stats

# Copy files to/from container
docker cp localfile.txt <container-id>:/path/in/container/
docker cp <container-id>:/path/in/container/remotefile.txt .
```

### Building Images

```bash
# Build with tag
docker build -t myapp:1.0 .

# Build without cache
docker build --no-cache -t myapp:latest .

# Build with build arguments
docker build --build-arg NODE_ENV=production -t myapp .

# Build for specific platform
docker build --platform linux/amd64 -t myapp .

# View image layers
docker history myapp:1.0
```

## Optimization Tips

### Image Size Reduction

```dockerfile
# ✅ Good: Use alpine base image
FROM node:18-alpine

# ✅ Good: Multi-stage builds
FROM node:18 AS builder
# ... build steps ...
FROM node:18-alpine
COPY --from=builder /app/dist ./dist

# ✅ Good: Clean up in same layer
RUN apt-get update && \
    apt-get install -y package && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ❌ Bad: Separate layers for cleanup
RUN apt-get update
RUN apt-get install -y package
RUN apt-get clean
```

### Caching Strategy

```dockerfile
# ✅ Good: Copy package files first
COPY package*.json ./
RUN npm ci
COPY . .

# ❌ Bad: Copy everything at once
COPY . .
RUN npm ci
```

## Development vs Production

### Development Dockerfile

```dockerfile
FROM node:18

WORKDIR /app

# Install all dependencies (including dev)
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Enable hot reloading with nodemon
RUN npm install -g nodemon
EXPOSE 3000
CMD ["nodemon", "index.js"]
```

### Production Dockerfile

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy and build application
COPY . .
RUN npm run build

# Production image
FROM node:18-alpine

WORKDIR /app

# Copy only production files
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

## Debugging

### View Container Logs

```bash
# All logs
docker logs <container>

# Last 100 lines
docker logs --tail 100 <container>

# Follow logs
docker logs -f <container>

# Logs with timestamps
docker logs -t <container>

# Logs from specific time
docker logs --since 2024-01-01T00:00:00 <container>
```

### Inspect Container State

```bash
# View container processes
docker top <container>

# View container ports
docker port <container>

# View container filesystem changes
docker diff <container>

# View container resource usage
docker stats <container>
```

### Debug Dockerfile Builds

```bash
# Build with verbose output
docker build --progress=plain -t myapp .

# Keep intermediate containers
docker build --rm=false -t myapp .

# Run specific build stage
docker build --target builder -t myapp-builder .
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Running as root | Create non-root user in Dockerfile |
| Storing secrets in images | Use environment variables or secrets management |
| Large image sizes | Use alpine bases, multi-stage builds |
| Not tagging images | Always use version tags |
| Ignoring .dockerignore | Create .dockerignore like .gitignore |
| Hardcoding paths | Use ENV and ARG for flexibility |
| Not limiting resources | Set memory and CPU limits in docker-compose |

## .dockerignore

```bash
# Dependencies
node_modules/
vendor/

# Build outputs
dist/
build/
*.pyc

# IDE
.vscode/
.idea/
*.swp

# Git
.git/
.gitignore

# Documentation
README.md
*.md

# Tests
test/
tests/
*.test.js
*.spec.js

# Environment
.env
.env.local
.env.*.local

# Logs
*.log
npm-debug.log*

# OS
.DS_Store
Thumbs.db
```

## Security Best Practices

```dockerfile
# ✅ Use specific version tags
FROM node:18.2.0-alpine

# ✅ Create non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# ✅ Scan for vulnerabilities
RUN apt-get update && \
    apt-get install -y security-updates

# ✅ Minimize attack surface
FROM node:18-alpine
# Don't install unnecessary tools

# ❌ Avoid latest tag
FROM node:latest

# ❌ Avoid running as root
USER root
```

## Resources

- **Docker Documentation**: https://docs.docker.com/
- **Docker Compose Reference**: https://docs.docker.com/compose/
- **Dockerfile Best Practices**: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
- **Docker Hub**: https://hub.docker.com/

**Remember:** Containers should be immutable infrastructure - use environment variables for configuration, never commit secrets, and always use specific version tags.
