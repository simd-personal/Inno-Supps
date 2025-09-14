'use client'

import { useState } from 'react'
import { 
  Users, 
  Plus, 
  Search, 
  Filter, 
  MoreVertical, 
  Mail, 
  Phone, 
  MapPin, 
  Building, 
  Calendar,
  Star,
  Edit,
  Trash2,
  Eye,
  Send,
  Download,
  Upload,
  RefreshCw,
  CheckCircle,
  AlertCircle,
  Clock,
  TrendingUp,
  Target,
  BarChart3
} from 'lucide-react'

interface Prospect {
  id: number
  name: string
  email: string
  company: string
  role: string
  industry: string
  location: string
  phone?: string
  status: 'new' | 'contacted' | 'qualified' | 'proposal' | 'closed' | 'lost'
  priority: 'low' | 'medium' | 'high'
  lastContact: string
  nextFollowUp: string
  personalizationScore: number
  tags: string[]
  notes: string
  source: string
  value: number
}

export default function ProspectsPage() {
  const [prospects, setProspects] = useState<Prospect[]>([
    {
      id: 1,
      name: "John Smith",
      email: "john@techcorp.com",
      company: "TechCorp Inc.",
      role: "CTO",
      industry: "Technology",
      location: "San Francisco, CA",
      phone: "+1 (555) 123-4567",
      status: "contacted",
      priority: "high",
      lastContact: "2024-01-15",
      nextFollowUp: "2024-01-22",
      personalizationScore: 85,
      tags: ["AI", "SaaS", "Enterprise"],
      notes: "Interested in AI automation solutions. Raised Series B funding.",
      source: "LinkedIn",
      value: 50000
    },
    {
      id: 2,
      name: "Sarah Johnson",
      email: "sarah@healthplus.com",
      company: "HealthPlus",
      role: "VP of Marketing",
      industry: "Healthcare",
      location: "Austin, TX",
      status: "qualified",
      priority: "medium",
      lastContact: "2024-01-14",
      nextFollowUp: "2024-01-21",
      personalizationScore: 92,
      tags: ["Healthcare", "Marketing", "Growth"],
      notes: "Looking for marketing automation tools. Budget approved.",
      source: "Referral",
      value: 25000
    },
    {
      id: 3,
      name: "Mike Chen",
      email: "mike@retailco.com",
      company: "RetailCo",
      role: "CEO",
      industry: "Retail",
      location: "New York, NY",
      status: "new",
      priority: "low",
      lastContact: "Never",
      nextFollowUp: "2024-01-20",
      personalizationScore: 78,
      tags: ["E-commerce", "Retail", "Startup"],
      notes: "Early stage startup. Interested in growth strategies.",
      source: "Cold Outreach",
      value: 15000
    }
  ])

  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [priorityFilter, setPriorityFilter] = useState('all')
  const [selectedProspects, setSelectedProspects] = useState<number[]>([])

  const filteredProspects = prospects.filter(prospect => {
    const matchesSearch = prospect.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         prospect.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         prospect.email.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = statusFilter === 'all' || prospect.status === statusFilter
    const matchesPriority = priorityFilter === 'all' || prospect.priority === priorityFilter
    
    return matchesSearch && matchesStatus && matchesPriority
  })

  const getStatusColor = (status: string) => {
    const colors = {
      new: 'bg-blue-500',
      contacted: 'bg-yellow-500',
      qualified: 'bg-green-500',
      proposal: 'bg-purple-500',
      closed: 'bg-green-600',
      lost: 'bg-red-500'
    }
    return colors[status as keyof typeof colors] || 'bg-gray-500'
  }

  const getPriorityColor = (priority: string) => {
    const colors = {
      low: 'text-gray-400',
      medium: 'text-yellow-400',
      high: 'text-red-400'
    }
    return colors[priority as keyof typeof colors] || 'text-gray-400'
  }

  const toggleProspectSelection = (id: number) => {
    setSelectedProspects(prev => 
      prev.includes(id) 
        ? prev.filter(prospectId => prospectId !== id)
        : [...prev, id]
    )
  }

  const selectAllProspects = () => {
    setSelectedProspects(filteredProspects.map(p => p.id))
  }

  const deselectAllProspects = () => {
    setSelectedProspects([])
  }

  return (
    <div className="content-body">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-heading-1 text-white mb-2">Prospects</h1>
            <p className="text-neutral-400 text-body-1">Manage your prospect pipeline and track outreach progress</p>
          </div>
          <div className="flex items-center space-x-4">
            <button className="btn-secondary">
              <Upload className="w-4 h-4 mr-2" />
              Import
            </button>
            <button className="btn-secondary">
              <Download className="w-4 h-4 mr-2" />
              Export
            </button>
            <button className="btn-primary">
              <Plus className="w-4 h-4 mr-2" />
              Add Prospect
            </button>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-neutral-400 text-sm">Total Prospects</p>
              <p className="text-2xl font-bold text-white">{prospects.length}</p>
            </div>
            <Users className="w-8 h-8 text-blue-400" />
          </div>
        </div>
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-neutral-400 text-sm">Qualified</p>
              <p className="text-2xl font-bold text-white">{prospects.filter(p => p.status === 'qualified').length}</p>
            </div>
            <CheckCircle className="w-8 h-8 text-green-400" />
          </div>
        </div>
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-neutral-400 text-sm">Pipeline Value</p>
              <p className="text-2xl font-bold text-white">${prospects.reduce((sum, p) => sum + p.value, 0).toLocaleString()}</p>
            </div>
            <TrendingUp className="w-8 h-8 text-green-400" />
          </div>
        </div>
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-neutral-400 text-sm">Avg. Score</p>
              <p className="text-2xl font-bold text-white">{Math.round(prospects.reduce((sum, p) => sum + p.personalizationScore, 0) / prospects.length)}</p>
            </div>
            <Target className="w-8 h-8 text-yellow-400" />
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
                placeholder="Search prospects..."
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
              <option value="new">New</option>
              <option value="contacted">Contacted</option>
              <option value="qualified">Qualified</option>
              <option value="proposal">Proposal</option>
              <option value="closed">Closed</option>
              <option value="lost">Lost</option>
            </select>
            <select
              value={priorityFilter}
              onChange={(e) => setPriorityFilter(e.target.value)}
              className="input"
            >
              <option value="all">All Priority</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>
          <div className="flex items-center space-x-2">
            {selectedProspects.length > 0 && (
              <div className="flex items-center space-x-2">
                <span className="text-sm text-neutral-400">{selectedProspects.length} selected</span>
                <button className="btn-secondary text-sm">
                  <Send className="w-4 h-4 mr-1" />
                  Send Email
                </button>
                <button className="btn-secondary text-sm">
                  <Edit className="w-4 h-4 mr-1" />
                  Edit
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

      {/* Prospects Table */}
      <div className="card">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-neutral-700">
                <th className="text-left py-3 px-4">
                  <input
                    type="checkbox"
                    checked={selectedProspects.length === filteredProspects.length && filteredProspects.length > 0}
                    onChange={selectedProspects.length === filteredProspects.length ? deselectAllProspects : selectAllProspects}
                    className="rounded border-neutral-600 bg-neutral-700"
                  />
                </th>
                <th className="text-left py-3 px-4 text-neutral-400 font-medium">Prospect</th>
                <th className="text-left py-3 px-4 text-neutral-400 font-medium">Company</th>
                <th className="text-left py-3 px-4 text-neutral-400 font-medium">Status</th>
                <th className="text-left py-3 px-4 text-neutral-400 font-medium">Priority</th>
                <th className="text-left py-3 px-4 text-neutral-400 font-medium">Score</th>
                <th className="text-left py-3 px-4 text-neutral-400 font-medium">Value</th>
                <th className="text-left py-3 px-4 text-neutral-400 font-medium">Last Contact</th>
                <th className="text-left py-3 px-4 text-neutral-400 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredProspects.map((prospect) => (
                <tr key={prospect.id} className="border-b border-neutral-800 hover:bg-neutral-800/50">
                  <td className="py-3 px-4">
                    <input
                      type="checkbox"
                      checked={selectedProspects.includes(prospect.id)}
                      onChange={() => toggleProspectSelection(prospect.id)}
                      className="rounded border-neutral-600 bg-neutral-700"
                    />
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                        <span className="text-white text-sm font-medium">
                          {prospect.name.split(' ').map(n => n[0]).join('')}
                        </span>
                      </div>
                      <div>
                        <div className="text-white font-medium">{prospect.name}</div>
                        <div className="text-neutral-400 text-sm">{prospect.email}</div>
                        <div className="text-neutral-500 text-xs">{prospect.role}</div>
                      </div>
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    <div>
                      <div className="text-white font-medium">{prospect.company}</div>
                      <div className="text-neutral-400 text-sm">{prospect.industry}</div>
                      <div className="text-neutral-500 text-xs flex items-center">
                        <MapPin className="w-3 h-3 mr-1" />
                        {prospect.location}
                      </div>
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(prospect.status)} text-white`}>
                      {prospect.status.charAt(0).toUpperCase() + prospect.status.slice(1)}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <div className={`flex items-center ${getPriorityColor(prospect.priority)}`}>
                      <Star className="w-4 h-4 mr-1" />
                      {prospect.priority.charAt(0).toUpperCase() + prospect.priority.slice(1)}
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex items-center">
                      <div className="w-16 bg-neutral-700 rounded-full h-2 mr-2">
                        <div 
                          className="bg-yellow-400 h-2 rounded-full" 
                          style={{ width: `${prospect.personalizationScore}%` }}
                        ></div>
                      </div>
                      <span className="text-white text-sm">{prospect.personalizationScore}</span>
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    <span className="text-white font-medium">${prospect.value.toLocaleString()}</span>
                  </td>
                  <td className="py-3 px-4">
                    <div className="text-neutral-400 text-sm">{prospect.lastContact}</div>
                    <div className="text-neutral-500 text-xs">Next: {prospect.nextFollowUp}</div>
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex items-center space-x-2">
                      <button className="p-1 hover:bg-neutral-700 rounded" title="View">
                        <Eye className="w-4 h-4" />
                      </button>
                      <button className="p-1 hover:bg-neutral-700 rounded" title="Edit">
                        <Edit className="w-4 h-4" />
                      </button>
                      <button className="p-1 hover:bg-neutral-700 rounded" title="Email">
                        <Mail className="w-4 h-4" />
                      </button>
                      <button className="p-1 hover:bg-neutral-700 rounded" title="More">
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

      {/* Empty State */}
      {filteredProspects.length === 0 && (
        <div className="card text-center py-12">
          <Users className="w-12 h-12 mx-auto mb-4 text-neutral-400" />
          <h3 className="text-lg font-medium text-white mb-2">No prospects found</h3>
          <p className="text-neutral-400 mb-4">
            {searchTerm || statusFilter !== 'all' || priorityFilter !== 'all' 
              ? 'Try adjusting your filters or search terms'
              : 'Get started by adding your first prospect'
            }
          </p>
          <button className="btn-primary">
            <Plus className="w-4 h-4 mr-2" />
            Add Prospect
          </button>
        </div>
      )}
    </div>
  )
}
