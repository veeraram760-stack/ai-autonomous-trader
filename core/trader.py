"""
Core AI Autonomous Trader - Main Entry Point
Manages capital allocation across multiple earning streams
"""

import os
import json
from datetime import datetime
from typing import Dict, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AutonomousTrader:
    """Main AI trader that manages multiple income streams"""
    
    def __init__(self, initial_capital: float = 10.0, name: str = "MainAI"):
        self.name = name
        self.capital = initial_capital
        self.total_earned = 0.0
        self.creation_time = datetime.now()
        self.clones = []
        self.active_streams = {}
        self.performance_history = []
        
        # Capital allocation percentages for different streams
        self.allocation = {
            'crypto_trading': 0.30,      # 30% - High risk, high reward
            'stock_trading': 0.10,       # 10% - Medium risk
            'dropshipping': 0.15,        # 15% - E-commerce
            'content_creation': 0.12,   # 12% - YouTube, TikTok, blogs
            'digital_products': 0.12,   # 12% - Courses, templates, ebooks
            'affiliate_marketing': 0.08, # 8% - Passive income
            'freelancing': 0.08,         # 8% - Services
            'gig_tasks': 0.05            # 5% - Micro-tasks
        }
        
        # Expected daily ROI for each stream (conservative estimates)
        self.daily_roi = {
            'crypto_trading': 0.015,      # 1.5% daily
            'stock_trading': 0.003,       # 0.3% daily
            'dropshipping': 0.02,         # 2% daily
            'content_creation': 0.001,    # 0.1% daily (slow start)
            'digital_products': 0.01,     # 1% daily
            'affiliate_marketing': 0.005, # 0.5% daily
            'freelancing': 0.015,         # 1.5% daily
            'gig_tasks': 0.01             # 1% daily
        }
        
        logger.info(f"🤖 Initialized {self.name} with ${self.capital:.2f}")
        self._allocate_capital()
    
    def _allocate_capital(self):
        """Allocate initial capital across earning streams"""
        for stream, percentage in self.allocation.items():
            amount = self.capital * percentage
            self.active_streams[stream] = {
                'capital': amount,
                'earnings': 0.0,
                'status': 'active',
                'created_at': datetime.now().isoformat()
            }
        
        logger.info(f"✅ Capital allocated across {len(self.active_streams)} streams")
    
    def simulate_daily_earnings(self) -> float:
        """Simulate earnings from all streams for one day"""
        daily_earnings = 0.0
        
        for stream_name, stream_data in self.active_streams.items():
            if stream_data['status'] == 'active':
                stream_capital = stream_data['capital']
                roi = self.daily_roi.get(stream_name, 0.005)
                earnings = stream_capital * roi
                
                daily_earnings += earnings
                self.active_streams[stream_name]['earnings'] += earnings
        
        self.total_earned += daily_earnings
        self.capital += daily_earnings
        
        return daily_earnings
    
    def get_balance(self) -> Dict:
        """Get current balance and portfolio status"""
        return {
            'name': self.name,
            'capital': self.capital,
            'total_earned': self.total_earned,
            'active_streams': len(self.active_streams),
            'clones': len(self.clones),
            'roi_percentage': (self.total_earned / 10.0) * 100,  # Based on initial $10
            'streams_detail': self.active_streams
        }
    
    def should_spawn_clone(self) -> bool:
        """Check if we have enough capital to spawn a clone"""
        return self.capital >= 2.0
    
    def spawn_clone(self, clone_name: str = None) -> 'AutonomousTrader':
        """Create a child AI clone with allocated capital"""
        if not self.should_spawn_clone():
            logger.warning(f"❌ Insufficient capital to spawn clone. Need $2.0, have ${self.capital:.2f}")
            return None
        
        clone_capital = 1.50  # Allocate $1.50 to each clone
        self.capital -= clone_capital  # Deduct from parent
        
        if clone_name is None:
            clone_name = f"{self.name}_Clone_{len(self.clones) + 1}"
        
        clone = AutonomousTrader(initial_capital=clone_capital, name=clone_name)
        self.clones.append(clone)
        
        logger.info(f"🧬 Spawned new clone: {clone_name} with ${clone_capital:.2f}")
        return clone
    
    def get_commission_from_clones(self, commission_rate: float = 0.15) -> float:
        """Collect commission (15-20%) from all child clones"""
        total_commission = 0.0
        
        for clone in self.clones:
            clone_earnings = clone.total_earned
            commission = clone_earnings * commission_rate
            total_commission += commission
        
        return total_commission
    
    def get_total_family_wealth(self) -> Dict:
        """Calculate total wealth including all clones"""
        total_capital = self.capital
        total_earned = self.total_earned
        total_clones = len(self.clones)
        
        for clone in self.clones:
            total_capital += clone.capital
            total_earned += clone.total_earned
            total_clones += len(clone.clones)
        
        return {
            'total_capital': total_capital,
            'total_earned': total_earned,
            'total_ai_instances': 1 + len(self.clones) + sum(len(c.clones) for c in self.clones),
            'family_tree_depth': self._get_tree_depth()
        }
    
    def _get_tree_depth(self) -> int:
        """Get the depth of AI family tree"""
        if not self.clones:
            return 1
        return 1 + max(clone._get_tree_depth() for clone in self.clones)
    
    def run_day_simulation(self) -> Dict:
        """Run one complete day of earning operations"""
        daily_earnings = self.simulate_daily_earnings()
        commission = self.get_commission_from_clones()
        
        self.capital += commission
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'ai_name': self.name,
            'daily_earnings': daily_earnings,
            'commission_from_clones': commission,
            'total_daily_income': daily_earnings + commission,
            'current_balance': self.capital,
            'total_earned': self.total_earned
        }
        
        self.performance_history.append(result)
        
        # Check if we should spawn a clone
        if self.should_spawn_clone():
            clone = self.spawn_clone()
            result['clone_spawned'] = clone.name if clone else None
        
        return result
    
    def get_performance_summary(self) -> Dict:
        """Get performance summary"""
        if not self.performance_history:
            return {'message': 'No performance history yet'}
        
        total_days = len(self.performance_history)
        total_income = sum(h['total_daily_income'] for h in self.performance_history)
        average_daily = total_income / total_days if total_days > 0 else 0
        
        return {
            'days_active': total_days,
            'total_income': total_income,
            'average_daily_income': average_daily,
            'current_balance': self.capital,
            'roi_percentage': (self.total_earned / 10.0) * 100
        }
    
    def export_report(self) -> Dict:
        """Export complete AI performance report"""
        return {
            'name': self.name,
            'created_at': self.creation_time.isoformat(),
            'balance': self.get_balance(),
            'family_wealth': self.get_total_family_wealth(),
            'performance': self.get_performance_summary(),
            'clone_count': len(self.clones),
            'status': 'active'
        }


def main():
    """Main execution - simulate autonomous trader"""
    
    # Initialize main AI with $10
    main_ai = AutonomousTrader(initial_capital=10.0, name="MainAI_v1")
    
    print("\n" + "="*60)
    print("🤖 AI AUTONOMOUS TRADER SYSTEM")
    print("="*60)
    print(f"Initial Capital: $10.00")
    print(f"Earning Streams: {len(main_ai.active_streams)}")
    print("="*60 + "\n")
    
    # Simulate 30 days of operation
    day = 0
    while day < 30:
        day_result = main_ai.run_day_simulation()
        
        print(f"📊 Day {day + 1}:")
        print(f"   Daily Income: ${day_result['total_daily_income']:.4f}")
        print(f"   Balance: ${day_result['current_balance']:.2f}")
        print(f"   Total Earned: ${day_result['total_earned']:.2f}")
        
        if 'clone_spawned' in day_result and day_result['clone_spawned']:
            print(f"   🧬 {day_result['clone_spawned']} spawned!")
        
        print()
        day += 1
    
    # Final report
    print("\n" + "="*60)
    print("📈 30-DAY SIMULATION COMPLETE")
    print("="*60)
    
    family_wealth = main_ai.get_total_family_wealth()
    print(f"Total Capital: ${family_wealth['total_capital']:.2f}")
    print(f"Total Earned: ${family_wealth['total_earned']:.2f}")
    print(f"AI Instances: {family_wealth['total_ai_instances']}")
    print(f"Family Tree Depth: {family_wealth['family_tree_depth']} levels")
    print(f"ROI: {(family_wealth['total_earned'] / 10.0) * 100:.1f}%")
    print("="*60 + "\n")
    
    # Export report
    report = main_ai.export_report()
    with open('trader_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    print("✅ Report exported to trader_report.json")


if __name__ == "__main__":
    main()
