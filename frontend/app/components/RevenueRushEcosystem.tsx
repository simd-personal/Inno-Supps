'use client';

import { useState } from 'react';
import { 
  GraduationCap, 
  Lightbulb, 
  Smartphone, 
  ShoppingCart, 
  ExternalLink,
  ArrowRight,
  Star,
  Users,
  TrendingUp,
  Zap
} from 'lucide-react';

interface EcosystemModule {
  id: string;
  name: string;
  description: string;
  icon: React.ComponentType<any>;
  status: 'active' | 'coming-soon' | 'beta';
  features: string[];
  pricing: string;
  external: boolean;
}

export default function RevenueRushEcosystem() {
  const [selectedModule, setSelectedModule] = useState<string | null>(null);

  const ecosystemModules: EcosystemModule[] = [
    {
      id: 'university',
      name: 'Revenue Rush University',
      description: 'Comprehensive eLearning platform with expert-led courses, community, and gamification',
      icon: GraduationCap,
      status: 'active',
      features: [
        'Expert-led courses by industry leaders',
        'Millionaire Vault with exclusive strategies',
        'Creative Workshop for ad creation',
        'Community Discord-like platform',
        'Gamified learning with achievements'
      ],
      pricing: '$100-$10,000/year',
      external: true
    },
    {
      id: 'swipe-lounge',
      name: 'Swipe Lounge',
      description: 'Creative intelligence platform for ad inspiration and collaboration',
      icon: Lightbulb,
      status: 'active',
      features: [
        'Chrome extension for ad capture',
        'Permanent ad archiving',
        'Team collaboration tools',
        'Global inspiration feed',
        'Brand research capabilities'
      ],
      pricing: '$10/user/month',
      external: true
    },
    {
      id: 'rushx',
      name: 'RushX',
      description: 'Social media management and analytics for Facebook and Instagram',
      icon: Smartphone,
      status: 'active',
      features: [
        'Centralized DM/comment management',
        'Advanced analytics and insights',
        'Content scheduling and planning',
        'Team collaboration workflows',
        'Sentiment analysis'
      ],
      pricing: 'Custom pricing',
      external: true
    },
    {
      id: 'cart-rush',
      name: 'Cart Rush',
      description: 'Shopify upsell and subscription management platform',
      icon: ShoppingCart,
      status: 'active',
      features: [
        'Advanced upsell/downsell paths',
        'Subscription management',
        'Cancellation prevention flows',
        'Surprise and delight automation',
        'Cross-store analytics'
      ],
      pricing: 'Custom pricing',
      external: true
    },
    {
      id: 'revcart',
      name: 'RevCart',
      description: 'Next-gen cart customization and smart upsells for Shopify',
      icon: Zap,
      status: 'coming-soon',
      features: [
        'Smart upsells and recommendations',
        'Tiered rewards system',
        'Cart drawer customization',
        'Mobile/desktop controls',
        'Multi-language support'
      ],
      pricing: 'Coming soon',
      external: false
    }
  ];

  const handleModuleClick = (module: EcosystemModule) => {
    if (module.external) {
      // TODO: Implement cross-platform navigation
      alert(`Redirecting to ${module.name}...`);
    } else {
      setSelectedModule(module.id);
    }
  };

  return (
    <div className="content-body">
      <div className="mb-8">
        <h1 className="text-heading-1 text-white mb-4">Revenue Rush Ecosystem</h1>
        <p className="text-neutral-400 text-body-1 mb-6">
          Access all Revenue Rush platforms and tools in one unified ecosystem
        </p>
        
        {/* Ecosystem Overview Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="card">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-red-600 rounded-lg flex items-center justify-center">
                <Star className="w-5 h-5 text-white" />
              </div>
              <div>
                <div className="text-heading-4 text-white">5</div>
                <div className="text-caption text-neutral-400">Platforms</div>
              </div>
            </div>
          </div>
          <div className="card">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-red-600 rounded-lg flex items-center justify-center">
                <Users className="w-5 h-5 text-white" />
              </div>
              <div>
                <div className="text-heading-4 text-white">10K+</div>
                <div className="text-caption text-neutral-400">Active Users</div>
              </div>
            </div>
          </div>
          <div className="card">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-red-600 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-white" />
              </div>
              <div>
                <div className="text-heading-4 text-white">$50M+</div>
                <div className="text-caption text-neutral-400">Revenue Generated</div>
              </div>
            </div>
          </div>
          <div className="card">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-red-600 rounded-lg flex items-center justify-center">
                <Zap className="w-5 h-5 text-white" />
              </div>
              <div>
                <div className="text-heading-4 text-white">99.9%</div>
                <div className="text-caption text-neutral-400">Uptime</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Platform Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {ecosystemModules.map((module) => (
          <div
            key={module.id}
            className="card cursor-pointer hover:border-red-600 transition-all duration-200"
            onClick={() => handleModuleClick(module)}
          >
            <div className="card-header">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-red-600 rounded-lg flex items-center justify-center">
                  <module.icon className="w-6 h-6 text-white" />
                </div>
                <div className="flex items-center space-x-2">
                  {module.status === 'active' && (
                    <span className="badge badge-success">Active</span>
                  )}
                  {module.status === 'coming-soon' && (
                    <span className="badge badge-warning">Coming Soon</span>
                  )}
                  {module.status === 'beta' && (
                    <span className="badge badge-secondary">Beta</span>
                  )}
                  {module.external && (
                    <ExternalLink className="w-4 h-4 text-neutral-400" />
                  )}
                </div>
              </div>
              <h3 className="card-title">{module.name}</h3>
              <p className="card-subtitle">{module.description}</p>
            </div>

            <div className="mb-4">
              <h4 className="text-sm font-semibold text-white mb-2">Key Features:</h4>
              <ul className="space-y-1">
                {module.features.slice(0, 3).map((feature, index) => (
                  <li key={index} className="text-sm text-neutral-400 flex items-center">
                    <span className="w-1 h-1 bg-red-600 rounded-full mr-2"></span>
                    {feature}
                  </li>
                ))}
                {module.features.length > 3 && (
                  <li className="text-sm text-neutral-500">
                    +{module.features.length - 3} more features
                  </li>
                )}
              </ul>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm font-semibold text-red-600">{module.pricing}</span>
              <button className="btn-ghost text-sm">
                {module.external ? 'Visit Platform' : 'Learn More'}
                <ArrowRight className="w-4 h-4 ml-1" />
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Integration Benefits */}
      <div className="mt-12">
        <h2 className="text-heading-2 text-white mb-6">Why Choose Revenue Rush Ecosystem?</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="card">
            <div className="w-12 h-12 bg-red-600 rounded-lg flex items-center justify-center mb-4">
              <Zap className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-heading-4 text-white mb-2">Seamless Integration</h3>
            <p className="text-neutral-400 text-body-2">
              All platforms work together seamlessly, sharing data and insights across your entire growth stack.
            </p>
          </div>
          <div className="card">
            <div className="w-12 h-12 bg-red-600 rounded-lg flex items-center justify-center mb-4">
              <TrendingUp className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-heading-4 text-white mb-2">Unified Analytics</h3>
            <p className="text-neutral-400 text-body-2">
              Get a complete view of your business performance across all channels and platforms.
            </p>
          </div>
          <div className="card">
            <div className="w-12 h-12 bg-red-600 rounded-lg flex items-center justify-center mb-4">
              <Users className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-heading-4 text-white mb-2">Expert Community</h3>
            <p className="text-neutral-400 text-body-2">
              Access to industry experts, mentorship, and a community of successful entrepreneurs.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
