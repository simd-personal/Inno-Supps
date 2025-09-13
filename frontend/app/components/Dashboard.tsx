'use client'

import { useState, useEffect } from 'react'

export default function Dashboard() {
  console.log('Dashboard component rendering')
  
  return (
    <div className="content-body">
      <h1 className="text-heading-1 text-white mb-4">Dashboard</h1>
      <p className="text-neutral-400 mb-8 text-body-1">AI-powered growth system overview</p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-neutral-400 text-sm">Total Campaigns</p>
              <p className="text-2xl font-bold text-white">12</p>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-neutral-400 text-sm">Emails Sent</p>
              <p className="text-2xl font-bold text-white">15,420</p>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-neutral-400 text-sm">Open Rate</p>
              <p className="text-2xl font-bold text-white">42.3%</p>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-neutral-400 text-sm">Meetings Booked</p>
              <p className="text-2xl font-bold text-white">156</p>
            </div>
          </div>
        </div>
      </div>
      
      <div className="card">
        <h2 className="text-heading-4 text-white mb-6">Active Campaigns</h2>
        <p className="text-neutral-300">Dashboard is working!</p>
      </div>
    </div>
  )
}