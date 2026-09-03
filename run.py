#!/usr/bin/env python3
"""
Main execution script - Run autonomous AI trader system
"""

import sys
import logging
from datetime import datetime

from core.trader import AutonomousTrader
from core.cloner import CloneNetwork
from core.manager import PortfolioManager, RiskManager
from dashboard.dashboard import Dashboard, NetworkDashboard
from utils.config import ConfigManager
from utils.logger import PerformanceLogger

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main execution function"""
    
    logger.info("🚀 Starting AI Autonomous Trader System...")
    
    # Load configuration
    config = ConfigManager()
    initial_capital = config.get('trader.initial_capital', 10.0)
    ai_name = config.get('trader.name', 'MainAI_v1')
    simulation_days = config.get('simulation.days', 30)
    
    print("\n" + "="*80)
    print("🤖 AI AUTONOMOUS TRADER SYSTEM - FULL PROJECT")
    print("="*80)
    print(f"Initial Capital: ${initial_capital:.2f}")
    print(f"AI Name: {ai_name}")
    print(f"Simulation Days: {simulation_days}")
    print("="*80 + "\n")
    
    # Initialize network and main AI
    network = CloneNetwork()
    main_ai = AutonomousTrader(initial_capital=initial_capital, name=ai_name)
    clone_manager = network.register_ai(ai_name)
    
    # Initialize monitoring
    dashboard = Dashboard(ai_name)
    network_dashboard = NetworkDashboard()
    network_dashboard.add_ai(ai_name, dashboard)
    
    performance_logger = PerformanceLogger(ai_name)
    
    # Initialize managers
    portfolio_mgr = PortfolioManager(initial_capital)
    risk_mgr = RiskManager(initial_capital)
    
    # Simulation loop
    print(f"\n📊 Starting {simulation_days}-day simulation...\n")
    
    for day in range(1, simulation_days + 1):
        # Run daily operations
        day_result = main_ai.run_day_simulation()
        
        # Log performance
        performance_logger.log_earnings(
            day_result['total_daily_income'],
            'multi_stream'
        )
        
        # Update portfolio
        portfolio_summary = portfolio_mgr.get_portfolio_summary()
        
        # Update dashboard
        balance = main_ai.get_balance()
        dashboard.update_data({
            'balance': balance,
            'streams': {stream: data['capital'] + data['earnings'] 
                       for stream, data in main_ai.active_streams.items()},
            'clones': len(main_ai.clones),
            'portfolio': portfolio_summary
        })
        
        # Display progress
        if day % 5 == 0 or day == 1:
            print(f"\n📅 Day {day}:")
            print(f"   💰 Daily Income: ${day_result['total_daily_income']:.4f}")
            print(f"   💵 Current Balance: ${day_result['current_balance']:.2f}")
            print(f"   📈 Total Earned: ${day_result['total_earned']:.2f}")
            print(f"   🤖 Active Clones: {len(main_ai.clones)}")
            
            if 'clone_spawned' in day_result and day_result['clone_spawned']:
                print(f"   ✨ {day_result['clone_spawned']} spawned!")
                performance_logger.log_clone_creation(
                    day_result['clone_spawned'],
                    1.50
                )
    
    # Final reports
    print("\n" + "="*80)
    print("📈 SIMULATION COMPLETE - FINAL REPORTS")
    print("="*80 + "\n")
    
    # AI Performance
    print("🤖 MAIN AI PERFORMANCE:")
    family_wealth = main_ai.get_total_family_wealth()
    print(f"   Total Capital: ${family_wealth['total_capital']:.2f}")
    print(f"   Total Earned: ${family_wealth['total_earned']:.2f}")
    print(f"   AI Instances: {family_wealth['total_ai_instances']}")
    print(f"   Family Tree Depth: {family_wealth['family_tree_depth']} levels")
    print(f"   ROI: {(family_wealth['total_earned'] / initial_capital) * 100:.1f}%\n")
    
    # Clone Network Stats
    if clone_manager:
        clone_stats = clone_manager.get_family_statistics()
        print(f"🧬 CLONE NETWORK STATISTICS:")
        print(f"   Total Clones Created: {clone_stats['total_clones_created']}")
        print(f"   Active Clones: {clone_stats['active_clones']}")
        print(f"   Total Clone Capital: ${clone_stats['total_clone_capital']:.2f}")
        print(f"   Total Clone Earnings: ${clone_stats['total_clone_earnings']:.2f}\n")
    
    # Portfolio Summary
    print(f"💼 PORTFOLIO SUMMARY:")
    print(f"   Initial Capital: ${portfolio_summary['initial_capital']:.2f}")
    print(f"   Current Value: ${portfolio_summary['current_value']:.2f}")
    print(f"   Total Invested: ${portfolio_summary['total_invested']:.2f}")
    print(f"   Profit/Loss: ${portfolio_summary['profit_loss']:.2f}")
    print(f"   ROI Percentage: {portfolio_summary['roi_percentage']:.1f}%\n")
    
    # Performance Summary
    perf = main_ai.get_performance_summary()
    print(f"📊 PERFORMANCE METRICS:")
    print(f"   Days Active: {perf.get('days_active', 0)}")
    print(f"   Total Income: ${perf.get('total_income', 0):.2f}")
    print(f"   Average Daily Income: ${perf.get('average_daily_income', 0):.4f}")
    print(f"   Current Balance: ${perf.get('current_balance', 0):.2f}")
    print(f"   Overall ROI: {perf.get('roi_percentage', 0):.1f}%\n")
    
    # Earning Streams Breakdown
    print(f"💸 EARNING STREAMS BREAKDOWN:")
    for stream_name, stream_data in main_ai.active_streams.items():
        capital = stream_data['capital']
        earnings = stream_data['earnings']
        total = capital + earnings
        print(f"   • {stream_name}: ${total:.2f} (Earnings: ${earnings:.4f})")
    print()
    
    print("="*80 + "\n")
    
    # Export reports
    print("💾 Exporting reports...")
    report = main_ai.export_report()
    with open('main_ai_report.json', 'w') as f:
        import json
        json.dump(report, f, indent=2)
    
    dashboard.export_dashboard('dashboard_report.json')
    performance_logger.export_logs()
    
    if clone_manager:
        clone_manager.get_family_statistics()
    
    print("✅ All reports exported successfully!\n")
    
    logger.info("✅ AI Autonomous Trader System completed successfully!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⛔ System interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}", exc_info=True)
        sys.exit(1)
