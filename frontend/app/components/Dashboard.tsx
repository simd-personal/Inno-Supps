'use client'

import { useState, useEffect } from 'react'
import { 
  BarChart3, 
  TrendingUp, 
  Users, 
  DollarSign, 
  Mail, 
  Phone, 
  Calendar,
  Target,
  Clock,
  MessageSquare,
  Eye,
  Reply,
  CheckCircle,
  AlertCircle,
  Star,
  ArrowUp,
  ArrowDown,
  MoreVertical,
  Filter,
  Download,
  Plus,
  Play,
  Pause,
  Edit,
  Trash2
} from 'lucide-react'

interface DashboardStats {
  total_campaigns: number
  active_campaigns: number
  total_emails_sent: number
  average_open_rate: number
  average_reply_rate: number
  meetings_booked: number
  revenue_generated: string
}

interface Campaign {
  id: number
  name: string
  type: string
  contacts: number
  status: string
  sent: number
  opens: string
  replies: string
  meetings: number
  created_at: string
}

interface RecentActivity {
  type: string
  message: string
  timestamp: string
}

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [campaigns, setCampaigns] = useState<Campaign[]>([])
  const [recentActivity, setRecentActivity] = useState<RecentActivity[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const [statsRes, campaignsRes] = await Promise.all([
        fetch('http://localhost:8000/api/agents/dashboard/analytics'),
        fetch('http://localhost:8000/api/agents/campaigns')
      ])
      
      const statsData = await statsRes.json()
      const campaignsData = await campaignsRes.json()
      
      if (statsData.success) {
        setStats(statsData.data)
        setRecentActivity(statsData.data.recent_activity || [])
      }
      
      if (campaignsData.success) {
        setCampaigns(campaignsData.data)
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading dashboard...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
        <p className="text-gray-400">AI-powered growth system overview</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Total Campaigns</p>
              <p className="text-2xl font-bold">{stats?.total_campaigns || 0}</p>
            </div>
            <BarChart3 className="w-8 h-8 text-blue-500" />
          </div>
          <div className="mt-2 flex items-center text-green-500">
            <ArrowUp className="w-4 h-4 mr-1" />
            <span className="text-sm">+12% from last month</span>
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Emails Sent</p>
              <p className="text-2xl font-bold">{stats?.total_emails_sent?.toLocaleString() || 0}</p>
            </div>
            <Mail className="w-8 h-8 text-green-500" />
          </div>
          <div className="mt-2 flex items-center text-green-500">
            <ArrowUp className="w-4 h-4 mr-1" />
            <span className="text-sm">+8% from last week</span>
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Open Rate</p>
              <p className="text-2xl font-bold">{stats?.average_open_rate || 0}%</p>
            </div>
            <Eye className="w-8 h-8 text-yellow-500" />
          </div>
          <div className="mt-2 flex items-center text-green-500">
            <ArrowUp className="w-4 h-4 mr-1" />
            <span className="text-sm">+2.3% from last week</span>
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Meetings Booked</p>
              <p className="text-2xl font-bold">{stats?.meetings_booked || 0}</p>
            </div>
            <Calendar className="w-8 h-8 text-purple-500" />
          </div>
          <div className="mt-2 flex items-center text-green-500">
            <ArrowUp className="w-4 h-4 mr-1" />
            <span className="text-sm">+15% from last week</span>
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Campaigns Table */}
        <div className="lg:col-span-2 bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold">Active Campaigns</h2>
            <div className="flex items-center space-x-2">
              <button className="p-2 hover:bg-gray-700 rounded-lg">
                <Filter className="w-5 h-5" />
              </button>
              <button className="p-2 hover:bg-gray-700 rounded-lg">
                <Download className="w-5 h-5" />
              </button>
              <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center">
                <Plus className="w-4 h-4 mr-2" />
                New Campaign
              </button>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-700">
                  <th className="text-left py-3 px-4">Campaign</th>
                  <th className="text-left py-3 px-4">Type</th>
                  <th className="text-left py-3 px-4">Status</th>
                  <th className="text-left py-3 px-4">Sent</th>
                  <th className="text-left py-3 px-4">Opens</th>
                  <th className="text-left py-3 px-4">Replies</th>
                  <th className="text-left py-3 px-4">Meetings</th>
                  <th className="text-left py-3 px-4">Actions</th>
                </tr>
              </thead>
              <tbody>
                {campaigns.map((campaign) => (
                  <tr key={campaign.id} className="border-b border-gray-700 hover:bg-gray-700">
                    <td className="py-3 px-4">
                      <div>
                        <p className="font-medium">{campaign.name}</p>
                        <p className="text-sm text-gray-400">{campaign.contacts} contacts</p>
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <span className="bg-gray-700 text-gray-300 px-2 py-1 rounded text-sm">
                        {campaign.type}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-1 rounded text-sm ${
                        campaign.status === 'Active' 
                          ? 'bg-green-900 text-green-300' 
                          : campaign.status === 'Scheduled'
                          ? 'bg-yellow-900 text-yellow-300'
                          : 'bg-gray-700 text-gray-300'
                      }`}>
                        {campaign.status}
                      </span>
                    </td>
                    <td className="py-3 px-4">{campaign.sent.toLocaleString()}</td>
                    <td className="py-3 px-4 text-green-400">{campaign.opens}</td>
                    <td className="py-3 px-4 text-blue-400">{campaign.replies}</td>
                    <td className="py-3 px-4 text-purple-400">{campaign.meetings}</td>
                    <td className="py-3 px-4">
                      <div className="flex items-center space-x-2">
                        <button className="p-1 hover:bg-gray-600 rounded">
                          <Play className="w-4 h-4" />
                        </button>
                        <button className="p-1 hover:bg-gray-600 rounded">
                          <Edit className="w-4 h-4" />
                        </button>
                        <button className="p-1 hover:bg-gray-600 rounded">
                          <MoreVertical className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-bold mb-6">Recent Activity</h2>
          <div className="space-y-4">
            {recentActivity.map((activity, index) => (
              <div key={index} className="flex items-start space-x-3">
                <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                  {activity.type === 'email_sent' && <Mail className="w-4 h-4" />}
                  {activity.type === 'meeting_booked' && <Calendar className="w-4 h-4" />}
                  {activity.type === 'reply_received' && <Reply className="w-4 h-4" />}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-300">{activity.message}</p>
                  <p className="text-xs text-gray-500 mt-1">
                    {new Date(activity.timestamp).toLocaleString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Performance Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-bold mb-6">Campaign Performance</h2>
          <div className="h-64 flex items-center justify-center text-gray-400">
            <div className="text-center">
              <BarChart3 className="w-12 h-12 mx-auto mb-4" />
              <p>Performance chart will be displayed here</p>
            </div>
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-bold mb-6">Revenue Trends</h2>
          <div className="h-64 flex items-center justify-center text-gray-400">
            <div className="text-center">
              <TrendingUp className="w-12 h-12 mx-auto mb-4" />
              <p>Revenue chart will be displayed here</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}