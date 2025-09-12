'use client'

import { useState } from 'react'
import { 
  Mail, 
  User, 
  Building, 
  Target, 
  Send, 
  Copy, 
  RefreshCw, 
  Star, 
  TrendingUp,
  CheckCircle,
  AlertCircle,
  Eye,
  Edit,
  Save,
  Download,
  Share,
  MoreVertical,
  Plus,
  Trash2,
  ArrowRight,
  Clock,
  MessageSquare,
  BarChart3
} from 'lucide-react'

interface ColdEmail {
  id?: number
  subject: string
  body: string
  personalization_score: number
  reply_probability: number
  tone: string
  compliance_notes: string
  follow_up_sequence: Array<{
    day: number
    subject: string
    body: string
    purpose: string
  }>
}

interface ProspectInfo {
  name: string
  company: string
  role: string
  industry: string
  recent_activity: string
  pain_points: string
  email: string
}

export default function ColdEmailWriter() {
  const [prospectInfo, setProspectInfo] = useState<ProspectInfo>({
    name: '',
    company: '',
    role: '',
    industry: '',
    recent_activity: '',
    pain_points: '',
    email: ''
  })
  const [campaignType, setCampaignType] = useState('initial')
  const [loading, setLoading] = useState(false)
  const [generatedEmail, setGeneratedEmail] = useState<ColdEmail | null>(null)
  const [savedEmails, setSavedEmails] = useState<ColdEmail[]>([])
  const [showFollowUps, setShowFollowUps] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await fetch('http://localhost:8000/api/agents/cold-email-writer/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prospect_info: prospectInfo,
          campaign_type: campaignType
        }),
      })

      const data = await response.json()

      if (data.success) {
        setGeneratedEmail(data.data)
      }
    } catch (error) {
      console.error('Error generating cold email:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setProspectInfo({
      ...prospectInfo,
      [e.target.name]: e.target.value
    })
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    // You could add a toast notification here
  }

  const saveEmail = () => {
    if (generatedEmail) {
      setSavedEmails([...savedEmails, { ...generatedEmail, id: Date.now() }])
    }
  }

  const regenerateEmail = () => {
    handleSubmit(new Event('submit') as any)
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">AI Cold Email Writer</h1>
        <p className="text-gray-400">Generate personalized cold emails that actually convert</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Prospect Information Form */}
        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-bold mb-6 flex items-center">
            <User className="w-5 h-5 mr-2" />
            Prospect Information
          </h2>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Name</label>
                <input
                  type="text"
                  name="name"
                  value={prospectInfo.name}
                  onChange={handleInputChange}
                  placeholder="John Smith"
                  className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Company</label>
                <input
                  type="text"
                  name="company"
                  value={prospectInfo.company}
                  onChange={handleInputChange}
                  placeholder="TechCorp Inc."
                  className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Role</label>
                <input
                  type="text"
                  name="role"
                  value={prospectInfo.role}
                  onChange={handleInputChange}
                  placeholder="VP of Marketing"
                  className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Industry</label>
                <input
                  type="text"
                  name="industry"
                  value={prospectInfo.industry}
                  onChange={handleInputChange}
                  placeholder="SaaS"
                  className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Email</label>
              <input
                type="email"
                name="email"
                value={prospectInfo.email}
                onChange={handleInputChange}
                placeholder="john@techcorp.com"
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Recent Activity</label>
              <textarea
                name="recent_activity"
                value={prospectInfo.recent_activity}
                onChange={handleInputChange}
                placeholder="e.g., Just raised Series B funding, expanding sales team, launched new product..."
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                rows={3}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Pain Points</label>
              <textarea
                name="pain_points"
                value={prospectInfo.pain_points}
                onChange={handleInputChange}
                placeholder="e.g., Struggling with lead generation, low conversion rates, manual processes..."
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                rows={3}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Campaign Type</label>
              <select
                value={campaignType}
                onChange={(e) => setCampaignType(e.target.value)}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="initial">Initial Outreach</option>
                <option value="follow_up">Follow-up</option>
                <option value="re_engagement">Re-engagement</option>
                <option value="referral">Referral</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white px-6 py-3 rounded-lg font-medium transition-colors flex items-center justify-center"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Generating Email...
                </>
              ) : (
                <>
                  <Mail className="w-5 h-5 mr-2" />
                  Generate Cold Email
                </>
              )}
            </button>
          </form>
        </div>

        {/* Generated Email */}
        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold flex items-center">
              <Mail className="w-5 h-5 mr-2" />
              Generated Email
            </h2>
            {generatedEmail && (
              <div className="flex items-center space-x-2">
                <button
                  onClick={regenerateEmail}
                  className="p-2 hover:bg-gray-700 rounded-lg"
                  title="Regenerate"
                >
                  <RefreshCw className="w-4 h-4" />
                </button>
                <button
                  onClick={saveEmail}
                  className="p-2 hover:bg-gray-700 rounded-lg"
                  title="Save"
                >
                  <Save className="w-4 h-4" />
                </button>
                <button
                  onClick={() => copyToClipboard(generatedEmail.body)}
                  className="p-2 hover:bg-gray-700 rounded-lg"
                  title="Copy"
                >
                  <Copy className="w-4 h-4" />
                </button>
              </div>
            )}
          </div>

          {generatedEmail ? (
            <div className="space-y-6">
              {/* Email Preview */}
              <div className="bg-gray-700 rounded-lg p-4">
                <div className="mb-4">
                  <div className="text-sm text-gray-400 mb-1">To: {prospectInfo.email}</div>
                  <div className="text-sm text-gray-400 mb-1">From: you@yourcompany.com</div>
                  <div className="text-sm text-gray-400 mb-3">Subject: {generatedEmail.subject}</div>
                </div>
                <div className="text-gray-300 whitespace-pre-wrap">
                  {generatedEmail.body}
                </div>
              </div>

              {/* Performance Metrics */}
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-gray-700 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-400">Personalization Score</span>
                    <Star className="w-4 h-4 text-yellow-400" />
                  </div>
                  <div className="text-2xl font-bold text-yellow-400">
                    {generatedEmail.personalization_score}/100
                  </div>
                </div>
                <div className="bg-gray-700 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-400">Reply Probability</span>
                    <TrendingUp className="w-4 h-4 text-green-400" />
                  </div>
                  <div className="text-2xl font-bold text-green-400">
                    {generatedEmail.reply_probability}%
                  </div>
                </div>
              </div>

              {/* Tone and Compliance */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <span className="text-sm text-gray-400">Tone:</span>
                  <div className="text-white font-medium">{generatedEmail.tone}</div>
                </div>
                <div>
                  <span className="text-sm text-gray-400">Compliance:</span>
                  <div className="text-green-400 font-medium flex items-center">
                    <CheckCircle className="w-4 h-4 mr-1" />
                    Compliant
                  </div>
                </div>
              </div>

              {/* Compliance Notes */}
              {generatedEmail.compliance_notes && (
                <div className="bg-green-900 bg-opacity-20 border border-green-500 rounded-lg p-4">
                  <div className="flex items-start">
                    <CheckCircle className="w-5 h-5 text-green-400 mr-2 mt-0.5" />
                    <div>
                      <h4 className="font-medium text-green-400 mb-1">Compliance Notes</h4>
                      <p className="text-sm text-gray-300">{generatedEmail.compliance_notes}</p>
                    </div>
                  </div>
                </div>
              )}

              {/* Follow-up Sequence */}
              {generatedEmail.follow_up_sequence.length > 0 && (
                <div>
                  <button
                    onClick={() => setShowFollowUps(!showFollowUps)}
                    className="flex items-center text-blue-400 hover:text-blue-300 mb-4"
                  >
                    <MessageSquare className="w-4 h-4 mr-2" />
                    View Follow-up Sequence ({generatedEmail.follow_up_sequence.length} emails)
                    <ArrowRight className={`w-4 h-4 ml-2 transition-transform ${showFollowUps ? 'rotate-90' : ''}`} />
                  </button>

                  {showFollowUps && (
                    <div className="space-y-4">
                      {generatedEmail.follow_up_sequence.map((email, index) => (
                        <div key={index} className="bg-gray-700 rounded-lg p-4">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-medium text-blue-400">
                              Day {email.day}
                            </span>
                            <span className="text-xs text-gray-400">{email.purpose}</span>
                          </div>
                          <div className="text-sm text-gray-400 mb-2">Subject: {email.subject}</div>
                          <div className="text-sm text-gray-300 whitespace-pre-wrap">
                            {email.body}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex space-x-4">
                <button className="flex-1 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center justify-center">
                  <Send className="w-4 h-4 mr-2" />
                  Send Email
                </button>
                <button className="flex-1 bg-gray-600 hover:bg-gray-500 text-white px-4 py-2 rounded-lg flex items-center justify-center">
                  <Download className="w-4 h-4 mr-2" />
                  Export
                </button>
              </div>
            </div>
          ) : (
            <div className="text-center text-gray-400 py-12">
              <Mail className="w-12 h-12 mx-auto mb-4 opacity-50" />
              <p>Fill in the prospect information and generate your first cold email</p>
            </div>
          )}
        </div>
      </div>

      {/* Saved Emails */}
      {savedEmails.length > 0 && (
        <div className="mt-8 bg-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-bold mb-6 flex items-center">
            <Save className="w-5 h-5 mr-2" />
            Saved Emails
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {savedEmails.map((email, index) => (
              <div key={index} className="bg-gray-700 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-medium truncate">{email.subject}</h3>
                  <button className="p-1 hover:bg-gray-600 rounded">
                    <MoreVertical className="w-4 h-4" />
                  </button>
                </div>
                <div className="text-sm text-gray-400 mb-2">
                  {email.personalization_score}/100 personalization
                </div>
                <div className="text-sm text-gray-300 line-clamp-3">
                  {email.body.substring(0, 100)}...
                </div>
                <div className="flex items-center justify-between mt-4">
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => copyToClipboard(email.body)}
                      className="p-1 hover:bg-gray-600 rounded"
                    >
                      <Copy className="w-4 h-4" />
                    </button>
                    <button className="p-1 hover:bg-gray-600 rounded">
                      <Edit className="w-4 h-4" />
                    </button>
                  </div>
                  <button className="p-1 hover:bg-gray-600 rounded text-red-400">
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}