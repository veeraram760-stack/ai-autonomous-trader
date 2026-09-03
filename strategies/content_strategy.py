"""
Content Creation Strategy Module
Handles YouTube, TikTok, blogs, and content monetization
"""

import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List

logger = logging.getLogger(__name__)


class ContentPlatform:
    """Base content platform"""
    
    def __init__(self, platform_name: str, cpm_rate: float = 3.0):
        self.platform_name = platform_name
        self.cpm_rate = cpm_rate  # Cost per 1000 views
        self.content_pieces = []
        self.total_views = 0
        self.total_revenue = 0.0
        self.subscribers = 0
        self.growth_rate = 0.15  # 15% monthly growth
    
    def create_content(self, title: str, initial_cost: float = 0) -> Dict:
        """Create a new content piece"""
        content = {
            'id': len(self.content_pieces) + 1,
            'title': title,
            'platform': self.platform_name,
            'created_at': datetime.now().isoformat(),
            'views': 0,
            'likes': 0,
            'shares': 0,
            'comments': 0,
            'revenue': 0.0,
            'status': 'published'
        }
        
        self.content_pieces.append(content)
        logger.info(f"📹 Content created on {self.platform_name}: {title}")
        return content
    
    def get_daily_engagement(self) -> Dict:
        """Simulate daily engagement on content"""
        daily_revenue = 0.0
        
        for content in self.content_pieces:
            # Simulate viral growth
            daily_views = random.randint(100, 500) * (1 + self.growth_rate/30)
            content['views'] += daily_views
            self.total_views += daily_views
            
            # Calculate engagement
            content['likes'] += int(daily_views * 0.05)
            content['shares'] += int(daily_views * 0.01)
            content['comments'] += int(daily_views * 0.03)
            
            # Calculate revenue (CPM based)
            revenue = (content['views'] / 1000) * self.cpm_rate * 0.001  # Daily portion
            content['revenue'] += revenue
            daily_revenue += revenue
        
        # Update subscriber count
        self.subscribers = int(self.total_views * 0.001)  # 1 subscriber per 1000 views
        self.total_revenue += daily_revenue
        
        return {
            'daily_revenue': daily_revenue,
            'total_views': self.total_views,
            'subscribers': self.subscribers
        }
    
    def get_platform_performance(self) -> Dict:
        """Get platform performance metrics"""
        return {
            'platform': self.platform_name,
            'total_content': len(self.content_pieces),
            'total_views': self.total_views,
            'subscribers': self.subscribers,
            'total_revenue': self.total_revenue,
            'average_views_per_content': self.total_views / len(self.content_pieces) if self.content_pieces else 0
        }


class YouTubeStrategy(ContentPlatform):
    """YouTube specific strategy"""
    
    def __init__(self, channel_name: str):
        super().__init__("YouTube", cpm_rate=5.0)  # YouTube pays ~$5 CPM
        self.channel_name = channel_name
        self.monetization_enabled = False
        self.subscriber_threshold = 1000  # Need 1k subs for monetization
    
    def check_monetization(self) -> bool:
        """Check if monetization requirements met"""
        if self.subscribers >= self.subscriber_threshold and not self.monetization_enabled:
            self.monetization_enabled = True
            logger.info(f"✅ YouTube monetization enabled for {self.channel_name}")
        return self.monetization_enabled
    
    def get_daily_engagement(self) -> Dict:
        """YouTube specific engagement"""
        result = super().get_daily_engagement()
        self.check_monetization()
        return result


class TikTokStrategy(ContentPlatform):
    """TikTok specific strategy"""
    
    def __init__(self, account_name: str):
        super().__init__("TikTok", cpm_rate=0.25)  # TikTok pays less per view
        self.account_name = account_name
        self.growth_rate = 0.30  # Faster growth on TikTok
        self.viral_potential = 0.15  # 15% chance of going viral
    
    def get_daily_engagement(self) -> Dict:
        """TikTok with viral potential"""
        result = super().get_daily_engagement()
        
        # Simulate viral videos
        if random.random() < self.viral_potential:
            viral_boost = self.total_views * random.uniform(0.5, 2.0)
            self.total_views += viral_boost
            logger.info(f"🚀 Viral video on {self.account_name}! +{viral_boost:.0f} views")
            result['viral_boost'] = viral_boost
        
        return result


class BlogStrategy(ContentPlatform):
    """Blog strategy with affiliate links and ads"""
    
    def __init__(self, blog_name: str):
        super().__init__("Blog", cpm_rate=2.0)
        self.blog_name = blog_name
        self.affiliate_revenue = 0.0
        self.affiliate_rate = 0.06  # 6% of content revenue from affiliate links
    
    def get_daily_engagement(self) -> Dict:
        """Blog specific engagement with affiliate revenue"""
        result = super().get_daily_engagement()
        
        # Add affiliate revenue
        affiliate_revenue = result['daily_revenue'] * self.affiliate_rate
        self.affiliate_revenue += affiliate_revenue
        self.total_revenue += affiliate_revenue
        
        result['affiliate_revenue'] = affiliate_revenue
        result['total_daily_revenue'] = result['daily_revenue'] + affiliate_revenue
        
        return result


class ContentNetwork:
    """Manages multiple content platforms"""
    
    def __init__(self):
        self.platforms: Dict[str, ContentPlatform] = {}
        self.total_revenue = 0.0
    
    def add_platform(self, platform: ContentPlatform):
        """Add a new platform"""
        self.platforms[platform.platform_name] = platform
    
    def get_daily_revenue(self) -> Dict:
        """Get revenue from all platforms"""
        total_daily = 0.0
        platform_breakdown = {}
        
        for name, platform in self.platforms.items():
            result = platform.get_daily_engagement()
            daily = result.get('daily_revenue', result.get('total_daily_revenue', 0))
            total_daily += daily
            platform_breakdown[name] = daily
        
        self.total_revenue += total_daily
        return {'total_daily_revenue': total_daily, 'breakdown': platform_breakdown}
    
    def get_network_performance(self) -> Dict:
        """Get entire content network performance"""
        return {
            'total_platforms': len(self.platforms),
            'total_revenue': self.total_revenue,
            'platforms': {name: platform.get_platform_performance() for name, platform in self.platforms.items()}
        }
