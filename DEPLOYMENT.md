# Deployment & Configuration Guide

## Environment Configuration

### Local Development Setup

#### Step 1: Create `.env` File
```bash
# Create the file
touch .env

# Add your OpenAI API key
echo OPENAI_API_KEY=sk-your-key-here >> .env
```

#### Step 2: Configure Environment Variables
```env
# Required
OPENAI_API_KEY=sk-your-openai-api-key

# Optional: LLM Configuration
LLM_MODEL=gpt-3.5-turbo          # Model name
LLM_TEMPERATURE=0.7              # 0-1, higher = more creative
LLM_MAX_TOKENS=2000              # Max response length

# Optional: Server Configuration
SERVER_HOST=0.0.0.0              # Server host
SERVER_PORT=8000                 # Server port
DEBUG=True                        # Debug mode
```

### Variables Explanation

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | Required | Your OpenAI API key from https://platform.openai.com |
| `LLM_MODEL` | gpt-3.5-turbo | Model to use (supports: gpt-3.5-turbo, gpt-4) |
| `LLM_TEMPERATURE` | 0.7 | Sampling temperature (0=deterministic, 1=creative) |
| `LLM_MAX_TOKENS` | 2000 | Maximum tokens in response |
| `SERVER_HOST` | 0.0.0.0 | Server host address |
| `SERVER_PORT` | 8000 | Server port |
| `DEBUG` | True | Enable debug mode (False for production) |

---

## Installation Variants

### Standard Installation
```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate
venv\Scripts\activate    # Windows
# or
source venv/bin/activate # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure .env
cp .env.example .env
# Edit .env and add your OpenAI API key

# 5. Run server
python main.py
```

### Using Poetry
```bash
# Install poetry (if not already installed)
pip install poetry

# Install dependencies
poetry install

# Run server
poetry run python main.py
```

### Using Docker (Recommended for Production)
```bash
# Build Docker image
docker build -t legal-drafting-llm .

# Run container
docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY=sk-your-key \
  --name legal-drafting-api \
  legal-drafting-llm
```

**Dockerfile** (create this file):
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Running the Server

### Development Mode (with auto-reload)
```bash
python main.py
```

### Production Mode (no auto-reload)
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Custom Port
```bash
uvicorn main:app --port 8001
```

### With Logging to File
```bash
python main.py > app.log 2>&1 &
```

---

## Production Deployment

### Recommended Setup
```
Client Request
    ↓
[Nginx/HAProxy] - Reverse Proxy & Load Balancer
    ↓
[Gunicorn/Uvicorn] - ASGI Server (Multiple Workers)
    ↓
[Legal Drafting App] - Main Application
    ↓
[Redis] - Caching Layer
    ↓
[OpenAI API] - LLM Service
```

### Using Gunicorn (Production)
```bash
# Install gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

# Run with more configuration
gunicorn \
  -w 8 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  main:app
```

### Using Systemd Service (Linux)
Create `/etc/systemd/system/legal-drafting.service`:
```ini
[Unit]
Description=Legal Document Drafting LLM Engine
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/opt/legal-drafting-llm
Environment="PATH=/opt/legal-drafting-llm/venv/bin"
ExecStart=/opt/legal-drafting-llm/venv/bin/gunicorn \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind unix:legal-drafting.sock \
  main:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable legal-drafting
sudo systemctl start legal-drafting
```

### Nginx Configuration
```nginx
upstream legal_drafting {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    # SSL Configuration (recommended)
    # listen 443 ssl http2;
    # ssl_certificate /path/to/cert.pem;
    # ssl_certificate_key /path/to/key.pem;

    client_max_body_size 10M;
    proxy_connect_timeout 120s;
    proxy_send_timeout 120s;
    proxy_read_timeout 120s;

    location / {
        proxy_pass http://legal_drafting;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /opt/legal-drafting-llm/static/;
    }
}
```

---

## Monitoring & Logging

### View Logs
```bash
# Real-time logs
tail -f logs/app.log

# Last 100 lines
tail -100 logs/app.log

# Search logs
grep ERROR logs/app.log
```

### Log Format
```
2024-01-01 12:00:00,123 - src.llm_config - INFO - LLM Config initialized with model: gpt-3.5-turbo
2024-01-01 12:00:01,234 - main - INFO - Received draft request: Draft a Loan Agreement...
2024-01-01 12:00:05,567 - main - INFO - Document generated: ./outputs/Loan-Agreement_20240101_120000.docx
```

### Setting Log Levels
Edit `main.py`:
```python
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more verbose output
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("./logs/app.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
```

---

## Database Integration (Optional)

### Using SQLite (Simple)
```python
# Add to requirements.txt
sqlalchemy==2.0.0
```

### Using PostgreSQL (Production)
```python
# Add to requirements.txt
sqlalchemy==2.0.0
psycopg2-binary==2.9.0
```

### Connection String
```env
DATABASE_URL=postgresql://user:password@localhost:5432/legal_db
```

---

## Caching Configuration (Optional)

### Using Redis
```bash
# Install Redis
# Windows: Use Windows Subsystem for Linux
# Linux: sudo apt-get install redis-server
# Mac: brew install redis

# Add to requirements.txt
redis==5.0.0

# Configure in main.py
from redis import Redis

redis_client = Redis(host='localhost', port=6379, db=0)
```

---

## Security Best Practices

### 1. Environment Variables
```bash
# ✓ Good: Use .env file (never commit to git)
OPENAI_API_KEY=sk-...

# ✗ Bad: Hardcode in source files
api_key = "sk-..."
```

### 2. API Authentication
Add to requirements.txt:
```
python-jose==3.3.0
passlib==1.7.4
```

Implement in main.py:
```python
from fastapi.security import APIKeyHeader
from fastapi import HTTPException, Depends

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key
```

### 3. Rate Limiting
Add to requirements.txt:
```
slowapi==0.1.8
```

Implement in main.py:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/draft-document")
@limiter.limit("5/minute")
async def draft_document(request: Request, ...):
    # Implementation
```

### 4. HTTPS/SSL
```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
}
```

### 5. CORS Configuration
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific origins
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)
```

---

## Backup & Recovery

### Backup Generated Documents
```bash
# Windows
copy outputs\* backup\documents\

# Linux/Mac
cp outputs/* backup/documents/
```

### Backup Configuration
```bash
# Backup .env file (securely)
cp .env backup/.env.backup
```

---

## Troubleshooting

### Issue: Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000          # Linux/Mac
netstat -ano | grep :8000  # Windows

# Kill process
kill -9 <PID>          # Linux/Mac
taskkill /PID <PID> /F # Windows

# Use different port
uvicorn main:app --port 8001
```

### Issue: OpenAI API Rate Limit
```
Error: openai.error.RateLimitError: Rate limit exceeded
```
**Solution**:
1. Check billing at https://platform.openai.com/account/billing
2. Implement exponential backoff
3. Use caching for repeated requests

### Issue: Out of Memory
**Solutions**:
1. Reduce `LLM_MAX_TOKENS` (default: 2000)
2. Use smaller model (`gpt-3.5-turbo` instead of `gpt-4`)
3. Increase server memory
4. Implement queue system for concurrent requests

### Issue: Slow Response Times
**Solutions**:
1. Check OpenAI API status
2. Implement caching
3. Use async processing
4. Reduce prompt complexity

---

## Performance Tuning

### LLM Configuration
```env
# Faster responses (less accurate)
LLM_TEMPERATURE=0.5
LLM_MAX_TOKENS=1000

# Slower but more accurate
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000
```

### Server Configuration
```bash
# More worker processes
gunicorn -w 8 main:app

# Increase thread pool
uvicorn main:app --workers 4
```

### Database Optimization
```python
# Add indexes for frequent queries
# Implement query result caching
# Use read replicas for scaling
```

---

## Scaling

### Horizontal Scaling
```
Load Balancer
    ↓
├─ Instance 1 (Port 8000)
├─ Instance 2 (Port 8001)
└─ Instance 3 (Port 8002)
    ↓
Shared Database
Shared File Storage
```

### Vertical Scaling
1. Increase server RAM
2. Increase CPU cores
3. Use faster storage (SSD)
4. Upgrade to higher-tier OpenAI models

---

## Monitoring

### Health Checks
```bash
# Continuous health monitoring
while true; do
  curl http://localhost:8000/health
  sleep 60
done
```

### Metrics to Track
- Request count per minute
- Average response time
- Error rate
- API token usage
- Document generation success rate
- Storage usage

### Recommended Tools
- **Prometheus**: Metrics collection
- **Grafana**: Metrics visualization
- **ELK Stack**: Centralized logging
- **New Relic**: Application monitoring
- **Sentry**: Error tracking

---

## Cost Optimization

### OpenAI API Costs
- **gpt-3.5-turbo**: ~$0.002 per 1K tokens
- **gpt-4**: ~$0.03 per 1K tokens
- Average document: 1000-2000 tokens

### Cost Reduction Strategies
1. Use `gpt-3.5-turbo` instead of `gpt-4`
2. Implement caching for similar requests
3. Reduce `LLM_MAX_TOKENS`
4. Batch process requests
5. Monitor token usage

---

## Compliance & Legal

### Data Handling
- Implement data retention policies
- Add GDPR compliance
- Ensure PII is handled securely
- Implement audit logging

### Document Generation
- Add disclaimer about legal review
- Implement version control
- Track document modifications
- Maintain audit trail

---

**Deployment Version**: 1.0.0
**Last Updated**: December 2024
