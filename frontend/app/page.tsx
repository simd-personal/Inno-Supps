'use client'

import { useState, useEffect } from 'react'
import Dashboard from './components/Dashboard'
import NicheResearcher from './components/NicheResearcher'
import ColdEmailWriter from './components/ColdEmailWriter'
import RevenueRushEcosystem from './components/RevenueRushEcosystem'
import UnifiedAnalytics from './components/UnifiedAnalytics'
import CrossPlatformNotifications from './components/CrossPlatformNotifications'
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

  console.log('Home component rendered with activeTab:', activeTab)

  const sidebarItems = [
    { id: 'overview', label: 'Overview', icon: BarChart3, active: false },
    { id: 'unified-analytics', label: 'Unified Analytics', icon: TrendingUp, active: false },
    { id: 'revenue-rush-ecosystem', label: 'Revenue Rush Ecosystem', icon: Server, active: false },
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
    console.log('Rendering content for activeTab:', activeTab)
    switch (activeTab) {
      case 'overview':
        console.log('Rendering Dashboard component')
        return <Dashboard />
      case 'unified-analytics':
        return <UnifiedAnalytics />
      case 'revenue-rush-ecosystem':
        return <RevenueRushEcosystem />
      case 'niche-researcher':
        return <NicheResearcher />
      case 'cold-email-writer':
        return <ColdEmailWriter />
      default:
        console.log('Rendering default content')
        return (
          <div className="content-body">
            <div className="text-center py-12">
              <h1 className="text-display text-white mb-4">Welcome to Inno</h1>
              <p className="text-neutral-400 mb-8 text-body-1">Your AI-powered B2B growth platform</p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
                <div className="card">
                  <Search className="w-12 h-12 text-red-500 mx-auto mb-4" />
                  <h3 className="text-heading-4 text-white mb-2">Niche Researcher</h3>
                  <p className="text-neutral-400 text-body-2">Find profitable niches with AI-powered market analysis</p>
                </div>
                <div className="card">
                  <Mail className="w-12 h-12 text-red-500 mx-auto mb-4" />
                  <h3 className="text-heading-4 text-white mb-2">Cold Email Writer</h3>
                  <p className="text-neutral-400 text-body-2">Generate personalized cold emails that convert</p>
                </div>
                <div className="card">
                  <BarChart3 className="w-12 h-12 text-red-500 mx-auto mb-4" />
                  <h3 className="text-heading-4 text-white mb-2">Analytics</h3>
                  <p className="text-neutral-400 text-body-2">Track performance and optimize your campaigns</p>
                </div>
              </div>
            </div>
          </div>
        )
    }
  }

  return (
    <div className="min-h-screen" style={{ backgroundColor: 'var(--neutral-900)', color: 'var(--neutral-50)' }}>
      {/* Top Navigation Bar */}
      <div className="content-header">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">I</span>
            </div>
            <span className="text-heading-4 text-white">Inno</span>
          </div>
          <div className="flex items-center space-x-2 text-neutral-400">
            <ChevronDown className="w-4 h-4" />
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 text-neutral-400">
            <span className="text-sm">revenue-rush.com</span>
          </div>
          <div className="flex items-center space-x-2">
            <CrossPlatformNotifications />
            <button className="p-2 hover:bg-neutral-700 rounded-lg transition-colors">
              <Plus className="w-5 h-5" />
            </button>
            <button className="p-2 hover:bg-neutral-700 rounded-lg transition-colors">
              <User className="w-5 h-5" />
            </button>
            <button className="p-2 hover:bg-neutral-700 rounded-lg transition-colors">
              <MoreVertical className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      <div className="flex">
        {/* Sidebar */}
        <div className={`sidebar transition-all duration-300 ${sidebarCollapsed ? 'w-16' : 'w-64'}`} style={{ width: sidebarCollapsed ? '64px' : '280px' }}>
          <div className="sidebar-header">
            <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">I</span>
              </div>
              {!sidebarCollapsed && <span className="text-heading-4 text-white">Inno</span>}
            </div>
              <button 
                onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
                className="p-1 hover:bg-neutral-700 rounded transition-colors"
              >
                <ChevronDown className="w-4 h-4" />
              </button>
            </div>
          </div>

            <nav className="sidebar-nav">
              {sidebarItems.map((item) => (
                <div key={item.id}>
                  <button
                    onClick={() => setActiveTab(item.id)}
                    className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
                  >
                    <item.icon className="nav-item-icon" />
                    {!sidebarCollapsed && <span>{item.label}</span>}
                    {item.children && <ChevronDown className="w-4 h-4 ml-auto" />}
                  </button>
                  
                  {item.children && item.expanded && !sidebarCollapsed && (
                    <div className="ml-6 mt-1 space-y-1">
                      {item.children.map((child) => (
                        <button
                          key={child.id}
                          onClick={() => setActiveTab(child.id)}
                          className={`nav-item ${activeTab === child.id ? 'active' : ''}`}
                        >
                          <child.icon className="nav-item-icon" />
                          <span>{child.label}</span>
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </nav>

          {/* User Profile - Now at bottom of sidebar */}
          <div className="absolute bottom-0 left-0 right-0 p-4 border-t" style={{ borderColor: 'var(--neutral-800)' }}>
            <div className="flex items-center space-x-3 p-3 rounded-lg" style={{ backgroundColor: 'var(--neutral-800)' }}>
              <div className="w-8 h-8 bg-red-600 rounded-full flex items-center justify-center">
                <span className="text-white font-bold text-sm">S</span>
              </div>
              {!sidebarCollapsed && (
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium truncate text-white">Simba</p>
                  <p className="text-xs text-neutral-400 truncate">simba@inno-supps.com</p>
                  <div className="flex items-center space-x-2 mt-1">
                    <span className="badge badge-primary">Pro</span>
                    <span className="badge badge-success">RR Access</span>
                  </div>
                </div>
              )}
              {!sidebarCollapsed && <MoreVertical className="w-4 h-4" />}
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className={`main-content ${sidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
          {renderContent()}
        </div>
      </div>
    </div>
  )
}