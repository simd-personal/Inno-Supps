'use client';

import { useState, useEffect } from 'react';
import { 
  Bell, 
  X, 
  CheckCircle, 
  AlertCircle, 
  Info, 
  ExternalLink,
  Zap,
  Users,
  DollarSign,
  TrendingUp
} from 'lucide-react';

interface Notification {
  id: string;
  type: 'success' | 'warning' | 'error' | 'info';
  title: string;
  message: string;
  platform: string;
  timestamp: Date;
  actionUrl?: string;
  read: boolean;
}

export default function CrossPlatformNotifications() {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [showNotifications, setShowNotifications] = useState(false);

  useEffect(() => {
    // Mock notifications - in real app, these would come from the API
    const mockNotifications: Notification[] = [
      {
        id: '1',
        type: 'success',
        title: 'Revenue Rush University',
        message: 'New course "Advanced B2B Growth Strategies" is now available',
        platform: 'revenue-rush-university',
        timestamp: new Date(Date.now() - 1000 * 60 * 30), // 30 minutes ago
        actionUrl: 'https://university.revenue-rush.com/courses/advanced-b2b-growth',
        read: false
      },
      {
        id: '2',
        type: 'info',
        title: 'Swipe Lounge',
        message: '5 new ad inspirations saved to your "B2B Campaigns" board',
        platform: 'swipe-lounge',
        timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2), // 2 hours ago
        actionUrl: 'https://swipe.revenue-rush.com/boards/b2b-campaigns',
        read: false
      },
      {
        id: '3',
        type: 'warning',
        title: 'RushX',
        message: 'Instagram engagement dropped 15% this week. Consider posting more frequently.',
        platform: 'rushx',
        timestamp: new Date(Date.now() - 1000 * 60 * 60 * 4), // 4 hours ago
        actionUrl: 'https://rushx.revenue-rush.com/analytics',
        read: true
      },
      {
        id: '4',
        type: 'success',
        title: 'Cart Rush',
        message: 'Upsell conversion rate increased by 23% after implementing new flow',
        platform: 'cart-rush',
        timestamp: new Date(Date.now() - 1000 * 60 * 60 * 6), // 6 hours ago
        actionUrl: 'https://cart.revenue-rush.com/analytics',
        read: true
      },
      {
        id: '5',
        type: 'error',
        title: 'RevCart',
        message: 'Integration failed. Please reconnect your Shopify store.',
        platform: 'revcart',
        timestamp: new Date(Date.now() - 1000 * 60 * 60 * 8), // 8 hours ago
        actionUrl: 'https://revcart.revenue-rush.com/integrations',
        read: false
      }
    ];

    setNotifications(mockNotifications);
  }, []);

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'success':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'warning':
        return <AlertCircle className="w-5 h-5 text-yellow-500" />;
      case 'error':
        return <AlertCircle className="w-5 h-5 text-red-500" />;
      case 'info':
        return <Info className="w-5 h-5 text-blue-500" />;
      default:
        return <Bell className="w-5 h-5 text-neutral-400" />;
    }
  };

  const getPlatformIcon = (platform: string) => {
    switch (platform) {
      case 'revenue-rush-university':
        return <Zap className="w-4 h-4 text-red-500" />;
      case 'swipe-lounge':
        return <Users className="w-4 h-4 text-red-500" />;
      case 'rushx':
        return <TrendingUp className="w-4 h-4 text-red-500" />;
      case 'cart-rush':
        return <DollarSign className="w-4 h-4 text-red-500" />;
      case 'revcart':
        return <Zap className="w-4 h-4 text-red-500" />;
      default:
        return <Bell className="w-4 h-4 text-neutral-400" />;
    }
  };

  const formatTimestamp = (timestamp: Date) => {
    const now = new Date();
    const diff = now.getTime() - timestamp.getTime();
    const minutes = Math.floor(diff / (1000 * 60));
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));

    if (minutes < 60) {
      return `${minutes}m ago`;
    } else if (hours < 24) {
      return `${hours}h ago`;
    } else {
      return `${days}d ago`;
    }
  };

  const markAsRead = (id: string) => {
    setNotifications(prev => 
      prev.map(notification => 
        notification.id === id 
          ? { ...notification, read: true }
          : notification
      )
    );
  };

  const markAllAsRead = () => {
    setNotifications(prev => 
      prev.map(notification => ({ ...notification, read: true }))
    );
  };

  const deleteNotification = (id: string) => {
    setNotifications(prev => prev.filter(notification => notification.id !== id));
  };

  const unreadCount = notifications.filter(n => !n.read).length;

  return (
    <div className="relative">
      {/* Notification Bell */}
      <button
        onClick={() => setShowNotifications(!showNotifications)}
        className="relative p-2 hover:bg-neutral-700 rounded-lg transition-colors"
      >
        <Bell className="w-5 h-5" />
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-600 text-white text-xs rounded-full flex items-center justify-center">
            {unreadCount}
          </span>
        )}
      </button>

      {/* Notifications Dropdown */}
      {showNotifications && (
        <div className="absolute right-0 top-12 w-96 bg-neutral-800 border border-neutral-700 rounded-lg shadow-xl z-50">
          <div className="p-4 border-b border-neutral-700">
            <div className="flex items-center justify-between">
              <h3 className="text-heading-4 text-white">Notifications</h3>
              <div className="flex items-center space-x-2">
                {unreadCount > 0 && (
                  <button
                    onClick={markAllAsRead}
                    className="text-sm text-red-600 hover:text-red-500"
                  >
                    Mark all read
                  </button>
                )}
                <button
                  onClick={() => setShowNotifications(false)}
                  className="p-1 hover:bg-neutral-700 rounded"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>

          <div className="max-h-96 overflow-y-auto">
            {notifications.length === 0 ? (
              <div className="p-6 text-center">
                <Bell className="w-8 h-8 text-neutral-400 mx-auto mb-2" />
                <p className="text-neutral-400">No notifications</p>
              </div>
            ) : (
              <div className="divide-y divide-neutral-700">
                {notifications.map((notification) => (
                  <div
                    key={notification.id}
                    className={`p-4 hover:bg-neutral-700 transition-colors ${
                      !notification.read ? 'bg-neutral-750' : ''
                    }`}
                  >
                    <div className="flex items-start space-x-3">
                      <div className="flex-shrink-0 mt-1">
                        {getNotificationIcon(notification.type)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between mb-1">
                          <h4 className="text-sm font-semibold text-white truncate">
                            {notification.title}
                          </h4>
                          <div className="flex items-center space-x-2">
                            {getPlatformIcon(notification.platform)}
                            <span className="text-xs text-neutral-400">
                              {formatTimestamp(notification.timestamp)}
                            </span>
                          </div>
                        </div>
                        <p className="text-sm text-neutral-400 mb-2">
                          {notification.message}
                        </p>
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-2">
                            {notification.actionUrl && (
                              <a
                                href={notification.actionUrl}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-xs text-red-600 hover:text-red-500 flex items-center"
                              >
                                <ExternalLink className="w-3 h-3 mr-1" />
                                View
                              </a>
                            )}
                          </div>
                          <div className="flex items-center space-x-2">
                            {!notification.read && (
                              <button
                                onClick={() => markAsRead(notification.id)}
                                className="text-xs text-neutral-400 hover:text-white"
                              >
                                Mark read
                              </button>
                            )}
                            <button
                              onClick={() => deleteNotification(notification.id)}
                              className="text-xs text-neutral-400 hover:text-red-500"
                            >
                              <X className="w-3 h-3" />
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="p-4 border-t border-neutral-700">
            <button className="w-full text-sm text-red-600 hover:text-red-500 text-center">
              View all notifications
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
