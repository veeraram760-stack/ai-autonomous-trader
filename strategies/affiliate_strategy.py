"""
Affiliate Marketing Strategy Module
Handles passive income through affiliate links and referrals
"""

import random
import logging
from datetime import datetime
from typing import Dict, List

logger = logging.getLogger(__name__)


class AffiliateProgram:
    """Base affiliate program"""
    
    def __init__(self, program_name: str, commission_rate: float = 0.05):
        self.program_name = program_name
        self.commission_rate = commission_rate
        self.referral_links = []
        self.total_clicks = 0
        self.total_conversions = 0
        self.total_revenue = 0.0
        self.conversion_rate = 0.02  # 2% conversion rate
        self.average_order_value = 50.0
    
    def create_referral_link(self, product_name: str) -> Dict:
        """Create a new referral link"""
        link = {
            'id': len(self.referral_links) + 1,
            'product': product_name,
            'url': f"https://affiliate.{self.program_name.lower()}.com/ref_{len(self.referral_links)}",
            'created_at': datetime.now().isoformat(),
            'clicks': 0,
            'conversions': 0,
            'revenue': 0.0
        }
        
        self.referral_links.append(link)
        logger.info(f"🔗 Referral link created: {product_name}")
        return link
    
    def get_daily_clicks(self) -> Dict:
        """Simulate daily affiliate traffic"""
        daily_revenue = 0.0
        
        for link in self.referral_links:
            # Simulate daily clicks
            daily_clicks = random.randint(10, 100)
            link['clicks'] += daily_clicks
            self.total_clicks += daily_clicks
            
            # Simulate conversions
            conversions = int(daily_clicks * self.conversion_rate)
            link['conversions'] += conversions
            self.total_conversions += conversions
            
            # Calculate revenue
            revenue = conversions * self.average_order_value * self.commission_rate
            link['revenue'] += revenue
            daily_revenue += revenue
        
        self.total_revenue += daily_revenue
        return {'daily_revenue': daily_revenue, 'daily_clicks': self.total_clicks}
    
    def get_program_performance(self) -> Dict:
        """Get affiliate program performance"""
        if self.total_clicks == 0:
            click_conversion = 0
        else:
            click_conversion = (self.total_conversions / self.total_clicks) * 100
        
        return {
            'program': self.program_name,
            'total_links': len(self.referral_links),
            'total_clicks': self.total_clicks,
            'total_conversions': self.total_conversions,
            'click_to_conversion': f"{click_conversion:.2f}%",
            'total_revenue': self.total_revenue,
            'average_revenue_per_link': self.total_revenue / len(self.referral_links) if self.referral_links else 0
        }


class AmazonAssociates(AffiliateProgram):
    """Amazon Associates program"""
    
    def __init__(self):
        super().__init__("Amazon", commission_rate=0.04)
        self.average_order_value = 35.0
        self.conversion_rate = 0.03


class ClickBank(AffiliateProgram):
    """ClickBank affiliate program"""
    
    def __init__(self):
        super().__init__("ClickBank", commission_rate=0.10)
        self.average_order_value = 47.0
        self.conversion_rate = 0.01  # Lower conversion but higher value


class ReferralProgram:
    """Direct referral program for services"""
    
    def __init__(self, service_name: str, referral_reward: float = 10.0):
        self.service_name = service_name
        self.referral_reward = referral_reward  # Reward per referral
        self.referred_customers = []
        self.total_referral_revenue = 0.0
        self.customer_lifetime_value = 100.0
    
    def add_referral(self, customer_id: str) -> Dict:
        """Add a new referred customer"""
        referral = {
            'id': len(self.referred_customers) + 1,
            'customer_id': customer_id,
            'referred_at': datetime.now().isoformat(),
            'status': 'active',
            'lifetime_value': self.customer_lifetime_value,
            'commission_paid': 0.0
        }
        
        self.referred_customers.append(referral)
        return referral
    
    def get_daily_referral_revenue(self) -> float:
        """Simulate daily referral revenue"""
        daily_revenue = 0.0
        
        for referral in self.referred_customers:
            if referral['status'] == 'active':
                # Simulate monthly value spread across days
                daily_value = referral['lifetime_value'] / 30
                commission = daily_value * 0.20  # 20% commission on referral value
                
                daily_revenue += commission
                referral['commission_paid'] += commission
        
        self.total_referral_revenue += daily_revenue
        return daily_revenue
    
    def get_referral_performance(self) -> Dict:
        """Get referral program performance"""
        active_referrals = [r for r in self.referred_customers if r['status'] == 'active']
        
        return {
            'service': self.service_name,
            'total_referrals': len(self.referred_customers),
            'active_referrals': len(active_referrals),
            'total_revenue': self.total_referral_revenue,
            'average_revenue_per_referral': self.total_referral_revenue / len(self.referred_customers) if self.referred_customers else 0
        }


class AffiliateNetwork:
    """Manages multiple affiliate programs"""
    
    def __init__(self):
        self.programs: Dict[str, AffiliateProgram] = {}
        self.referral_programs: Dict[str, ReferralProgram] = {}
        self.total_affiliate_revenue = 0.0
    
    def add_affiliate_program(self, program: AffiliateProgram):
        """Add an affiliate program"""
        self.programs[program.program_name] = program
    
    def add_referral_program(self, program: ReferralProgram):
        """Add a referral program"""
        self.referral_programs[program.service_name] = program
    
    def get_daily_affiliate_revenue(self) -> Dict:
        """Get daily revenue from all affiliate programs"""
        total_daily = 0.0
        program_breakdown = {}
        
        for name, program in self.programs.items():
            result = program.get_daily_clicks()
            daily = result['daily_revenue']
            total_daily += daily
            program_breakdown[name] = daily
        
        # Add referral program revenue
        for name, program in self.referral_programs.items():
            daily = program.get_daily_referral_revenue()
            total_daily += daily
            program_breakdown[name] = daily
        
        self.total_affiliate_revenue += total_daily
        return {'total_daily_revenue': total_daily, 'breakdown': program_breakdown}
    
    def get_network_performance(self) -> Dict:
        """Get entire affiliate network performance"""
        return {
            'total_programs': len(self.programs),
            'total_referral_programs': len(self.referral_programs),
            'total_revenue': self.total_affiliate_revenue,
            'affiliate_programs': {name: program.get_program_performance() for name, program in self.programs.items()},
            'referral_programs': {name: program.get_referral_performance() for name, program in self.referral_programs.items()}
        }
