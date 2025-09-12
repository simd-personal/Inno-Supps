# Deployment Guide

## 🚀 Quick Deploy to Cloud

### Prerequisites
- Cloud provider account (AWS, GCP, Azure, DigitalOcean)
- Docker and Docker Compose installed locally
- Domain name (optional)

### 1. Choose Your Cloud Provider

#### AWS (Recommended)
```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure AWS
aws configure
```

#### DigitalOcean (Easiest)
```bash
# Install doctl
snap install doctl
doctl auth init
```

### 2. Create Cloud Resources

#### Database (PostgreSQL with pgvector)
```bash
# AWS RDS
aws rds create-db-instance \
  --db-instance-identifier inno-supps-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username postgres \
  --master-user-password your-secure-password \
  --allocated-storage 20

# DigitalOcean Managed Database
doctl databases create inno-supps-db \
  --engine pg \
  --region nyc1 \
  --size db-s-1vcpu-1gb \
  --num-nodes 1
```

#### Redis Cache
```bash
# AWS ElastiCache
aws elasticache create-cache-cluster \
  --cache-cluster-id inno-supps-redis \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --num-cache-nodes 1

# DigitalOcean Managed Redis
doctl databases create inno-supps-redis \
  --engine redis \
  --region nyc1 \
  --size db-s-1vcpu-1gb
```

### 3. Deploy Application

#### Using Docker Swarm
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.prod.yml inno-supps
```

#### Using Kubernetes
```bash
# Create namespace
kubectl create namespace inno-supps

# Apply configurations
kubectl apply -f k8s/
```

### 4. Configure Environment

Create production environment file:
```bash
# .env.production
DATABASE_URL=postgresql://user:pass@your-db-host:5432/inno_supps
REDIS_URL=redis://your-redis-host:6379
OPENAI_API_KEY=your-openai-key
SLACK_BOT_TOKEN=your-slack-token
N8N_WEBHOOK_SECRET=your-n8n-secret
SECRET_KEY=your-production-secret-key
ENVIRONMENT=production
```

### 5. Run Migrations

```bash
# Connect to your production environment
docker exec -it inno-supps_api_1 python scripts/init_db.py
```

### 6. Set Up Monitoring

#### Health Checks
```bash
# API Health
curl https://your-domain.com/health

# Database Health
curl https://your-domain.com/api/health/db

# Redis Health
curl https://your-domain.com/api/health/redis
```

#### Logging
```bash
# View logs
docker service logs inno-supps_api
docker service logs inno-supps_web
```

## 🔧 Production Configuration

### Security
- Use strong passwords and secrets
- Enable SSL/TLS certificates
- Configure firewall rules
- Set up rate limiting
- Enable CORS properly

### Performance
- Use connection pooling for database
- Configure Redis caching
- Set up CDN for static assets
- Enable gzip compression
- Monitor resource usage

### Monitoring
- Set up application monitoring (DataDog, New Relic)
- Configure log aggregation (ELK stack)
- Set up alerting for critical issues
- Monitor database performance
- Track API usage and errors

## 📊 Scaling

### Horizontal Scaling
```bash
# Scale API service
docker service scale inno-supps_api=3

# Scale web service
docker service scale inno-supps_web=2
```

### Database Scaling
- Read replicas for read-heavy workloads
- Connection pooling
- Query optimization
- Index optimization

### Caching Strategy
- Redis for session storage
- CDN for static assets
- Application-level caching
- Database query caching

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to cloud
        run: |
          # Your deployment commands
          docker build -t inno-supps .
          docker push your-registry/inno-supps
          # Deploy to cloud
```

## 🚨 Troubleshooting

### Common Issues

**Database Connection Failed**
```bash
# Check database status
docker exec -it inno-supps_postgres_1 pg_isready

# Check connection string
echo $DATABASE_URL
```

**Redis Connection Failed**
```bash
# Check Redis status
docker exec -it inno-supps_redis_1 redis-cli ping

# Check Redis logs
docker logs inno-supps_redis_1
```

**API Not Responding**
```bash
# Check API logs
docker logs inno-supps_api_1

# Check API health
curl http://localhost:8000/health
```

**Frontend Build Failed**
```bash
# Check build logs
docker logs inno-supps_web_1

# Rebuild frontend
docker-compose build web
```

### Recovery Procedures

**Database Recovery**
```bash
# Backup database
docker exec inno-supps_postgres_1 pg_dump -U postgres inno_supps > backup.sql

# Restore database
docker exec -i inno-supps_postgres_1 psql -U postgres inno_supps < backup.sql
```

**Application Recovery**
```bash
# Restart all services
docker-compose restart

# Rebuild and restart
docker-compose down
docker-compose up --build -d
```

## 📈 Performance Optimization

### Database Optimization
- Add indexes for frequently queried columns
- Use connection pooling
- Optimize queries
- Regular maintenance

### Application Optimization
- Enable caching
- Optimize Docker images
- Use multi-stage builds
- Minimize dependencies

### Infrastructure Optimization
- Use load balancers
- Configure auto-scaling
- Monitor resource usage
- Optimize network configuration

## 🔐 Security Checklist

- [ ] Strong passwords and secrets
- [ ] SSL/TLS certificates
- [ ] Firewall configuration
- [ ] Rate limiting enabled
- [ ] CORS properly configured
- [ ] Input validation
- [ ] SQL injection prevention
- [ ] XSS protection
- [ ] CSRF protection
- [ ] Regular security updates
- [ ] Monitoring and alerting
- [ ] Backup and recovery procedures
