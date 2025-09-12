# Inno Supps - AI-Powered B2B Growth System

A complete AI-powered B2B growth system that mirrors the functionality of AI Clients, featuring multiple AI agents for niche research, cold email generation, and growth automation.

## 🚀 Features

### AI Agents
- **Niche Researcher** - AI-powered market analysis and niche discovery
- **Cold Email Writer** - Personalized cold email generation with high conversion rates
- **SDR (Sales Development Representative)** - Automated reply and booking agent
- **Ad Writer** - AI-generated ad copy for multiple platforms
- **Sales Call Analyzer** - Call analysis and insights
- **Growth Consultant** - Strategic growth recommendations
- **Growth Plan Creator** - Comprehensive growth strategy development
- **Cold Email Campaign Agent** - End-to-end campaign management
- **Compliance Checker** - FDA and FTC compliance validation

### Technical Stack
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python
- **Database**: PostgreSQL with pgvector for embeddings
- **AI**: OpenAI GPT-4 integration
- **Caching**: Redis for queues and rate limiting
- **Automation**: n8n workflow integration
- **Messaging**: Slack bot integration

## 🛠️ Quick Start

### Prerequisites
- Node.js 18+
- Python 3.8+
- Docker (optional)
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/simd-personal/Inno-Supps.git
   cd Inno-Supps
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Install dependencies**
   ```bash
   # Frontend
   cd frontend
   npm install
   
   # Backend
   cd ../backend
   pip install -r requirements.txt
   ```

4. **Start the application**
   ```bash
   # Start API server
   python simple_ai_api.py
   
   # Start frontend (in new terminal)
   cd frontend
   npm run dev
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - API: http://localhost:8000

## 📁 Project Structure

```
inno-supps/
├── frontend/                 # Next.js frontend application
│   ├── app/                 # App router pages and components
│   │   ├── components/      # React components
│   │   ├── page.tsx         # Main page
│   │   └── layout.tsx       # Root layout
│   ├── package.json         # Frontend dependencies
│   └── tailwind.config.js   # Tailwind configuration
├── backend/                 # FastAPI backend
│   ├── routes/              # API route handlers
│   ├── services/            # Business logic services
│   ├── database.py          # Database models
│   └── requirements.txt     # Python dependencies
├── simple_ai_api.py         # Simplified API server
├── docker-compose.yml       # Docker orchestration
├── .env.example            # Environment variables template
└── README.md               # This file
```

## 🎯 Usage

### Cold Email Writer
1. Navigate to "Cold Email Writer" in the sidebar
2. Fill in prospect information (name, company, role, industry, etc.)
3. Select campaign type (initial, follow-up, re-engagement)
4. Click "Generate Cold Email" to create personalized content
5. Review personalization score and reply probability
6. Copy or export the generated email

### Niche Researcher
1. Go to "Niche Researcher" in the sidebar
2. Enter your skills, interests, budget, and experience level
3. Click "Analyze My Niches" to get AI-powered market analysis
4. Review profitability scores, opportunities, and challenges
5. Generate growth plans for promising niches

### Dashboard
- View campaign performance metrics
- Track email open rates and reply rates
- Monitor meeting bookings and revenue
- Access recent activity and analytics

## 🔧 Development

### Adding New AI Agents
1. Create agent logic in `backend/services/ai_agents.py`
2. Add API routes in `backend/routes/ai_agents.py`
3. Create frontend component in `frontend/app/components/`
4. Add navigation item in `frontend/app/page.tsx`

### Database Setup
```bash
# Start PostgreSQL with Docker
docker run --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15

# Run migrations
cd backend
alembic upgrade head

# Seed database
python scripts/seed_data.py
```

## 🚀 Deployment

### Docker Deployment
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Production Deployment
1. Set up PostgreSQL database
2. Configure environment variables
3. Deploy backend to your preferred platform
4. Deploy frontend to Vercel/Netlify
5. Set up domain and SSL certificates

## 📝 API Documentation

### Endpoints
- `GET /health` - Health check
- `GET /api/agents/dashboard/analytics` - Dashboard metrics
- `GET /api/agents/campaigns` - Campaign data
- `POST /api/agents/niche-researcher/analyze` - Niche analysis
- `POST /api/agents/cold-email-writer/generate` - Generate cold emails

### Example API Usage
```bash
# Generate cold email
curl -X POST http://localhost:8000/api/agents/cold-email-writer/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prospect_info": {
      "name": "John Smith",
      "company": "TechCorp",
      "role": "VP of Marketing",
      "industry": "SaaS"
    },
    "campaign_type": "initial"
  }'
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by AI Clients platform
- Built with Next.js and FastAPI
- Powered by OpenAI GPT-4
- UI components from Lucide React

## 📞 Support

For support, email simba@inno-supps.com or create an issue in this repository.

---

**Built with ❤️ by Simba**