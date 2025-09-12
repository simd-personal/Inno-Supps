'use client'

import { useState, useEffect } from 'react'
import Dashboard from './components/Dashboard'
import NicheResearcher from './components/NicheResearcher'
import ColdEmailWriter from './components/ColdEmailWriter'
import { 
  BarChart3, 
  Server, 
  Menu, 
  Search, 
  Gift, 
  Mail, 
  User, 
  Zap, 
  LineChart, 
  Calculator, 
  Phone,
  Wrench,
  BookOpen,
  Workflow,
  Settings,
  Bell,
  Plus,
  MoreVertical,
  ChevronDown,
  CheckCircle,
  Star,
  TrendingUp,
  Users,
  DollarSign,
  Target,
  Clock,
  MessageSquare,
  Calendar,
  Filter,
  Download,
  Upload,
  Eye,
  Edit,
  Trash2,
  Copy,
  Share,
  ExternalLink
} from 'lucide-react'

export default function Home() {
  const [activeTab, setActiveTab] = useState('overview')
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [selectedNiche, setSelectedNiche] = useState(null)

  const sidebarItems = [
    { id: 'overview', label: 'Overview', icon: BarChart3, active: true },
    { id: 'operating-system', label: 'Operating System', icon: Server, active: false },
    { id: 'submissions', label: 'Submissions', icon: Menu, active: false },
    { id: 'growth-consultant', label: 'AI Growth Consultant', icon: CheckCircle, active: false },
    { 
      id: 'acquisition', 
      label: 'Acquisition', 
      icon: ChevronDown, 
      active: false,
      expanded: true,
      children: [
        { id: 'niche-researcher', label: 'Niche Researcher', icon: Search },
        { id: 'top-50-niches', label: 'Top 50 Niches', icon: Menu },
        { id: 'offer-creator', label: 'Offer Creator', icon: Gift },
        { id: 'cold-email-writer', label: 'Cold Email Writer', icon: Mail },
        { id: 'cold-email-agent', label: 'Cold Email Agent', icon: User },
        { id: 'ad-writer', label: 'Ad Writer', icon: Zap },
        { id: 'growth-plan-creator', label: 'Growth Plan Creator', icon: LineChart },
        { id: 'pricing-calculator', label: 'Pricing Calculator', icon: Calculator },
        { id: 'sales-call-analyzer', label: 'Sales Call Analyzer', icon: Phone }
      ]
    },
    { 
      id: 'client-delivery', 
      label: 'Client Delivery', 
      icon: ChevronDown, 
      active: false,
      expanded: true,
      children: [
        { id: 'ai-tools', label: 'AI Tools', icon: Wrench },
        { id: 'hiring-portal', label: 'Hiring Portal', icon: User }
      ]
    },
    { 
      id: 'automations', 
      label: 'Automations', 
      icon: ChevronDown, 
      active: false,
      expanded: true,
      children: [
        { id: 'n8n-workflow-creator', label: 'n8n Workflow Creator', icon: Workflow },
        { id: 'n8n-workflow-library', label: 'n8n Workflow Library', icon: BookOpen }
      ]
    },
    { id: 'feedback', label: 'Submit Feedback', icon: MessageSquare, active: false },
    { id: 'settings', label: 'Workspace Settings', icon: Settings, active: false }
  ]

  const renderContent = () => {
    switch (activeTab) {
      case 'overview':
        return <Dashboard />
      case 'niche-researcher':
        return <NicheResearcher />
      case 'cold-email-writer':
        return <ColdEmailWriter />
      default:
        return (
          <div className="min-h-screen bg-gray-900 text-white p-6">
            <div className="text-center py-12">
              <h1 className="text-3xl font-bold mb-4">Welcome to AI Acquisition</h1>
              <p className="text-gray-400 mb-8">Your AI-powered B2B growth system</p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
                <div className="bg-gray-800 rounded-lg p-6">
                  <Search className="w-12 h-12 text-blue-500 mx-auto mb-4" />
                  <h3 className="text-xl font-bold mb-2">Niche Researcher</h3>
                  <p className="text-gray-400">Find profitable niches with AI-powered market analysis</p>
                </div>
                <div className="bg-gray-800 rounded-lg p-6">
                  <Mail className="w-12 h-12 text-green-500 mx-auto mb-4" />
                  <h3 className="text-xl font-bold mb-2">Cold Email Writer</h3>
                  <p className="text-gray-400">Generate personalized cold emails that convert</p>
                </div>
                <div className="bg-gray-800 rounded-lg p-6">
                  <BarChart3 className="w-12 h-12 text-purple-500 mx-auto mb-4" />
                  <h3 className="text-xl font-bold mb-2">Analytics</h3>
                  <p className="text-gray-400">Track performance and optimize your campaigns</p>
                </div>
              </div>
            </div>
          </div>
        )
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Top Navigation Bar */}
      <div className="bg-gray-800 border-b border-gray-700 px-4 py-3 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">A</span>
            </div>
            <span className="font-semibold text-lg">AI Acquisition</span>
          </div>
          <div className="flex items-center space-x-2 text-gray-400">
            <ChevronDown className="w-4 h-4" />
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 text-gray-400">
            <span className="text-sm">ai-clients.com</span>
          </div>
          <div className="flex items-center space-x-2">
            <button className="p-2 hover:bg-gray-700 rounded-lg">
              <Bell className="w-5 h-5" />
            </button>
            <button className="p-2 hover:bg-gray-700 rounded-lg">
              <Plus className="w-5 h-5" />
            </button>
            <button className="p-2 hover:bg-gray-700 rounded-lg">
              <User className="w-5 h-5" />
            </button>
            <button className="p-2 hover:bg-gray-700 rounded-lg">
              <MoreVertical className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      <div className="flex">
        {/* Sidebar */}
        <div className={`bg-gray-800 border-r border-gray-700 transition-all duration-300 ${sidebarCollapsed ? 'w-16' : 'w-64'} flex flex-col h-screen`}>
          <div className="p-4 flex-1">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">A</span>
                </div>
                {!sidebarCollapsed && <span className="font-semibold">AI Acquisition</span>}
              </div>
              <button 
                onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
                className="p-1 hover:bg-gray-700 rounded"
              >
                <ChevronDown className="w-4 h-4" />
              </button>
            </div>

            <nav className="space-y-1">
              {sidebarItems.map((item) => (
                <div key={item.id}>
                  <button
                    onClick={() => setActiveTab(item.id)}
                    className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-left transition-colors ${
                      item.active ? 'bg-gray-700 border-l-2 border-blue-500' : 'hover:bg-gray-700'
                    }`}
                  >
                    <item.icon className="w-5 h-5" />
                    {!sidebarCollapsed && <span>{item.label}</span>}
                    {item.children && <ChevronDown className="w-4 h-4 ml-auto" />}
                  </button>
                  
                  {item.children && item.expanded && !sidebarCollapsed && (
                    <div className="ml-6 mt-1 space-y-1">
                      {item.children.map((child) => (
                        <button
                          key={child.id}
                          onClick={() => setActiveTab(child.id)}
                          className="w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-left text-gray-300 hover:bg-gray-700 hover:text-white transition-colors"
                        >
                          <child.icon className="w-4 h-4" />
                          <span>{child.label}</span>
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </nav>
          </div>

          {/* User Profile - Now at bottom of sidebar */}
          <div className="p-4 border-t border-gray-700">
            <div className="flex items-center space-x-3 p-3 bg-gray-700 rounded-lg">
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                <span className="text-white font-bold text-sm">S</span>
              </div>
              {!sidebarCollapsed && (
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium truncate">Simba</p>
                  <p className="text-xs text-gray-400 truncate">simba@inno-supps.com</p>
                </div>
              )}
              {!sidebarCollapsed && <MoreVertical className="w-4 h-4" />}
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1">
          {renderContent()}
        </div>
      </div>
    </div>
  )
}