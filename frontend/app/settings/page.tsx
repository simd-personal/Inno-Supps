'use client'

import { useState } from 'react'
import { 
  Settings as SettingsIcon, 
  User, 
  Bell, 
  Shield, 
  CreditCard, 
  Database, 
  Key, 
  Globe, 
  Mail, 
  Phone, 
  Building, 
  Save, 
  Edit, 
  Trash2, 
  Plus, 
  CheckCircle, 
  AlertCircle, 
  Eye, 
  EyeOff,
  Download,
  Upload,
  RefreshCw,
  LogOut,
  HelpCircle,
  Info
} from 'lucide-react'

interface UserProfile {
  name: string
  email: string
  role: string
  company: string
  phone: string
  timezone: string
  avatar?: string
}

interface Integration {
  id: number
  name: string
  type: 'email' | 'crm' | 'calendar' | 'social' | 'analytics'
  status: 'connected' | 'disconnected' | 'error'
  lastSync: string
  description: string
}

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState('profile')
  const [profile, setProfile] = useState<UserProfile>({
    name: 'John Doe',
    email: 'john@yourcompany.com',
    role: 'Admin',
    company: 'Your Company',
    phone: '+1 (555) 123-4567',
    timezone: 'America/New_York'
  })

  const [integrations, setIntegrations] = useState<Integration[]>([
    {
      id: 1,
      name: 'Gmail',
      type: 'email',
      status: 'connected',
      lastSync: '2024-01-15T10:30:00Z',
      description: 'Email integration for sending and receiving messages'
    },
    {
      id: 2,
      name: 'Salesforce',
      type: 'crm',
      status: 'connected',
      lastSync: '2024-01-15T09:15:00Z',
      description: 'CRM integration for prospect and lead management'
    },
    {
      id: 3,
      name: 'Google Calendar',
      type: 'calendar',
      status: 'connected',
      lastSync: '2024-01-15T08:45:00Z',
      description: 'Calendar integration for scheduling and meetings'
    },
    {
      id: 4,
      name: 'LinkedIn',
      type: 'social',
      status: 'disconnected',
      lastSync: '2024-01-10T14:20:00Z',
      description: 'LinkedIn integration for social selling'
    },
    {
      id: 5,
      name: 'HubSpot',
      type: 'crm',
      status: 'error',
      lastSync: '2024-01-12T16:30:00Z',
      description: 'HubSpot CRM integration'
    }
  ])

  const [notifications, setNotifications] = useState({
    email: true,
    push: true,
    sms: false,
    weeklyDigest: true,
    campaignUpdates: true,
    prospectActivity: true,
    systemAlerts: true
  })

  const [apiKeys, setApiKeys] = useState([
    { name: 'OpenAI API', key: 'sk-...', lastUsed: '2024-01-15', status: 'active' },
    { name: 'SendGrid API', key: 'SG...', lastUsed: '2024-01-14', status: 'active' },
    { name: 'LinkedIn API', key: 'LI...', lastUsed: '2024-01-10', status: 'expired' }
  ])

  const tabs = [
    { id: 'profile', name: 'Profile', icon: User },
    { id: 'integrations', name: 'Integrations', icon: Database },
    { id: 'notifications', name: 'Notifications', icon: Bell },
    { id: 'security', name: 'Security', icon: Shield },
    { id: 'billing', name: 'Billing', icon: CreditCard },
    { id: 'api', name: 'API Keys', icon: Key }
  ]

  const getIntegrationIcon = (type: string) => {
    const icons = {
      email: Mail,
      crm: Building,
      calendar: Calendar,
      social: Globe,
      analytics: BarChart3
    }
    const Icon = icons[type as keyof typeof icons] || SettingsIcon
    return <Icon className="w-5 h-5" />
  }

  const getStatusColor = (status: string) => {
    const colors = {
      connected: 'text-green-400',
      disconnected: 'text-gray-400',
      error: 'text-red-400'
    }
    return colors[status as keyof typeof colors] || 'text-gray-400'
  }

  const getStatusIcon = (status: string) => {
    const icons = {
      connected: CheckCircle,
      disconnected: AlertCircle,
      error: AlertCircle
    }
    const Icon = icons[status as keyof typeof icons] || AlertCircle
    return <Icon className="w-4 h-4" />
  }

  return (
    <div className="content-body">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-heading-1 text-white mb-2">Settings</h1>
        <p className="text-neutral-400 text-body-1">Manage your account settings and preferences</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Sidebar */}
        <div className="lg:col-span-1">
          <div className="card">
            <nav className="space-y-1">
              {tabs.map((tab) => {
                const Icon = tab.icon
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                      activeTab === tab.id
                        ? 'bg-blue-600 text-white'
                        : 'text-neutral-400 hover:text-white hover:bg-neutral-700'
                    }`}
                  >
                    <Icon className="w-4 h-4 mr-3" />
                    {tab.name}
                  </button>
                )
              })}
            </nav>
          </div>
        </div>

        {/* Content */}
        <div className="lg:col-span-3">
          {/* Profile Tab */}
          {activeTab === 'profile' && (
            <div className="space-y-6">
              <div className="card">
                <div className="card-header">
                  <h2 className="card-title">Profile Information</h2>
                  <p className="card-subtitle">Update your personal information and contact details</p>
                </div>
                <div className="space-y-6">
                  <div className="flex items-center space-x-6">
                    <div className="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center">
                      <span className="text-white text-2xl font-bold">
                        {profile.name.split(' ').map(n => n[0]).join('')}
                      </span>
                    </div>
                    <div>
                      <button className="btn-secondary mb-2">
                        <Upload className="w-4 h-4 mr-2" />
                        Upload Photo
                      </button>
                      <p className="text-sm text-neutral-400">JPG, PNG or GIF. Max size 2MB.</p>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium mb-2">Full Name</label>
                      <input
                        type="text"
                        value={profile.name}
                        onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                        className="input"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-2">Email</label>
                      <input
                        type="email"
                        value={profile.email}
                        onChange={(e) => setProfile({ ...profile, email: e.target.value })}
                        className="input"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-2">Role</label>
                      <input
                        type="text"
                        value={profile.role}
                        onChange={(e) => setProfile({ ...profile, role: e.target.value })}
                        className="input"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-2">Company</label>
                      <input
                        type="text"
                        value={profile.company}
                        onChange={(e) => setProfile({ ...profile, company: e.target.value })}
                        className="input"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-2">Phone</label>
                      <input
                        type="tel"
                        value={profile.phone}
                        onChange={(e) => setProfile({ ...profile, phone: e.target.value })}
                        className="input"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-2">Timezone</label>
                      <select
                        value={profile.timezone}
                        onChange={(e) => setProfile({ ...profile, timezone: e.target.value })}
                        className="input"
                      >
                        <option value="America/New_York">Eastern Time</option>
                        <option value="America/Chicago">Central Time</option>
                        <option value="America/Denver">Mountain Time</option>
                        <option value="America/Los_Angeles">Pacific Time</option>
                        <option value="Europe/London">London</option>
                        <option value="Europe/Paris">Paris</option>
                        <option value="Asia/Tokyo">Tokyo</option>
                      </select>
                    </div>
                  </div>

                  <div className="flex items-center justify-end">
                    <button className="btn-primary">
                      <Save className="w-4 h-4 mr-2" />
                      Save Changes
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Integrations Tab */}
          {activeTab === 'integrations' && (
            <div className="space-y-6">
              <div className="card">
                <div className="card-header">
                  <h2 className="card-title">Connected Integrations</h2>
                  <p className="card-subtitle">Manage your third-party integrations and data sources</p>
                </div>
                <div className="space-y-4">
                  {integrations.map((integration) => (
                    <div key={integration.id} className="flex items-center justify-between p-4 bg-neutral-800 rounded-lg">
                      <div className="flex items-center space-x-4">
                        <div className="p-2 bg-blue-600 rounded-lg">
                          {getIntegrationIcon(integration.type)}
                        </div>
                        <div>
                          <h3 className="text-white font-medium">{integration.name}</h3>
                          <p className="text-sm text-neutral-400">{integration.description}</p>
                          <p className="text-xs text-neutral-500">
                            Last sync: {new Date(integration.lastSync).toLocaleString()}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-4">
                        <div className={`flex items-center space-x-2 ${getStatusColor(integration.status)}`}>
                          {getStatusIcon(integration.status)}
                          <span className="text-sm capitalize">{integration.status}</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          {integration.status === 'connected' ? (
                            <button className="btn-secondary text-sm">
                              <RefreshCw className="w-4 h-4 mr-1" />
                              Sync
                            </button>
                          ) : (
                            <button className="btn-primary text-sm">
                              <Plus className="w-4 h-4 mr-1" />
                              Connect
                            </button>
                          )}
                          <button className="p-2 hover:bg-neutral-700 rounded">
                            <MoreVertical className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="card">
                <div className="card-header">
                  <h2 className="card-title">Available Integrations</h2>
                  <p className="card-subtitle">Connect additional services to enhance your workflow</p>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {[
                    { name: 'Slack', type: 'communication', description: 'Team communication and notifications' },
                    { name: 'Zoom', type: 'meeting', description: 'Video conferencing and meeting scheduling' },
                    { name: 'Zapier', type: 'automation', description: 'Automate workflows between apps' },
                    { name: 'Intercom', type: 'support', description: 'Customer support and live chat' }
                  ].map((integration, index) => (
                    <div key={index} className="p-4 bg-neutral-800 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="text-white font-medium">{integration.name}</h3>
                        <button className="btn-primary text-sm">
                          <Plus className="w-4 h-4 mr-1" />
                          Connect
                        </button>
                      </div>
                      <p className="text-sm text-neutral-400">{integration.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Notifications Tab */}
          {activeTab === 'notifications' && (
            <div className="space-y-6">
              <div className="card">
                <div className="card-header">
                  <h2 className="card-title">Notification Preferences</h2>
                  <p className="card-subtitle">Choose how you want to be notified about important events</p>
                </div>
                <div className="space-y-6">
                  <div>
                    <h3 className="text-lg font-medium text-white mb-4">Communication Channels</h3>
                    <div className="space-y-4">
                      {[
                        { key: 'email', label: 'Email Notifications', description: 'Receive notifications via email' },
                        { key: 'push', label: 'Push Notifications', description: 'Receive push notifications in your browser' },
                        { key: 'sms', label: 'SMS Notifications', description: 'Receive text message notifications' }
                      ].map((item) => (
                        <div key={item.key} className="flex items-center justify-between p-4 bg-neutral-800 rounded-lg">
                          <div>
                            <h4 className="text-white font-medium">{item.label}</h4>
                            <p className="text-sm text-neutral-400">{item.description}</p>
                          </div>
                          <label className="relative inline-flex items-center cursor-pointer">
                            <input
                              type="checkbox"
                              checked={notifications[item.key as keyof typeof notifications]}
                              onChange={(e) => setNotifications({
                                ...notifications,
                                [item.key]: e.target.checked
                              })}
                              className="sr-only peer"
                            />
                            <div className="w-11 h-6 bg-neutral-600 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-neutral-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                          </label>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div>
                    <h3 className="text-lg font-medium text-white mb-4">Notification Types</h3>
                    <div className="space-y-4">
                      {[
                        { key: 'weeklyDigest', label: 'Weekly Digest', description: 'Weekly summary of your activities' },
                        { key: 'campaignUpdates', label: 'Campaign Updates', description: 'Updates about your campaigns' },
                        { key: 'prospectActivity', label: 'Prospect Activity', description: 'New prospect interactions and responses' },
                        { key: 'systemAlerts', label: 'System Alerts', description: 'Important system notifications' }
                      ].map((item) => (
                        <div key={item.key} className="flex items-center justify-between p-4 bg-neutral-800 rounded-lg">
                          <div>
                            <h4 className="text-white font-medium">{item.label}</h4>
                            <p className="text-sm text-neutral-400">{item.description}</p>
                          </div>
                          <label className="relative inline-flex items-center cursor-pointer">
                            <input
                              type="checkbox"
                              checked={notifications[item.key as keyof typeof notifications]}
                              onChange={(e) => setNotifications({
                                ...notifications,
                                [item.key]: e.target.checked
                              })}
                              className="sr-only peer"
                            />
                            <div className="w-11 h-6 bg-neutral-600 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-neutral-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                          </label>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Security Tab */}
          {activeTab === 'security' && (
            <div className="space-y-6">
              <div className="card">
                <div className="card-header">
                  <h2 className="card-title">Password & Security</h2>
                  <p className="card-subtitle">Manage your password and security settings</p>
                </div>
                <div className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium mb-2">Current Password</label>
                    <input type="password" className="input" placeholder="Enter current password" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">New Password</label>
                    <input type="password" className="input" placeholder="Enter new password" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">Confirm New Password</label>
                    <input type="password" className="input" placeholder="Confirm new password" />
                  </div>
                  <button className="btn-primary">
                    <Save className="w-4 h-4 mr-2" />
                    Update Password
                  </button>
                </div>
              </div>

              <div className="card">
                <div className="card-header">
                  <h2 className="card-title">Two-Factor Authentication</h2>
                  <p className="card-subtitle">Add an extra layer of security to your account</p>
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-white font-medium">Authenticator App</h3>
                    <p className="text-sm text-neutral-400">Use an authenticator app to generate verification codes</p>
                  </div>
                  <button className="btn-secondary">
                    <Plus className="w-4 h-4 mr-2" />
                    Enable 2FA
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* API Keys Tab */}
          {activeTab === 'api' && (
            <div className="space-y-6">
              <div className="card">
                <div className="card-header">
                  <h2 className="card-title">API Keys</h2>
                  <p className="card-subtitle">Manage your API keys for third-party integrations</p>
                </div>
                <div className="space-y-4">
                  {apiKeys.map((apiKey, index) => (
                    <div key={index} className="flex items-center justify-between p-4 bg-neutral-800 rounded-lg">
                      <div>
                        <h3 className="text-white font-medium">{apiKey.name}</h3>
                        <p className="text-sm text-neutral-400 font-mono">{apiKey.key}</p>
                        <p className="text-xs text-neutral-500">Last used: {apiKey.lastUsed}</p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className={`px-2 py-1 rounded text-xs ${
                          apiKey.status === 'active' ? 'bg-green-900 text-green-400' : 'bg-red-900 text-red-400'
                        }`}>
                          {apiKey.status}
                        </span>
                        <button className="p-2 hover:bg-neutral-700 rounded">
                          <Eye className="w-4 h-4" />
                        </button>
                        <button className="p-2 hover:bg-neutral-700 rounded">
                          <Edit className="w-4 h-4" />
                        </button>
                        <button className="p-2 hover:bg-neutral-700 rounded text-red-400">
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="mt-6">
                  <button className="btn-primary">
                    <Plus className="w-4 h-4 mr-2" />
                    Add API Key
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Billing Tab */}
          {activeTab === 'billing' && (
            <div className="space-y-6">
              <div className="card">
                <div className="card-header">
                  <h2 className="card-title">Billing & Subscription</h2>
                  <p className="card-subtitle">Manage your subscription and billing information</p>
                </div>
                <div className="space-y-6">
                  <div className="flex items-center justify-between p-4 bg-neutral-800 rounded-lg">
                    <div>
                      <h3 className="text-white font-medium">Pro Plan</h3>
                      <p className="text-sm text-neutral-400">$99/month • Billed monthly</p>
                    </div>
                    <button className="btn-secondary">Change Plan</button>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h3 className="text-lg font-medium text-white mb-4">Payment Method</h3>
                      <div className="p-4 bg-neutral-800 rounded-lg">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-3">
                            <div className="w-8 h-8 bg-blue-600 rounded flex items-center justify-center">
                              <CreditCard className="w-4 h-4" />
                            </div>
                            <div>
                              <p className="text-white font-medium">•••• •••• •••• 4242</p>
                              <p className="text-sm text-neutral-400">Expires 12/25</p>
                            </div>
                          </div>
                          <button className="btn-secondary text-sm">Update</button>
                        </div>
                      </div>
                    </div>
                    
                    <div>
                      <h3 className="text-lg font-medium text-white mb-4">Billing Address</h3>
                      <div className="p-4 bg-neutral-800 rounded-lg">
                        <p className="text-white">123 Business St</p>
                        <p className="text-white">San Francisco, CA 94105</p>
                        <p className="text-white">United States</p>
                        <button className="btn-secondary text-sm mt-2">Update</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
