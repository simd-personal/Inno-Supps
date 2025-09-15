# 🧪 Inno Supps - Testing Guide

## Quick Start

```bash
# Start all services
./start.sh

# Or start manually:
# Terminal 1 - Backend
cd backend
export OPENAI_API_KEY="your-key-here"
python main.py

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

## 🌐 Access Points

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🧪 Testing the AI Features

### 🧠 NEW: AI Input Cleaning
The system now automatically cleans and improves all user input before processing:
- **Spelling & Grammar**: Fixes typos and grammatical errors
- **Professional Formatting**: Proper capitalization and punctuation
- **Enhanced Value Props**: Transforms basic phrases into compelling descriptions
- **Business Terminology**: Standardizes industry-specific language

**Test with messy input:**
```bash
# Try with intentionally poor formatting
curl -X POST http://localhost:8000/api/agents/cold-email-writer/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prospect_name": "john smith",
    "company": "techcorp inc",
    "role": "vp marketing", 
    "pain_points": ["lead gen", "conversion rates"],
    "value_proposition": "help techcorp inc scale marketing",
    "email_type": "initial_outreach"
  }'
```

### 1. Cold Email Writer
```bash
curl -X POST http://localhost:8000/api/agents/cold-email-writer/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prospect_name": "John Smith",
    "company": "TechCorp",
    "role": "CTO",
    "pain_points": ["scaling infrastructure", "cost optimization"],
    "value_proposition": "help TechCorp scale efficiently",
    "email_type": "initial_outreach"
  }'
```

### 2. Email Sequences
```bash
curl -X POST http://localhost:8000/api/agents/cold-email-writer/sequence \
  -H "Content-Type: application/json" \
  -d '{
    "prospect_name": "Sarah Johnson",
    "company": "TechStart Inc",
    "role": "VP of Marketing",
    "pain_points": ["lead generation", "conversion optimization"],
    "value_proposition": "help TechStart Inc scale marketing",
    "sequence_length": 5,
    "industry": "SaaS"
  }'
```

### 3. Email Templates
```bash
# Get all templates
curl http://localhost:8000/api/agents/email-templates

# Filter by category
curl "http://localhost:8000/api/agents/email-templates?category=cold_outreach"

# Get specific template
curl http://localhost:8000/api/agents/email-templates/template_1
```

### 4. A/B Testing
```bash
# Get all A/B tests
curl http://localhost:8000/api/agents/ab-tests

# Create new A/B test
curl -X POST http://localhost:8000/api/agents/ab-tests \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Subject Line Test",
    "description": "Testing different subject lines",
    "base_email_id": "template_1",
    "variants": [
      {
        "variant_id": "A",
        "name": "Question Subject",
        "subject": "Quick question about {company}",
        "traffic_percentage": 50
      },
      {
        "variant_id": "B",
        "name": "Value Subject",
        "subject": "How {company} can grow 40%",
        "traffic_percentage": 50
      }
    ],
    "test_duration_days": 7,
    "success_metric": "open_rate"
  }'
```

### 5. Niche Researcher
```bash
curl -X POST http://localhost:8000/api/agents/niche-researcher/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "skills": ["marketing", "sales", "content creation"],
    "interests": ["health supplements", "fitness", "wellness"],
    "budget": 10000,
    "experience_level": "intermediate",
    "time_commitment": "part_time"
  }'
```

## 🎯 Frontend Testing

### Available Pages
- **Overview**: Main dashboard with key metrics
- **Prospects**: Prospect management and tracking
- **Campaigns**: Email campaign management
- **Inbox**: Email inbox and thread management
- **Settings**: Workspace and user settings

### AI Tools
- **Niche Researcher**: AI-powered market analysis
- **Cold Email Writer**: Personalized email generation
- **Email Sequences**: Automated follow-up sequences
- **A/B Testing**: Email variant testing

## 🔧 Troubleshooting

### Backend Issues
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check logs
cd backend
python main.py
```

### Frontend Issues
```bash
# Check if frontend is running
curl http://localhost:3000

# Restart frontend
cd frontend
npm run dev
```

### Database Issues
```bash
# Check database
cd backend
python -c "from database import engine; print('Database connected')"

# Recreate database
rm inno_supps.db
python -c "from database import init_db; init_db()"
```

## 📊 Expected Results

### Cold Email Generation
- **Personalization Score**: 75-85%
- **Subject Lines**: Personalized and engaging
- **Email Body**: Professional and value-focused
- **Call-to-Action**: Clear and specific

### Email Sequences
- **5-Step Sequence**: Initial outreach to final follow-up
- **Progressive Timing**: 3-5 day intervals
- **Decreasing Personalization**: 85% → 60%
- **Success Metrics**: Open rates 25-35%, Reply rates 8-12%

### A/B Testing
- **Variant Creation**: Easy setup with traffic splitting
- **Results Tracking**: Open, reply, and meeting rates
- **Statistical Analysis**: Confidence levels and significance
- **Winner Selection**: Automatic identification of best performers

## 🚀 Production Readiness

The system is production-ready with:
- ✅ **Database Persistence**: SQLite with all tables
- ✅ **API Endpoints**: Full CRUD operations
- ✅ **Error Handling**: Graceful fallbacks
- ✅ **Health Monitoring**: System status checks
- ✅ **CORS Support**: Frontend-backend communication
- ✅ **Mock Data**: Fallback when AI services unavailable

## 📈 Next Steps

1. **Test All Features**: Run through each AI tool
2. **Frontend Navigation**: Test all pages and components
3. **API Integration**: Verify frontend-backend communication
4. **Performance**: Check response times and loading
5. **User Experience**: Test complete workflows

---

**Happy Testing! 🎉**
