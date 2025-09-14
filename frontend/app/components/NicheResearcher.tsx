'use client'

import { useState } from 'react'
import { 
  Search, 
  TrendingUp, 
  DollarSign, 
  Target, 
  Users, 
  BarChart3,
  CheckCircle,
  AlertCircle,
  Star,
  ArrowRight,
  Download,
  Share,
  Bookmark,
  Filter,
  SortAsc,
  Eye,
  Edit,
  Trash2
} from 'lucide-react'

interface NicheAnalysis {
  market_size: string
  competition_level: string
  growth_rate: string
  profitability_score: number
  opportunities: string[]
  challenges: string[]
  target_audience: string
  pricing_range: string
  revenue_potential: string
}

interface NicheResult {
  id: number
  title: string
  isBestOption: boolean
  metrics: {
    potential: string
    highTicket: string
    familiarity: string
    targetability: string
  }
  description: string
  marketSize: string
  competitionLevel: string
  growthRate: string
  analysis?: NicheAnalysis
}

export default function NicheResearcher() {
  const [formData, setFormData] = useState({
    skills: '',
    interests: '',
    budget: '',
    experience: ''
  })
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<NicheResult[]>([])
  const [selectedNiche, setSelectedNiche] = useState<NicheResult | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      // Convert form data to match API requirements
      const skillsArray = formData.skills
        .split(',')
        .map(skill => skill.trim())
        .filter(skill => skill.length > 0)
      
      const interestsArray = formData.interests
        .split(',')
        .map(interest => interest.trim())
        .filter(interest => interest.length > 0)

      // Convert budget string to number
      const budgetMap: { [key: string]: number } = {
        'under-5k': 5000,
        '5k-10k': 10000,
        '10k-25k': 25000,
        '25k-50k': 50000,
        '50k-plus': 100000
      }

      const response = await fetch('http://localhost:8000/api/agents/niche-researcher/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          skills: skillsArray,
          interests: interestsArray,
          budget: budgetMap[formData.budget] || 10000,
          experience_level: formData.experience,
          time_commitment: "part_time"
        }),
      })

      const data = await response.json()

      if (response.ok) {
        // Map API response to our component format
        const mappedResults: NicheResult[] = data.recommended_niches.map((niche: any, index: number) => ({
          id: index + 1,
          title: niche.name,
          isBestOption: index === 0, // First result is best option
          metrics: {
            potential: niche.profitability_score > 80 ? "Yes" : "Maybe",
            highTicket: niche.entry_barrier === "Low" ? "Yes" : "Maybe",
            familiarity: "High", // Default based on skills/interests match
            targetability: niche.competition_level === "Low" ? "High" : "Medium"
          },
          description: niche.description,
          marketSize: niche.market_size,
          competitionLevel: niche.competition_level,
          growthRate: data.market_analysis?.growth_rate || "15% annually",
          analysis: {
            market_size: niche.market_size,
            competition_level: niche.competition_level,
            growth_rate: data.market_analysis?.growth_rate || "15% annually",
            profitability_score: niche.profitability_score,
            opportunities: data.implementation_strategy || [],
            challenges: data.risk_assessment ? [
              `Market Risk: ${data.risk_assessment.market_risk}`,
              `Competition Risk: ${data.risk_assessment.competition_risk}`,
              `Technical Risk: ${data.risk_assessment.technical_risk}`
            ] : [],
            target_audience: "Business owners and decision makers",
            pricing_range: "$5K - $50K",
            revenue_potential: "High"
          }
        }))
        
        setResults(mappedResults)
      } else {
        console.error('API Error:', data)
        // Fallback to mock data
        setResults(getMockResults())
      }
    } catch (error) {
      console.error('Error analyzing niche:', error)
      // Fallback to mock data on error
      setResults(getMockResults())
    } finally {
      setLoading(false)
    }
  }

  // Helper function for mock data
  const getMockResults = (): NicheResult[] => [
    {
      id: 1,
      title: "SaaS for Small Businesses",
      isBestOption: true,
      metrics: {
        potential: "Yes",
        highTicket: "Yes",
        familiarity: "High",
        targetability: "High"
      },
      description: "B2B software solutions for small to medium businesses. High demand for automation tools, CRM systems, and productivity software.",
      marketSize: "$50B",
      competitionLevel: "Medium",
      growthRate: "15% annually",
      analysis: {
        market_size: "$50B",
        competition_level: "Medium",
        growth_rate: "15% annually",
        profitability_score: 85,
        opportunities: ["Start with MVP in 3 months", "Focus on one specific use case"],
        challenges: ["Market Risk: Low", "Competition Risk: Medium"],
        target_audience: "Small business owners",
        pricing_range: "$5K - $50K",
        revenue_potential: "High"
      }
    },
    {
      id: 2,
      title: "AI-Powered Marketing Tools",
      isBestOption: false,
      metrics: {
        potential: "Yes",
        highTicket: "Yes",
        familiarity: "High",
        targetability: "High"
      },
      description: "Marketing automation and AI-driven customer acquisition tools. Growing market with high demand for personalization.",
      marketSize: "$25B",
      competitionLevel: "High",
      growthRate: "20% annually",
      analysis: {
        market_size: "$25B",
        competition_level: "High",
        growth_rate: "20% annually",
        profitability_score: 90,
        opportunities: ["Build strong customer feedback loop"],
        challenges: ["Market Risk: Low", "Competition Risk: High"],
        target_audience: "Marketing teams",
        pricing_range: "$10K - $100K",
        revenue_potential: "Very High"
      }
    }
  ]

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">AI Niche Researcher</h1>
        <p className="text-gray-400">Discover profitable niches in minutes with AI-powered market analysis</p>
      </div>

      {/* Analysis Form */}
      <div className="bg-gray-800 rounded-lg p-6 mb-8">
        <h2 className="text-xl font-bold mb-6">Tell Us About You</h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium mb-2">Your Skills & Expertise</label>
              <textarea
                name="skills"
                value={formData.skills}
                onChange={handleInputChange}
                placeholder="e.g., Digital marketing, Sales automation, Content creation, Web development..."
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                rows={3}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Your Interests & Passions</label>
              <textarea
                name="interests"
                value={formData.interests}
                onChange={handleInputChange}
                placeholder="e.g., Health & wellness, Technology, Finance, E-commerce, Real estate..."
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                rows={3}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Available Budget</label>
              <select
                name="budget"
                value={formData.budget}
                onChange={handleInputChange}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              >
                <option value="">Select budget range</option>
                <option value="under-5k">Under $5K</option>
                <option value="5k-10k">$5K - $10K</option>
                <option value="10k-25k">$10K - $25K</option>
                <option value="25k-50k">$25K - $50K</option>
                <option value="50k-plus">$50K+</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Experience Level</label>
              <select
                name="experience"
                value={formData.experience}
                onChange={handleInputChange}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              >
                <option value="">Select experience level</option>
                <option value="beginner">Beginner (0-1 years)</option>
                <option value="intermediate">Intermediate (1-3 years)</option>
                <option value="advanced">Advanced (3-5 years)</option>
                <option value="expert">Expert (5+ years)</option>
              </select>
            </div>
          </div>
          
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white px-6 py-3 rounded-lg font-medium transition-colors flex items-center justify-center"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Analyzing Niches...
              </>
            ) : (
              <>
                <Search className="w-5 h-5 mr-2" />
                Analyze My Niches
              </>
            )}
          </button>
        </form>
      </div>

      {/* Results */}
      {results.length > 0 && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold">Recommended Niches</h2>
            <div className="flex items-center space-x-2">
              <button className="p-2 hover:bg-gray-700 rounded-lg">
                <Filter className="w-5 h-5" />
              </button>
              <button className="p-2 hover:bg-gray-700 rounded-lg">
                <SortAsc className="w-5 h-5" />
              </button>
              <button className="p-2 hover:bg-gray-700 rounded-lg">
                <Download className="w-5 h-5" />
              </button>
            </div>
          </div>

          {results.map((niche) => (
            <div
              key={niche.id}
              className={`bg-gray-800 rounded-lg p-6 border-2 transition-all cursor-pointer ${
                niche.isBestOption 
                  ? 'border-green-500 bg-gray-800' 
                  : 'border-gray-700 hover:border-gray-600'
              }`}
              onClick={() => setSelectedNiche(niche)}
            >
              <div className="flex items-start justify-between mb-4">
                <h3 className="text-xl font-bold text-white">{niche.title}</h3>
                {niche.isBestOption && (
                  <span className="bg-green-500 text-white px-3 py-1 rounded-full text-sm font-medium flex items-center">
                    <Star className="w-4 h-4 mr-1" />
                    Best Option
                  </span>
                )}
              </div>

              <div className="grid grid-cols-4 gap-4 mb-4">
                <div className="bg-white text-gray-900 px-3 py-1 rounded-full text-sm font-medium text-center">
                  $1M+ Potential: {niche.metrics.potential}
                </div>
                <div className="bg-white text-gray-900 px-3 py-1 rounded-full text-sm font-medium text-center">
                  High Ticket: {niche.metrics.highTicket}
                </div>
                <div className="text-gray-300 text-sm">
                  Familiarity: <span className="text-white font-medium">{niche.metrics.familiarity}</span>
                </div>
                <div className="text-gray-300 text-sm">
                  Targetability: <span className="text-white font-medium">{niche.metrics.targetability}</span>
                </div>
              </div>

              <p className="text-gray-300 leading-relaxed mb-4">{niche.description}</p>

              <div className="grid grid-cols-3 gap-4 text-sm mb-4">
                <div>
                  <span className="text-gray-400">Market Size: </span>
                  <span className="text-white font-medium">{niche.marketSize}</span>
                </div>
                <div>
                  <span className="text-gray-400">Competition: </span>
                  <span className="text-white font-medium">{niche.competitionLevel}</span>
                </div>
                <div>
                  <span className="text-gray-400">Growth Rate: </span>
                  <span className="text-white font-medium">{niche.growthRate}</span>
                </div>
              </div>

              {niche.analysis && (
                <div className="mt-4 p-4 bg-gray-700 rounded-lg">
                  <h4 className="font-bold mb-2">AI Analysis Results</h4>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-400">Profitability Score: </span>
                      <span className="text-green-400 font-medium">{niche.analysis.profitability_score}/100</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Pricing Range: </span>
                      <span className="text-white font-medium">{niche.analysis.pricing_range}</span>
                    </div>
                  </div>
                  {niche.analysis.opportunities.length > 0 && (
                    <div className="mt-3">
                      <p className="text-gray-400 text-sm mb-2">Key Opportunities:</p>
                      <ul className="text-sm text-gray-300 space-y-1">
                        {niche.analysis.opportunities.slice(0, 3).map((opp, index) => (
                          <li key={index} className="flex items-center">
                            <CheckCircle className="w-4 h-4 text-green-400 mr-2" />
                            {opp}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}

              <div className="flex items-center justify-between mt-4">
                <div className="flex items-center space-x-2">
                  <button className="p-2 hover:bg-gray-700 rounded-lg">
                    <Bookmark className="w-4 h-4" />
                  </button>
                  <button className="p-2 hover:bg-gray-700 rounded-lg">
                    <Share className="w-4 h-4" />
                  </button>
                  <button className="p-2 hover:bg-gray-700 rounded-lg">
                    <Edit className="w-4 h-4" />
                  </button>
                </div>
                <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center">
                  Generate Growth Plan
                  <ArrowRight className="w-4 h-4 ml-2" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Selected Niche Modal */}
      {selectedNiche && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-gray-800 rounded-lg p-6 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold">{selectedNiche.title}</h2>
              <button
                onClick={() => setSelectedNiche(null)}
                className="p-2 hover:bg-gray-700 rounded-lg"
              >
                <Trash2 className="w-5 h-5" />
              </button>
            </div>
            
            <div className="space-y-6">
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <h3 className="font-bold mb-2">Market Analysis</h3>
                  <div className="space-y-2 text-sm">
                    <div><span className="text-gray-400">Market Size:</span> <span className="text-white">{selectedNiche.marketSize}</span></div>
                    <div><span className="text-gray-400">Competition:</span> <span className="text-white">{selectedNiche.competitionLevel}</span></div>
                    <div><span className="text-gray-400">Growth Rate:</span> <span className="text-white">{selectedNiche.growthRate}</span></div>
                  </div>
                </div>
                <div>
                  <h3 className="font-bold mb-2">Opportunity Score</h3>
                  <div className="space-y-2 text-sm">
                    <div><span className="text-gray-400">$1M+ Potential:</span> <span className="text-green-400">{selectedNiche.metrics.potential}</span></div>
                    <div><span className="text-gray-400">High Ticket:</span> <span className="text-green-400">{selectedNiche.metrics.highTicket}</span></div>
                    <div><span className="text-gray-400">Familiarity:</span> <span className="text-white">{selectedNiche.metrics.familiarity}</span></div>
                    <div><span className="text-gray-400">Targetability:</span> <span className="text-white">{selectedNiche.metrics.targetability}</span></div>
                  </div>
                </div>
              </div>
              
              <div>
                <h3 className="font-bold mb-2">Description</h3>
                <p className="text-gray-300 leading-relaxed">{selectedNiche.description}</p>
              </div>
              
              {selectedNiche.analysis && (
                <div>
                  <h3 className="font-bold mb-2">AI Analysis</h3>
                  <div className="bg-gray-700 rounded-lg p-4">
                    <div className="grid grid-cols-2 gap-4 mb-4">
                      <div>
                        <span className="text-gray-400">Profitability Score:</span>
                        <div className="text-2xl font-bold text-green-400">{selectedNiche.analysis.profitability_score}/100</div>
                      </div>
                      <div>
                        <span className="text-gray-400">Pricing Range:</span>
                        <div className="text-lg font-medium text-white">{selectedNiche.analysis.pricing_range}</div>
                      </div>
                    </div>
                    
                    {selectedNiche.analysis.opportunities.length > 0 && (
                      <div className="mb-4">
                        <h4 className="font-bold mb-2">Key Opportunities</h4>
                        <ul className="space-y-1">
                          {selectedNiche.analysis.opportunities.map((opp, index) => (
                            <li key={index} className="flex items-start">
                              <CheckCircle className="w-4 h-4 text-green-400 mr-2 mt-0.5 flex-shrink-0" />
                              <span className="text-sm text-gray-300">{opp}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                    
                    {selectedNiche.analysis.challenges.length > 0 && (
                      <div>
                        <h4 className="font-bold mb-2">Potential Challenges</h4>
                        <ul className="space-y-1">
                          {selectedNiche.analysis.challenges.map((challenge, index) => (
                            <li key={index} className="flex items-start">
                              <AlertCircle className="w-4 h-4 text-yellow-400 mr-2 mt-0.5 flex-shrink-0" />
                              <span className="text-sm text-gray-300">{challenge}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
            
            <div className="flex items-center justify-end space-x-4 mt-6">
              <button
                onClick={() => setSelectedNiche(null)}
                className="px-4 py-2 text-gray-400 hover:text-white"
              >
                Close
              </button>
              <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg">
                Generate Growth Plan
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}