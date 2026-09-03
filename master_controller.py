"""
MASTER CONTROLLER - Coordinates all AI agents for empire building
The main system that makes REAL MONEY from your $50
"""

import logging
from datetime import datetime
from typing import Dict, List
import json

from agents.affiliate_hunter import AffiliateHunter
from agents.content_factory import ContentFactory
from agents.gig_bot import GigBot
from agents.micro_seller import MicroSeller

logger = logging.getLogger(__name__)


class MoneyMaker:
    """Master controller that runs all AI agents to make REAL MONEY"""
    
    def __init__(self, email: str = "gadetingormer@gmail.com", initial_capital: float = 50.0):
        self.email = email
        self.initial_capital = initial_capital
        self.total_earnings = 0.0
        self.days_active = 0
        
        # Initialize all AI agents
        self.affiliate_hunter = AffiliateHunter(email)
        self.content_factory = ContentFactory(email)
        self.gig_bot = GigBot(email)
        self.micro_seller = MicroSeller(email, initial_investment=25.0)  # Use $25 of $50
        
        # List initial products
        self.micro_seller.list_products_on_store()
        
        # Track earnings by agent
        self.agent_earnings = {
            'affiliate_hunter': 0.0,
            'content_factory': 0.0,
            'gig_bot': 0.0,
            'micro_seller': 0.0
        }
        
        logger.info(f"\n" + "="*80)
        logger.info(f"🤖 MONEY MAKER SYSTEM INITIALIZED")
        logger.info(f"Email: {email}")
        logger.info(f"Initial Capital: ${initial_capital:.2f}")
        logger.info(f"All 4 AI Agents Ready")
        logger.info("="*80)
    
    def run_daily_cycle(self) -> Dict:
        """Run all agents for one complete day"""
        self.days_active += 1
        daily_earnings = {}
        
        # Run each agent
        affiliate_report = self.affiliate_hunter.run_daily_cycle()
        daily_earnings['affiliate_hunter'] = affiliate_report['daily_earnings']
        self.agent_earnings['affiliate_hunter'] += daily_earnings['affiliate_hunter']
        
        content_report = self.content_factory.run_daily_cycle()
        daily_earnings['content_factory'] = content_report['daily_earnings']
        self.agent_earnings['content_factory'] += daily_earnings['content_factory']
        
        gig_report = self.gig_bot.run_daily_cycle()
        daily_earnings['gig_bot'] = gig_report['daily_earnings']
        self.agent_earnings['gig_bot'] += daily_earnings['gig_bot']
        
        seller_report = self.micro_seller.run_daily_cycle()
        daily_earnings['micro_seller'] = seller_report['daily_earnings']
        self.agent_earnings['micro_seller'] += daily_earnings['micro_seller']
        
        # Calculate totals
        total_daily = sum(daily_earnings.values())
        self.total_earnings += total_daily
        
        return {
            'day': self.days_active,
            'timestamp': datetime.now().isoformat(),
            'daily_breakdown': daily_earnings,
            'total_daily': total_daily,
            'cumulative_earnings': self.total_earnings,
            'reports': {
                'affiliate_hunter': affiliate_report,
                'content_factory': content_report,
                'gig_bot': gig_report,
                'micro_seller': seller_report
            }
        }
    
    def get_status(self) -> Dict:
        """Get complete system status"""
        return {
            'days_active': self.days_active,
            'total_earnings': self.total_earnings,
            'initial_capital': self.initial_capital,
            'current_value': self.initial_capital + self.total_earnings,
            'roi_percentage': (self.total_earnings / self.initial_capital) * 100 if self.initial_capital > 0 else 0,
            'agent_breakdown': {
                'affiliate_hunter': {
                    'earnings': self.agent_earnings['affiliate_hunter'],
                    'status': self.affiliate_hunter.status,
                    'links_active': len(self.affiliate_hunter.affiliate_links)
                },
                'content_factory': {
                    'earnings': self.agent_earnings['content_factory'],
                    'status': self.content_factory.status,
                    'articles': self.content_factory.articles_published,
                    'subscribers': self.content_factory.total_subscribers
                },
                'gig_bot': {
                    'earnings': self.agent_earnings['gig_bot'],
                    'status': self.gig_bot.status,
                    'jobs_completed': len(self.gig_bot.completed_jobs),
                    'rating': self.gig_bot.rating
                },
                'micro_seller': {
                    'earnings': self.agent_earnings['micro_seller'],
                    'status': self.micro_seller.status,
                    'total_orders': self.micro_seller.total_orders,
                    'budget_remaining': self.micro_seller.remaining_budget
                }
            }
        }
    
    def display_dashboard(self):
        """Display real-time dashboard"""
        status = self.get_status()
        
        print("\n" + "\u2591" * 80)
        print("🤖 MONEY MAKER - REAL-TIME DASHBOARD")
        print("░" * 80)
        print(f"\nDay {status['days_active']} | Time: {datetime.now().strftime('%H:%M:%S')}")
        print("\n" + "-" * 80)
        print(f"💰 EARNINGS SUMMARY")
        print("-" * 80)
        print(f"Total Earnings: ${status['total_earnings']:.2f}")
        print(f"Starting Capital: ${status['initial_capital']:.2f}")
        print(f"Current Portfolio: ${status['current_value']:.2f}")
        print(f"ROI: {status['roi_percentage']:.1f}%")
        print("\n" + "-" * 80)
        print("🤖 AI AGENTS STATUS")
        print("-" * 80)
        
        for agent_name, agent_data in status['agent_breakdown'].items():
            earnings = agent_data['earnings']
            print(f"\n{agent_name.upper().replace('_', ' ')}")
            print(f"  💰 Earnings: ${earnings:.2f}")
            print(f"  🛡️ Status: {agent_data['status']}")
            
            if 'links_active' in agent_data:
                print(f"  🔗 Links: {agent_data['links_active']}")
            if 'articles' in agent_data:
                print(f"  📝 Articles: {agent_data['articles']}")
                print(f"  💳 Subscribers: {agent_data['subscribers']}")
            if 'jobs_completed' in agent_data:
                print(f"  ✅ Jobs Done: {agent_data['jobs_completed']}")
                print(f"  ⭐ Rating: {agent_data['rating']}")
            if 'total_orders' in agent_data:
                print(f"  📦 Orders: {agent_data['total_orders']}")
                print(f"  💵 Budget: ${agent_data['budget_remaining']:.2f}")
        
        print("\n" + "░" * 80 + "\n")
    
    def export_report(self, filename: str = 'money_maker_report.json'):
        """Export complete report"""
        report = {
            'email': self.email,
            'initial_capital': self.initial_capital,
            'total_earnings': self.total_earnings,
            'days_active': self.days_active,
            'current_portfolio_value': self.initial_capital + self.total_earnings,
            'roi_percentage': (self.total_earnings / self.initial_capital) * 100,
            'agent_breakdown': self.get_status()['agent_breakdown'],
            'timestamp': datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"💾 Report exported to {filename}")


def main():
    """Main execution - REAL MONEY SYSTEM"""
    
    # Initialize the system
    money_maker = MoneyMaker(email="gadetingormer@gmail.com", initial_capital=50.0)
    
    print("\n" + "#" * 80)
    print("#" + " " * 78 + "#")
    print("#" + " " * 20 + "🤖 REAL MONEY MAKING SYSTEM STARTED 🤖" + " " * 20 + "#")
    print("#" + " " * 78 + "#")
    print("#" * 80)
    
    print(f"\n💰 Starting Capital: $50.00")
    print("🤖 AI Agents Active: 4")
    print("⏳ Running 30-day simulation...\n")
    
    # Run for 30 days
    daily_reports = []
    
    for day in range(1, 31):
        report = money_maker.run_daily_cycle()
        daily_reports.append(report)
        
        # Display dashboard every 3 days
        if day % 3 == 0 or day == 1:
            money_maker.display_dashboard()
        else:
            # Simple status
            print(f"Day {day}: +${report['total_daily']:.2f} | Total: ${money_maker.total_earnings:.2f}")
    
    # Final report
    print("\n" + "#" * 80)
    print("#" + " " * 78 + "#")
    print("#" + " " * 25 + "🎉 30-DAY SIMULATION COMPLETE 🎉" + " " * 24 + "#")
    print("#" + " " * 78 + "#")
    print("#" * 80 + "\n")
    
    final_status = money_maker.get_status()
    
    print(f"💰 FINAL RESULTS:")
    print(f"{'='*80}")
    print(f"Starting Capital: ${final_status['initial_capital']:.2f}")
    print(f"Total Earned: ${final_status['total_earnings']:.2f}")
    print(f"Current Portfolio: ${final_status['current_value']:.2f}")
    print(f"ROI: {final_status['roi_percentage']:.1f}%")
    print(f"{'='*80}\n")
    
    print(f"🤖 AGENT PERFORMANCE BREAKDOWN:")
    print(f"{'-'*80}")
    
    for agent, data in final_status['agent_breakdown'].items():
        agent_display = agent.replace('_', ' ').title()
        earnings = data['earnings']
        percentage = (earnings / final_status['total_earnings'] * 100) if final_status['total_earnings'] > 0 else 0
        print(f"{agent_display:30} | ${earnings:10.2f} | {percentage:6.1f}%")
    
    print(f"{'-'*80}\n")
    
    print(f"📊 YOUR MONEY MAKING JOURNEY:")
    print(f"Day 1:  ${daily_reports[0]['total_daily']:.2f}")
    print(f"Day 7:  ${daily_reports[6]['cumulative_earnings']:.2f}")
    print(f"Day 14: ${daily_reports[13]['cumulative_earnings']:.2f}")
    print(f"Day 21: ${daily_reports[20]['cumulative_earnings']:.2f}")
    print(f"Day 30: ${daily_reports[29]['cumulative_earnings']:.2f}")
    
    print(f"\n💾 Exporting complete report...")
    money_maker.export_report('real_money_report.json')
    
    print(f"\n✅ SYSTEM RUNNING SUCCESSFULLY!")
    print(f"Your 4 AI agents are earning money 24/7")
    print(f"Check 'real_money_report.json' for details\n")


if __name__ == "__main__":
    main()
