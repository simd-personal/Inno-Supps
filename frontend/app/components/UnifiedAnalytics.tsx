'use client';

import { useState, useEffect } from 'react';
import { 
  TrendingUp, 
  Users, 
  DollarSign, 
  Target, 
  BarChart3, 
  PieChart,
  Activity,
  Zap,
  RefreshCw,
  ExternalLink
} from 'lucide-react';
import { revenueRushIntegration, CrossPlatformAnalytics } from '../services/RevenueRushIntegration';

export default function UnifiedAnalytics() {
  const [analytics, setAnalytics] = useState<CrossPlatformAnalytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  useEffect(() => {
    loadAnalytics();
    
    // Set up real-time updates
    const unsubscribe = revenueRushIntegration.subscribeToUpdates((data) => {
      setAnalytics(data);
      setLastUpdated(new Date());
    });

    return () => unsubscribe();
  }, []);

  const loadAnalytics = async () => {
    setLoading(true);
    try {
      const data = await revenueRushIntegration.getCrossPlatformAnalytics();
      setAnalytics(data);
      setLastUpdated(new Date());
    } catch (error) {
      console.error('Failed to load analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const formatNumber = (num: number) => {
    return new Intl.NumberFormat('en-US').format(num);
  };

  const formatPercentage = (num: number) => {
    return `${(num * 100).toFixed(1)}%`;
  };

  if (loading) {
    return (
      <div className="content-body">
        <div className="flex items-center justify-center h-64">
          <div className="flex items-center space-x-3">
            <RefreshCw className="w-6 h-6 animate-spin text-red-600" />
            <span className="text-neutral-400">Loading analytics...</span>
          </div>
        </div>
      </div>
    );
  }

  if (!analytics) {
    return (
      <div className="content-body">
        <div className="text-center py-12">
          <div className="w-16 h-16 bg-neutral-800 rounded-full flex items-center justify-center mx-auto mb-4">
            <BarChart3 className="w-8 h-8 text-neutral-400" />
          </div>
          <h3 className="text-heading-3 text-white mb-2">No Analytics Data</h3>
          <p className="text-neutral-400 mb-6">Connect your platforms to see unified analytics</p>
          <button className="btn-primary" onClick={loadAnalytics}>
            <RefreshCw className="w-4 h-4" />
            <span>Refresh</span>
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="content-body">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-heading-1 text-white mb-2">Unified Analytics</h1>
          <p className="text-neutral-400 text-body-1">
            Cross-platform performance metrics and insights
          </p>
        </div>
        <div className="flex items-center space-x-4">
          {lastUpdated && (
            <span className="text-sm text-neutral-400">
              Last updated: {lastUpdated.toLocaleTimeString()}
            </span>
          )}
          <button className="btn-secondary" onClick={loadAnalytics}>
            <RefreshCw className="w-4 h-4" />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-red-600 rounded-lg flex items-center justify-center">
              <DollarSign className="w-6 h-6 text-white" />
            </div>
            <TrendingUp className="w-5 h-5 text-green-500" />
          </div>
          <div className="text-heading-2 text-white mb-1">
            {formatCurrency(analytics.totalRevenue)}
          </div>
          <div className="text-caption text-neutral-400">Total Revenue</div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-red-600 rounded-lg flex items-center justify-center">
              <Users className="w-6 h-6 text-white" />
            </div>
            <TrendingUp className="w-5 h-5 text-green-500" />
          </div>
          <div className="text-heading-2 text-white mb-1">
            {formatNumber(analytics.totalUsers)}
          </div>
          <div className="text-caption text-neutral-400">Total Users</div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-red-600 rounded-lg flex items-center justify-center">
              <Target className="w-6 h-6 text-white" />
            </div>
            <TrendingUp className="w-5 h-5 text-green-500" />
          </div>
          <div className="text-heading-2 text-white mb-1">
            {formatPercentage(analytics.conversionRate)}
          </div>
          <div className="text-caption text-neutral-400">Conversion Rate</div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-red-600 rounded-lg flex items-center justify-center">
              <BarChart3 className="w-6 h-6 text-white" />
            </div>
            <TrendingUp className="w-5 h-5 text-green-500" />
          </div>
          <div className="text-heading-2 text-white mb-1">
            {formatCurrency(analytics.averageOrderValue)}
          </div>
          <div className="text-caption text-neutral-400">Average Order Value</div>
        </div>
      </div>

      {/* Platform Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Platform Performance</h3>
            <p className="card-subtitle">Revenue and conversion by platform</p>
          </div>
          <div className="space-y-4">
            {Object.entries(analytics.platformBreakdown).map(([platform, data]) => (
              <div key={platform} className="flex items-center justify-between p-4 bg-neutral-800 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-red-600 rounded-lg flex items-center justify-center">
                    <Zap className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <div className="font-semibold text-white capitalize">
                      {platform.replace('-', ' ')}
                    </div>
                    <div className="text-sm text-neutral-400">
                      {formatNumber(data.users)} users
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-semibold text-white">
                    {formatCurrency(data.revenue)}
                  </div>
                  <div className="text-sm text-neutral-400">
                    {formatPercentage(data.conversionRate)} conversion
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Revenue Distribution</h3>
            <p className="card-subtitle">Revenue breakdown by platform</p>
          </div>
          <div className="space-y-3">
            {Object.entries(analytics.platformBreakdown).map(([platform, data]) => {
              const percentage = (data.revenue / analytics.totalRevenue) * 100;
              return (
                <div key={platform} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-white capitalize">
                      {platform.replace('-', ' ')}
                    </span>
                    <span className="text-sm text-neutral-400">
                      {formatCurrency(data.revenue)} ({percentage.toFixed(1)}%)
                    </span>
                  </div>
                  <div className="w-full bg-neutral-700 rounded-full h-2">
                    <div
                      className="bg-red-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${percentage}%` }}
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Quick Actions</h3>
          <p className="card-subtitle">Manage your platform integrations</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="btn-secondary">
            <ExternalLink className="w-4 h-4" />
            <span>Connect Platform</span>
          </button>
          <button className="btn-secondary">
            <Activity className="w-4 h-4" />
            <span>View Detailed Reports</span>
          </button>
          <button className="btn-secondary">
            <PieChart className="w-4 h-4" />
            <span>Export Data</span>
          </button>
        </div>
      </div>
    </div>
  );
}
