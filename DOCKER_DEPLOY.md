# Docker Deployment Guide

## 🐳 Quick Start with Docker

### Option 1: Using Docker Compose (Recommended)

1. **Set your API key in `.env` file**:
   ```bash
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

2. **Build and run**:
   ```bash
   docker-compose up -d
   ```

3. **Access the app**:
   - Open http://localhost:3000

4. **Stop the app**:
   ```bash
   docker-compose down
   ```

### Option 2: Using Docker CLI

1. **Build the image**:
   ```bash
   docker build -t rag-chat-app .
   ```

2. **Run the container**:
   ```bash
   docker run -d \
     --name rag-chat \
     -p 3000:3000 \
     -e GOOGLE_API_KEY=your_actual_api_key_here \
     rag-chat-app
   ```

3. **View logs**:
   ```bash
   docker logs -f rag-chat
   ```

4. **Stop the container**:
   ```bash
   docker stop rag-chat
   docker rm rag-chat
   ```

## 🚀 Deployment Options

### Deploy to Cloud Platforms

#### **Google Cloud Run**
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/rag-chat-app

# Deploy to Cloud Run
gcloud run deploy rag-chat-app \
  --image gcr.io/YOUR_PROJECT_ID/rag-chat-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=your_api_key
```

#### **AWS ECS/Fargate**
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker tag rag-chat-app:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/rag-chat-app:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/rag-chat-app:latest
```

#### **Azure Container Instances**
```bash
# Build and push to Azure Container Registry
az acr build --registry YOUR_REGISTRY --image rag-chat-app:latest .

# Deploy to ACI
az container create \
  --resource-group YOUR_RG \
  --name rag-chat-app \
  --image YOUR_REGISTRY.azurecr.io/rag-chat-app:latest \
  --dns-name-label rag-chat \
  --ports 3000 \
  --environment-variables GOOGLE_API_KEY=your_api_key
```

#### **Heroku**
```bash
# Login to Heroku Container Registry
heroku container:login

# Build and push
heroku container:push web -a your-app-name

# Release
heroku container:release web -a your-app-name

# Set environment variable
heroku config:set GOOGLE_API_KEY=your_api_key -a your-app-name
```

#### **Railway.app**
1. Connect your GitHub repository
2. Add environment variable: `GOOGLE_API_KEY`
3. Railway will auto-detect Dockerfile and deploy

#### **Render.com**
1. Create new Web Service from Docker
2. Connect repository
3. Add environment variable: `GOOGLE_API_KEY`
4. Deploy

## 📦 Image Details

- **Base Image**: `node:20-alpine` (lightweight)
- **Size**: ~200MB (optimized)
- **Port**: 3000
- **Health Check**: Included in docker-compose

## 🔧 Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GOOGLE_API_KEY` | Yes | - | Your Google Gemini API key |
| `PORT` | No | 3000 | Server port |
| `EMBEDDING_PROVIDER` | No | google | Embedding provider |
| `SYSTEM_PROMPT` | No | default | Default system prompt |

## 🛠️ Troubleshooting

**Container won't start?**
- Check logs: `docker logs rag-chat`
- Verify API key is set correctly

**Can't access on localhost:3000?**
- Ensure port mapping is correct: `-p 3000:3000`
- Check if port 3000 is already in use

**Out of memory?**
- Increase Docker memory limit in Docker Desktop settings
- Recommended: At least 2GB RAM

## 📝 Production Best Practices

1. **Use secrets management** for API keys (not environment variables)
2. **Enable HTTPS** with a reverse proxy (nginx, Caddy)
3. **Set up monitoring** and logging
4. **Use volume mounts** for persistent data if needed
5. **Implement rate limiting** to prevent abuse
6. **Regular security updates** of base image

## 🔐 Security Notes

- Never commit `.env` file with real API keys
- Use Docker secrets or cloud provider secret managers in production
- Keep base image updated for security patches
- Consider using non-root user in Dockerfile for production
