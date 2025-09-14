'use client'

import { useState } from 'react'
import { 
  Megaphone, 
  Plus, 
  Play, 
  Pause, 
  Stop, 
  Edit, 
  Trash2, 
  Eye, 
  Copy, 
  MoreVertical,
  Users,
  Mail,
  TrendingUp,
  Target,
  Calendar,
  BarChart3,
  Clock,
  CheckCircle,
  AlertCircle,
  ArrowRight,
  Settings,
  Download,
  Share,
  RefreshCw,
  Filter,
  Search
} from 'lucide-react'

interface Campaign {
  id: number
  name: string
  type: 'email' | 'linkedin' | 'cold_call' | 'social' | 'multi_channel'
  status: 'draft' | 'active' | 'paused' | 'completed' | 'archived'
  prospects: number
  sent: number
  opened: number
  replied: number
  converted: number
  openRate: number
  replyRate: number
  conversionRate: number
  startDate: string
  endDate?: string
  createdBy: string
  lastModified: string
  description: string
  tags: string[]
}

export default function CampaignsPage() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([
    {
      id: 1,
      name: "Q1 Enterprise Outreach",
      type: "email",
      status: "active",
      prospects: 150,
      sent: 120,
      opened: 45,
      replied: 12,
      converted: 3,
      openRate: 37.5,
      replyRate: 10.0,
      conversionRate: 2.5,
      startDate: "2024-01-01",
      endDate: "2024-03-31",
      createdBy: "John Doe",
      lastModified: "2024-01-15",
      description: "Targeting enterprise prospects with AI automation solutions",
      tags: ["Enterprise", "AI", "Q1"]
    },
    {
      id: 2,
      name: "Healthcare LinkedIn Campaign",
      type: "linkedin",
      status: "paused",
      prospects: 75,
      sent: 60,
      opened: 25,
      replied: 8,
      converted: 2,
      openRate: 41.7,
      replyRate: 13.3,
      conversionRate: 3.3,
      startDate: "2024-01-10",
      createdBy: "Sarah Johnson",
      lastModified: "2024-01-14",
      description: "LinkedIn outreach to healthcare decision makers",
      tags: ["Healthcare", "LinkedIn", "B2B"]
    },
    {
      id: 3,
      name: "SaaS Cold Call Blitz",
      type: "cold_call",
      status: "completed",
      prospects: 200,
      sent: 200,
      opened: 0,
      replied: 35,
      converted: 8,
      openRate: 0,
      replyRate: 17.5,
      conversionRate: 4.0,
      startDate: "2023-12-01",
      endDate: "2023-12-31",
      createdBy: "Mike Chen",
      lastModified: "2023-12-31",
      description: "High-volume cold calling campaign for SaaS prospects",
      tags: ["SaaS", "Cold Call", "Q4"]
    }
  ])

  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [typeFilter, setTypeFilter] = useState('all')
  const [selectedCampaigns, setSelectedCampaigns] = useState<number[]>([])

  const filteredCampaigns = campaigns.filter(campaign => {
    const matchesSearch = campaign.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         campaign.description.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = statusFilter === 'all' || campaign.status === statusFilter
    const matchesType = typeFilter === 'all' || campaign.type === typeFilter
    
    return matchesSearch && matchesStatus && matchesType
  })

  const getStatusColor = (status: string) => {
    const colors = {
      draft: 'bg-gray-500',
      active: 'bg-green-500',
      paused: 'bg-yellow-500',
      completed: 'bg-blue-500',
      archived: 'bg-neutral-500'
    }
    return colors[status as keyof typeof colors] || 'bg-gray-500'
  }

  const getTypeIcon = (type: string) => {
    const icons = {
      email: Mail,
      linkedin: Users,
      cold_call: Phone,
      social: Megaphone,
      multi_channel: Target
    }
    const Icon = icons[type as keyof typeof icons] || Megaphone
    return <Icon className="w-4 h-4" />
  }

  const toggleCampaignSelection = (id: number) => {
    setSelectedCampaigns(prev => 
      prev.includes(id) 
        ? prev.filter(campaignId => campaignId !== id)
        : [...prev, id]
    )
  }

  const selectAllCampaigns = () => {
    setSelectedCampaigns(filteredCampaigns.map(c => c.id))
  }

  const deselectAllCampaigns = () => {
    setSelectedCampaigns([])
  }

  return (
    <div className="content-body">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-heading-1 text-white mb-2">Campaigns</h1>
            <p className="text-neutral-400 text-body-1">Create and manage your outreach campaigns</p>
          </div>
          <div className="flex items-center space-x-4">
            <button className="btn-secondary">
              <Download className="w-4 h-4 mr-2" />
              Export
            </button>
            <button className="btn-secondary">
              <Copy className="w-4 h-4 mr-2" />
              Duplicate
            </button>
            <button className="btn-primary">
              <Plus className="w-4 h-4 mr-2" />
              Create Campaign
            </button>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-neutral-400 text-sm">Total Campaigns</p>
              <p className="text-2xl font-bold text-white">{campaigns.length}</p>
            </div>
            <Megaphone className="w-8 h-8 text-blue-400" />
          </div>
        </div>
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-neutral-400 text-sm">Active</p>
              <p className="text-2xl font-bold text-white">{campaigns.filter(c => c.status === 'active').length}</p>
            </div>
            <Play className="w-8 h-8 text-green-400" />
          </div>
        </div>
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-neutral-400 text-sm">Avg. Open Rate</p>
              <p className="text-2xl font-bold text-white">{Math.round(campaigns.reduce((sum, c) => sum + c.openRate, 0) / campaigns.length)}%</p>
            </div>
            <TrendingUp className="w-8 h-8 text-green-400" />
          </div>
        </div>
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-neutral-400 text-sm">Total Prospects</p>
              <p className="text-2xl font-bold text-white">{campaigns.reduce((sum, c) => sum + c.prospects, 0)}</p>
            </div>
            <Users className="w-8 h-8 text-yellow-400" />
          </div>
        </div>
      </div>

      {/* Filters and Search */}
      <div className="card mb-6">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
          <div className="flex items-center space-x-4">
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-neutral-400" />
              <input
                type="text"
                placeholder="Search campaigns..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input pl-10 w-64"
              />
            </div>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="input"
            >
              <option value="all">All Status</option>
              <option value="draft">Draft</option>
              <option value="active">Active</option>
              <option value="paused">Paused</option>
              <option value="completed">Completed</option>
              <option value="archived">Archived</option>
            </select>
            <select
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              className="input"
            >
              <option value="all">All Types</option>
              <option value="email">Email</option>
              <option value="linkedin">LinkedIn</option>
              <option value="cold_call">Cold Call</option>
              <option value="social">Social</option>
              <option value="multi_channel">Multi-Channel</option>
            </select>
          </div>
          <div className="flex items-center space-x-2">
            {selectedCampaigns.length > 0 && (
              <div className="flex items-center space-x-2">
                <span className="text-sm text-neutral-400">{selectedCampaigns.length} selected</span>
                <button className="btn-secondary text-sm">
                  <Play className="w-4 h-4 mr-1" />
                  Start
                </button>
                <button className="btn-secondary text-sm">
                  <Pause className="w-4 h-4 mr-1" />
                  Pause
                </button>
              </div>
            )}
            <button className="btn-secondary">
              <Filter className="w-4 h-4 mr-2" />
              Filters
            </button>
          </div>
        </div>
      </div>

      {/* Campaigns Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {filteredCampaigns.map((campaign) => (
          <div key={campaign.id} className="card">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-blue-600 rounded-lg">
                  {getTypeIcon(campaign.type)}
                </div>
                <div>
                  <h3 className="text-white font-medium">{campaign.name}</h3>
                  <p className="text-neutral-400 text-sm">{campaign.type.charAt(0).toUpperCase() + campaign.type.slice(1)} Campaign</p>
                </div>
              </div>
              <div className="flex items-center space-x-1">
                <button className="p-1 hover:bg-neutral-700 rounded">
                  <MoreVertical className="w-4 h-4" />
                </button>
              </div>
            </div>

            <p className="text-neutral-300 text-sm mb-4 line-clamp-2">{campaign.description}</p>

            <div className="flex items-center justify-between mb-4">
              <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(campaign.status)} text-white`}>
                {campaign.status.charAt(0).toUpperCase() + campaign.status.slice(1)}
              </span>
              <div className="flex items-center space-x-2 text-xs text-neutral-400">
                <Calendar className="w-3 h-3" />
                <span>{campaign.startDate}</span>
              </div>
            </div>

            {/* Metrics */}
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="bg-neutral-800 rounded-lg p-3">
                <div className="text-xs text-neutral-400 mb-1">Prospects</div>
                <div className="text-lg font-bold text-white">{campaign.prospects}</div>
                <div className="text-xs text-neutral-500">Sent: {campaign.sent}</div>
              </div>
              <div className="bg-neutral-800 rounded-lg p-3">
                <div className="text-xs text-neutral-400 mb-1">Open Rate</div>
                <div className="text-lg font-bold text-white">{campaign.openRate}%</div>
                <div className="text-xs text-neutral-500">Opened: {campaign.opened}</div>
              </div>
              <div className="bg-neutral-800 rounded-lg p-3">
                <div className="text-xs text-neutral-400 mb-1">Reply Rate</div>
                <div className="text-lg font-bold text-white">{campaign.replyRate}%</div>
                <div className="text-xs text-neutral-500">Replied: {campaign.replied}</div>
              </div>
              <div className="bg-neutral-800 rounded-lg p-3">
                <div className="text-xs text-neutral-400 mb-1">Conversion</div>
                <div className="text-lg font-bold text-white">{campaign.conversionRate}%</div>
                <div className="text-xs text-neutral-500">Converted: {campaign.converted}</div>
              </div>
            </div>

            {/* Tags */}
            <div className="flex flex-wrap gap-1 mb-4">
              {campaign.tags.map((tag, index) => (
                <span key={index} className="px-2 py-1 bg-neutral-700 text-neutral-300 text-xs rounded">
                  {tag}
                </span>
              ))}
            </div>

            {/* Actions */}
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <button className="p-1 hover:bg-neutral-700 rounded" title="View">
                  <Eye className="w-4 h-4" />
                </button>
                <button className="p-1 hover:bg-neutral-700 rounded" title="Edit">
                  <Edit className="w-4 h-4" />
                </button>
                <button className="p-1 hover:bg-neutral-700 rounded" title="Settings">
                  <Settings className="w-4 h-4" />
                </button>
              </div>
              <div className="flex items-center space-x-2">
                {campaign.status === 'active' ? (
                  <button className="btn-secondary text-sm">
                    <Pause className="w-4 h-4 mr-1" />
                    Pause
                  </button>
                ) : campaign.status === 'paused' ? (
                  <button className="btn-primary text-sm">
                    <Play className="w-4 h-4 mr-1" />
                    Resume
                  </button>
                ) : campaign.status === 'draft' ? (
                  <button className="btn-primary text-sm">
                    <Play className="w-4 h-4 mr-1" />
                    Start
                  </button>
                ) : (
                  <button className="btn-secondary text-sm">
                    <RefreshCw className="w-4 h-4 mr-1" />
                    Restart
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {filteredCampaigns.length === 0 && (
        <div className="card text-center py-12">
          <Megaphone className="w-12 h-12 mx-auto mb-4 text-neutral-400" />
          <h3 className="text-lg font-medium text-white mb-2">No campaigns found</h3>
          <p className="text-neutral-400 mb-4">
            {searchTerm || statusFilter !== 'all' || typeFilter !== 'all' 
              ? 'Try adjusting your filters or search terms'
              : 'Get started by creating your first campaign'
            }
          </p>
          <button className="btn-primary">
            <Plus className="w-4 h-4 mr-2" />
            Create Campaign
          </button>
        </div>
      )}
    </div>
  )
}
