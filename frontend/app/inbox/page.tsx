'use client'

import { useState } from 'react'
import { 
  Mail, 
  Search, 
  Filter, 
  RefreshCw, 
  Reply, 
  ReplyAll, 
  Forward, 
  Archive, 
  Trash2, 
  Star, 
  StarOff,
  MoreVertical,
  Eye,
  Edit,
  Send,
  Clock,
  CheckCircle,
  AlertCircle,
  User,
  Building,
  Calendar,
  Phone,
  MessageSquare,
  Tag,
  Flag,
  Download,
  Upload
} from 'lucide-react'

interface Email {
  id: number
  from: string
  fromName: string
  fromCompany: string
  to: string
  subject: string
  preview: string
  body: string
  timestamp: string
  isRead: boolean
  isStarred: boolean
  isImportant: boolean
  isReplied: boolean
  tags: string[]
  threadId: string
  type: 'inbound' | 'outbound' | 'draft'
  status: 'new' | 'read' | 'replied' | 'archived'
  prospectId?: number
  campaignId?: number
}

export default function InboxPage() {
  const [emails, setEmails] = useState<Email[]>([
    {
      id: 1,
      from: "john@techcorp.com",
      fromName: "John Smith",
      fromCompany: "TechCorp Inc.",
      to: "you@yourcompany.com",
      subject: "Re: AI Automation Solutions - Quick Question",
      preview: "Thanks for reaching out! I'm definitely interested in learning more about your AI automation solutions. When would be a good time to schedule a call?",
      body: "Hi there,\n\nThanks for reaching out! I'm definitely interested in learning more about your AI automation solutions. We've been looking for ways to streamline our operations and your approach sounds promising.\n\nWhen would be a good time to schedule a call? I'm available most afternoons this week.\n\nBest regards,\nJohn Smith\nCTO, TechCorp Inc.",
      timestamp: "2024-01-15T14:30:00Z",
      isRead: false,
      isStarred: true,
      isImportant: true,
      isReplied: false,
      tags: ["AI", "Enterprise", "Hot Lead"],
      threadId: "thread_001",
      type: "inbound",
      status: "new",
      prospectId: 1,
      campaignId: 1
    },
    {
      id: 2,
      from: "sarah@healthplus.com",
      fromName: "Sarah Johnson",
      fromCompany: "HealthPlus",
      to: "you@yourcompany.com",
      subject: "Marketing Automation - Budget Approved",
      preview: "Great news! We've approved the budget for marketing automation. Can you send over the proposal and next steps?",
      body: "Hi,\n\nGreat news! We've approved the budget for marketing automation tools. The team is excited to move forward.\n\nCan you send over the detailed proposal and next steps? We'd like to get started as soon as possible.\n\nThanks,\nSarah Johnson\nVP of Marketing, HealthPlus",
      timestamp: "2024-01-15T11:15:00Z",
      isRead: true,
      isStarred: false,
      isImportant: true,
      isReplied: false,
      tags: ["Marketing", "Approved", "Ready to Close"],
      threadId: "thread_002",
      type: "inbound",
      status: "read",
      prospectId: 2,
      campaignId: 1
    },
    {
      id: 3,
      from: "you@yourcompany.com",
      fromName: "You",
      fromCompany: "Your Company",
      to: "mike@retailco.com",
      subject: "Follow-up: Growth Strategies for RetailCo",
      preview: "Hi Mike, I wanted to follow up on our conversation about growth strategies. I've prepared some specific recommendations for RetailCo...",
      body: "Hi Mike,\n\nI wanted to follow up on our conversation about growth strategies for RetailCo. I've prepared some specific recommendations based on your current challenges.\n\nWould you be available for a 30-minute call this week to discuss?\n\nBest regards,\n[Your Name]",
      timestamp: "2024-01-14T16:45:00Z",
      isRead: true,
      isStarred: false,
      isImportant: false,
      isReplied: false,
      tags: ["Follow-up", "Retail", "Cold Outreach"],
      threadId: "thread_003",
      type: "outbound",
      status: "read",
      prospectId: 3,
      campaignId: 2
    },
    {
      id: 4,
      from: "support@linkedin.com",
      fromName: "LinkedIn",
      fromCompany: "LinkedIn",
      to: "you@yourcompany.com",
      subject: "New connection request from Alex Chen",
      preview: "Alex Chen wants to connect with you on LinkedIn. They work at DataFlow Solutions as a Sales Director.",
      body: "Alex Chen wants to connect with you on LinkedIn.\n\nThey work at DataFlow Solutions as a Sales Director.\n\nAccept or decline this connection request.",
      timestamp: "2024-01-14T09:20:00Z",
      isRead: true,
      isStarred: false,
      isImportant: false,
      isReplied: false,
      tags: ["LinkedIn", "Connection"],
      threadId: "thread_004",
      type: "inbound",
      status: "read"
    }
  ])

  const [selectedEmails, setSelectedEmails] = useState<number[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [filterType, setFilterType] = useState('all')
  const [filterStatus, setFilterStatus] = useState('all')
  const [selectedEmail, setSelectedEmail] = useState<Email | null>(null)

  const filteredEmails = emails.filter(email => {
    const matchesSearch = email.subject.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         email.fromName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         email.fromCompany.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         email.preview.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesType = filterType === 'all' || email.type === filterType
    const matchesStatus = filterStatus === 'all' || email.status === filterStatus
    
    return matchesSearch && matchesType && matchesStatus
  })

  const unreadCount = emails.filter(email => !email.isRead).length
  const importantCount = emails.filter(email => email.isImportant).length

  const toggleEmailSelection = (id: number) => {
    setSelectedEmails(prev => 
      prev.includes(id) 
        ? prev.filter(emailId => emailId !== id)
        : [...prev, id]
    )
  }

  const selectAllEmails = () => {
    setSelectedEmails(filteredEmails.map(e => e.id))
  }

  const deselectAllEmails = () => {
    setSelectedEmails([])
  }

  const markAsRead = (id: number) => {
    setEmails(prev => prev.map(email => 
      email.id === id ? { ...email, isRead: true, status: 'read' } : email
    ))
  }

  const toggleStar = (id: number) => {
    setEmails(prev => prev.map(email => 
      email.id === id ? { ...email, isStarred: !email.isStarred } : email
    ))
  }

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diffInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60)
    
    if (diffInHours < 24) {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    } else if (diffInHours < 48) {
      return 'Yesterday'
    } else {
      return date.toLocaleDateString()
    }
  }

  return (
    <div className="content-body">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-heading-1 text-white mb-2">Inbox</h1>
            <p className="text-neutral-400 text-body-1">Manage your email communications and responses</p>
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
              <Send className="w-4 h-4 mr-2" />
              Compose
            </button>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-neutral-400 text-sm">Total Emails</p>
              <p className="text-2xl font-bold text-white">{emails.length}</p>
            </div>
            <Mail className="w-8 h-8 text-blue-400" />
          </div>
        </div>
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-neutral-400 text-sm">Unread</p>
              <p className="text-2xl font-bold text-white">{unreadCount}</p>
            </div>
            <AlertCircle className="w-8 h-8 text-yellow-400" />
          </div>
        </div>
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-neutral-400 text-sm">Important</p>
              <p className="text-2xl font-bold text-white">{importantCount}</p>
            </div>
            <Star className="w-8 h-8 text-yellow-400" />
          </div>
        </div>
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-neutral-400 text-sm">Replies</p>
              <p className="text-2xl font-bold text-white">{emails.filter(e => e.type === 'inbound').length}</p>
            </div>
            <Reply className="w-8 h-8 text-green-400" />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Email List */}
        <div className="lg:col-span-1">
          <div className="card">
            {/* Filters */}
            <div className="p-4 border-b border-neutral-700">
              <div className="flex items-center space-x-4 mb-4">
                <div className="relative flex-1">
                  <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-neutral-400" />
                  <input
                    type="text"
                    placeholder="Search emails..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="input pl-10"
                  />
                </div>
                <button className="btn-secondary">
                  <Filter className="w-4 h-4" />
                </button>
              </div>
              <div className="flex items-center space-x-4">
                <select
                  value={filterType}
                  onChange={(e) => setFilterType(e.target.value)}
                  className="input text-sm"
                >
                  <option value="all">All Types</option>
                  <option value="inbound">Inbound</option>
                  <option value="outbound">Outbound</option>
                  <option value="draft">Drafts</option>
                </select>
                <select
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value)}
                  className="input text-sm"
                >
                  <option value="all">All Status</option>
                  <option value="new">New</option>
                  <option value="read">Read</option>
                  <option value="replied">Replied</option>
                  <option value="archived">Archived</option>
                </select>
              </div>
            </div>

            {/* Email List */}
            <div className="max-h-96 overflow-y-auto">
              {filteredEmails.map((email) => (
                <div
                  key={email.id}
                  className={`p-4 border-b border-neutral-800 hover:bg-neutral-800/50 cursor-pointer ${
                    selectedEmail?.id === email.id ? 'bg-neutral-800' : ''
                  } ${!email.isRead ? 'bg-blue-900/20' : ''}`}
                  onClick={() => {
                    setSelectedEmail(email)
                    markAsRead(email.id)
                  }}
                >
                  <div className="flex items-start space-x-3">
                    <input
                      type="checkbox"
                      checked={selectedEmails.includes(email.id)}
                      onChange={(e) => {
                        e.stopPropagation()
                        toggleEmailSelection(email.id)
                      }}
                      className="mt-1 rounded border-neutral-600 bg-neutral-700"
                    />
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between mb-1">
                        <div className="flex items-center space-x-2">
                          <span className={`text-sm font-medium ${!email.isRead ? 'text-white' : 'text-neutral-300'}`}>
                            {email.fromName}
                          </span>
                          {email.isImportant && <Flag className="w-3 h-3 text-red-400" />}
                          {email.isStarred && <Star className="w-3 h-3 text-yellow-400" />}
                        </div>
                        <div className="flex items-center space-x-1">
                          <span className="text-xs text-neutral-500">{formatTimestamp(email.timestamp)}</span>
                          <button
                            onClick={(e) => {
                              e.stopPropagation()
                              toggleStar(email.id)
                            }}
                            className="p-1 hover:bg-neutral-700 rounded"
                          >
                            {email.isStarred ? (
                              <Star className="w-3 h-3 text-yellow-400" />
                            ) : (
                              <StarOff className="w-3 h-3 text-neutral-400" />
                            )}
                          </button>
                        </div>
                      </div>
                      <div className="text-sm text-neutral-400 mb-1">{email.fromCompany}</div>
                      <div className={`text-sm font-medium mb-1 ${!email.isRead ? 'text-white' : 'text-neutral-300'}`}>
                        {email.subject}
                      </div>
                      <div className="text-sm text-neutral-500 line-clamp-2">{email.preview}</div>
                      {email.tags.length > 0 && (
                        <div className="flex flex-wrap gap-1 mt-2">
                          {email.tags.slice(0, 2).map((tag, index) => (
                            <span key={index} className="px-2 py-1 bg-neutral-700 text-neutral-300 text-xs rounded">
                              {tag}
                            </span>
                          ))}
                          {email.tags.length > 2 && (
                            <span className="text-xs text-neutral-500">+{email.tags.length - 2} more</span>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Email Detail */}
        <div className="lg:col-span-2">
          {selectedEmail ? (
            <div className="card">
              <div className="p-6">
                {/* Email Header */}
                <div className="flex items-start justify-between mb-6">
                  <div className="flex items-center space-x-4">
                    <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
                      <span className="text-white text-sm font-medium">
                        {selectedEmail.fromName.split(' ').map(n => n[0]).join('')}
                      </span>
                    </div>
                    <div>
                      <div className="flex items-center space-x-2">
                        <h3 className="text-lg font-medium text-white">{selectedEmail.fromName}</h3>
                        {selectedEmail.isImportant && <Flag className="w-4 h-4 text-red-400" />}
                        {selectedEmail.isStarred && <Star className="w-4 h-4 text-yellow-400" />}
                      </div>
                      <div className="text-sm text-neutral-400">{selectedEmail.fromCompany}</div>
                      <div className="text-sm text-neutral-500">{selectedEmail.from}</div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <button className="p-2 hover:bg-neutral-700 rounded">
                      <Reply className="w-4 h-4" />
                    </button>
                    <button className="p-2 hover:bg-neutral-700 rounded">
                      <ReplyAll className="w-4 h-4" />
                    </button>
                    <button className="p-2 hover:bg-neutral-700 rounded">
                      <Forward className="w-4 h-4" />
                    </button>
                    <button className="p-2 hover:bg-neutral-700 rounded">
                      <MoreVertical className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {/* Subject */}
                <div className="mb-6">
                  <h2 className="text-xl font-medium text-white mb-2">{selectedEmail.subject}</h2>
                  <div className="text-sm text-neutral-400">
                    {new Date(selectedEmail.timestamp).toLocaleString()}
                  </div>
                </div>

                {/* Tags */}
                {selectedEmail.tags.length > 0 && (
                  <div className="flex flex-wrap gap-2 mb-6">
                    {selectedEmail.tags.map((tag, index) => (
                      <span key={index} className="px-3 py-1 bg-blue-600 text-white text-sm rounded-full">
                        {tag}
                      </span>
                    ))}
                  </div>
                )}

                {/* Email Body */}
                <div className="prose prose-invert max-w-none mb-6">
                  <div className="text-neutral-300 whitespace-pre-wrap">{selectedEmail.body}</div>
                </div>

                {/* Actions */}
                <div className="flex items-center justify-between pt-6 border-t border-neutral-700">
                  <div className="flex items-center space-x-4">
                    <button className="btn-primary">
                      <Reply className="w-4 h-4 mr-2" />
                      Reply
                    </button>
                    <button className="btn-secondary">
                      <ReplyAll className="w-4 h-4 mr-2" />
                      Reply All
                    </button>
                    <button className="btn-secondary">
                      <Forward className="w-4 h-4 mr-2" />
                      Forward
                    </button>
                  </div>
                  <div className="flex items-center space-x-2">
                    <button className="p-2 hover:bg-neutral-700 rounded">
                      <Archive className="w-4 h-4" />
                    </button>
                    <button className="p-2 hover:bg-neutral-700 rounded">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="card text-center py-12">
              <Mail className="w-12 h-12 mx-auto mb-4 text-neutral-400" />
              <h3 className="text-lg font-medium text-white mb-2">Select an email to view</h3>
              <p className="text-neutral-400">Choose an email from the list to read its contents</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
