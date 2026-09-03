"""
Real-time Dashboard and Monitoring
"""

import json
from datetime import datetime
from typing import Dict, List


class Dashboard:
    """Real-time dashboard for monitoring AI performance"""
    
    def __init__(self, ai_name: str):
        self.ai_name = ai_name
        self.data = {}
        self.update_time = None
    
    def update_data(self, data: Dict):
        """Update dashboard data"""
        self.data = data
        self.update_time = datetime.now().isoformat()
    
    def display_summary(self):
        """Display dashboard summary"""
        print("\n" + "="*80)
        print(f"🤖 {self.ai_name} - DASHBOARD")
        print("="*80)
        print(f"Last Updated: {self.update_time}\n")
        
        if 'balance' in self.data:
            balance = self.data['balance']
            print(f"💰 Capital: ${balance.get('capital', 0):.2f}")
            print(f"📈 Total Earned: ${balance.get('total_earned', 0):.2f}")
            print(f"🎯 ROI: {balance.get('roi_percentage', 0):.1f}%")
            print()
        
        if 'streams' in self.data:
            print("📊 Active Streams:")
            for stream, value in self.data['streams'].items():
                print(f"   • {stream}: ${value:.2f}")
            print()
        
        if 'clones' in self.data:
            print(f"🧬 AI Clones: {self.data['clones']} active")
            print()
        
        print("="*80 + "\n")
    
    def display_detailed_report(self):
        """Display detailed performance report"""
        print("\n" + "#"*80)
        print(f"# DETAILED REPORT - {self.ai_name}")
        print("#"*80 + "\n")
        
        print(json.dumps(self.data, indent=2))
        print("\n" + "#"*80 + "\n")
    
    def export_dashboard(self, filename: str = 'dashboard_export.json'):
        """Export dashboard data"""
        export_data = {
            'ai_name': self.ai_name,
            'timestamp': self.update_time,
            'data': self.data
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"✅ Dashboard exported to {filename}")


class NetworkDashboard:
    """Dashboard for entire AI network"""
    
    def __init__(self):
        self.ai_dashboards: Dict[str, Dashboard] = {}
        self.network_data = {}
    
    def add_ai(self, ai_name: str, dashboard: Dashboard):
        """Add AI dashboard to network"""
        self.ai_dashboards[ai_name] = dashboard
    
    def update_network_data(self, data: Dict):
        """Update network data"""
        self.network_data = data
    
    def display_network_overview(self):
        """Display network overview"""
        print("\n" + "="*80)
        print("🌐 AI NETWORK OVERVIEW")
        print("="*80 + "\n")
        
        if 'total_capital' in self.network_data:
            print(f"💰 Total Network Capital: ${self.network_data['total_capital']:.2f}")
            print(f"📈 Total Network Earnings: ${self.network_data['total_earnings']:.2f}")
            print(f"🤖 Total AI Instances: {self.network_data.get('total_instances', 0)}")
            print(f"🧬 AI Families: {self.network_data.get('families', 0)}")
            print()
        
        print("Individual AI Status:")
        for ai_name, dashboard in self.ai_dashboards.items():
            if 'balance' in dashboard.data:
                balance = dashboard.data['balance']
                print(f"  • {ai_name}: ${balance.get('capital', 0):.2f} (ROI: {balance.get('roi_percentage', 0):.1f}%)")
        
        print("\n" + "="*80 + "\n")
    
    def export_network_report(self, filename: str = 'network_report.json'):
        """Export network report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'network_data': self.network_data,
            'ai_reports': {name: dashboard.data for name, dashboard in self.ai_dashboards.items()}
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Network report exported to {filename}")
