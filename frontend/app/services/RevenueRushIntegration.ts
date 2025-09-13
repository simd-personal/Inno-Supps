// Revenue Rush Ecosystem Integration Service
// Handles cross-platform communication and data sharing

export interface RevenueRushUser {
  id: string;
  name: string;
  email: string;
  plan: 'freemium' | 'pro' | 'expert' | 'enterprise';
  revenueRushAccess: boolean;
  platforms: string[];
  lastActive: string;
}

export interface PlatformData {
  platform: string;
  data: any;
  lastSync: string;
  status: 'connected' | 'disconnected' | 'error';
}

export interface CrossPlatformAnalytics {
  totalRevenue: number;
  totalUsers: number;
  conversionRate: number;
  averageOrderValue: number;
  platformBreakdown: {
    [platform: string]: {
      revenue: number;
      users: number;
      conversionRate: number;
    };
  };
}

class RevenueRushIntegration {
  private baseUrl = process.env.NEXT_PUBLIC_REVENUE_RUSH_API_URL || 'https://api.revenue-rush.com';
  private user: RevenueRushUser | null = null;

  constructor() {
    this.initializeUser();
  }

  private initializeUser() {
    // Initialize user from localStorage or API (only on client side)
    if (typeof window !== 'undefined') {
      const storedUser = localStorage.getItem('revenueRushUser');
      if (storedUser) {
        this.user = JSON.parse(storedUser);
      }
    }
  }

  // User Management
  async getUser(): Promise<RevenueRushUser | null> {
    if (this.user) return this.user;

    try {
      const response = await fetch(`${this.baseUrl}/api/user/profile`, {
        headers: {
          'Authorization': `Bearer ${this.getAuthToken()}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        this.user = await response.json();
        if (typeof window !== 'undefined') {
          localStorage.setItem('revenueRushUser', JSON.stringify(this.user));
        }
        return this.user;
      }
    } catch (error) {
      console.error('Failed to fetch user:', error);
    }

    return null;
  }

  async updateUser(updates: Partial<RevenueRushUser>): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/api/user/profile`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${this.getAuthToken()}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(updates)
      });

      if (response.ok) {
        this.user = { ...this.user, ...updates } as RevenueRushUser;
        if (typeof window !== 'undefined') {
          localStorage.setItem('revenueRushUser', JSON.stringify(this.user));
        }
        return true;
      }
    } catch (error) {
      console.error('Failed to update user:', error);
    }

    return false;
  }

  // Platform Integration
  async connectPlatform(platform: string): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/api/integrations/connect`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.getAuthToken()}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ platform })
      });

      if (response.ok) {
        const data = await response.json();
        // Update user platforms
        if (this.user) {
          this.user.platforms = [...this.user.platforms, platform];
          await this.updateUser({ platforms: this.user.platforms });
        }
        return true;
      }
    } catch (error) {
      console.error(`Failed to connect ${platform}:`, error);
    }

    return false;
  }

  async disconnectPlatform(platform: string): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/api/integrations/disconnect`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${this.getAuthToken()}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ platform })
      });

      if (response.ok) {
        // Update user platforms
        if (this.user) {
          this.user.platforms = this.user.platforms.filter(p => p !== platform);
          await this.updateUser({ platforms: this.user.platforms });
        }
        return true;
      }
    } catch (error) {
      console.error(`Failed to disconnect ${platform}:`, error);
    }

    return false;
  }

  // Data Synchronization
  async syncPlatformData(platform: string): Promise<PlatformData | null> {
    try {
      const response = await fetch(`${this.baseUrl}/api/integrations/sync/${platform}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.getAuthToken()}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        return await response.json();
      }
    } catch (error) {
      console.error(`Failed to sync ${platform} data:`, error);
    }

    return null;
  }

  async getPlatformData(platform: string): Promise<PlatformData | null> {
    try {
      const response = await fetch(`${this.baseUrl}/api/integrations/data/${platform}`, {
        headers: {
          'Authorization': `Bearer ${this.getAuthToken()}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        return await response.json();
      }
    } catch (error) {
      console.error(`Failed to get ${platform} data:`, error);
    }

    return null;
  }

  // Cross-Platform Analytics
  async getCrossPlatformAnalytics(): Promise<CrossPlatformAnalytics | null> {
    try {
      const response = await fetch(`${this.baseUrl}/api/analytics/cross-platform`, {
        headers: {
          'Authorization': `Bearer ${this.getAuthToken()}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        return await response.json();
      }
    } catch (error) {
      console.error('Failed to get cross-platform analytics:', error);
    }

    return null;
  }

  // Revenue Rush University Integration
  async getCourseRecommendations(): Promise<any[]> {
    try {
      const response = await fetch(`${this.baseUrl}/api/university/recommendations`, {
        headers: {
          'Authorization': `Bearer ${this.getAuthToken()}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        return await response.json();
      }
    } catch (error) {
      console.error('Failed to get course recommendations:', error);
    }

    return [];
  }

  async enrollInCourse(courseId: string): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/api/university/enroll`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.getAuthToken()}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ courseId })
      });

      return response.ok;
    } catch (error) {
      console.error('Failed to enroll in course:', error);
      return false;
    }
  }

  // Swipe Lounge Integration
  async getAdInspiration(category?: string): Promise<any[]> {
    try {
      const response = await fetch(`${this.baseUrl}/api/swipe-lounge/inspiration${category ? `?category=${category}` : ''}`, {
        headers: {
          'Authorization': `Bearer ${this.getAuthToken()}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        return await response.json();
      }
    } catch (error) {
      console.error('Failed to get ad inspiration:', error);
    }

    return [];
  }

  async saveAdInspiration(adData: any): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/api/swipe-lounge/save`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.getAuthToken()}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(adData)
      });

      return response.ok;
    } catch (error) {
      console.error('Failed to save ad inspiration:', error);
      return false;
    }
  }

  // RushX Integration
  async getSocialMediaInsights(): Promise<any> {
    try {
      const response = await fetch(`${this.baseUrl}/api/rushx/insights`, {
        headers: {
          'Authorization': `Bearer ${this.getAuthToken()}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        return await response.json();
      }
    } catch (error) {
      console.error('Failed to get social media insights:', error);
    }

    return null;
  }

  // Cart Rush Integration
  async getEcommerceMetrics(): Promise<any> {
    try {
      const response = await fetch(`${this.baseUrl}/api/cart-rush/metrics`, {
        headers: {
          'Authorization': `Bearer ${this.getAuthToken()}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        return await response.json();
      }
    } catch (error) {
      console.error('Failed to get ecommerce metrics:', error);
    }

    return null;
  }

  // Utility Methods
  private getAuthToken(): string {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('authToken') || '';
    }
    return '';
  }

  async isPlatformConnected(platform: string): Promise<boolean> {
    if (!this.user) return false;
    return this.user.platforms.includes(platform);
  }

  async getAvailablePlatforms(): Promise<string[]> {
    return [
      'revenue-rush-university',
      'swipe-lounge',
      'rushx',
      'cart-rush',
      'revcart'
    ];
  }

  // Real-time Updates
  subscribeToUpdates(callback: (data: any) => void): () => void {
    // TODO: Implement WebSocket connection for real-time updates
    const interval = setInterval(async () => {
      const analytics = await this.getCrossPlatformAnalytics();
      if (analytics) {
        callback(analytics);
      }
    }, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }
}

// Export singleton instance
export const revenueRushIntegration = new RevenueRushIntegration();
export default revenueRushIntegration;
