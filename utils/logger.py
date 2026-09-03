"""
Logging and Monitoring System
"""

import logging
import json
from datetime import datetime
from typing import Dict, List


class PerformanceLogger:
    """Logs AI performance metrics"""
    
    def __init__(self, ai_name: str):
        self.ai_name = ai_name
        self.logs = []
        self.metrics = {}
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        self.logger = logging.getLogger(self.ai_name)
        self.logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # File handler
        fh = logging.FileHandler(f'logs/{self.ai_name}.log')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
    
    def log_event(self, event_type: str, data: Dict):
        """Log an event"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'ai_name': self.ai_name,
            'event_type': event_type,
            'data': data
        }
        
        self.logs.append(log_entry)
        self.logger.info(f"{event_type}: {json.dumps(data)}")
    
    def log_earnings(self, amount: float, source: str):
        """Log earnings"""
        self.log_event('EARNINGS', {
            'amount': amount,
            'source': source,
            'currency': 'USD'
        })
    
    def log_trade(self, trade_data: Dict):
        """Log trade"""
        self.log_event('TRADE', trade_data)
    
    def log_clone_creation(self, clone_name: str, capital: float):
        """Log clone creation"""
        self.log_event('CLONE_CREATED', {
            'clone_name': clone_name,
            'initial_capital': capital
        })
    
    def get_logs_summary(self) -> Dict:
        """Get logs summary"""
        earnings_logs = [l for l in self.logs if l['event_type'] == 'EARNINGS']
        trade_logs = [l for l in self.logs if l['event_type'] == 'TRADE']
        clone_logs = [l for l in self.logs if l['event_type'] == 'CLONE_CREATED']
        
        return {
            'total_logs': len(self.logs),
            'earnings_events': len(earnings_logs),
            'trades': len(trade_logs),
            'clones_created': len(clone_logs)
        }
    
    def export_logs(self, filename: str = None):
        """Export logs to file"""
        if filename is None:
            filename = f'logs/{self.ai_name}_export.json'
        
        with open(filename, 'w') as f:
            json.dump(self.logs, f, indent=2)
        
        self.logger.info(f"Logs exported to {filename}")


class MetricsCollector:
    """Collects and aggregates performance metrics"""
    
    def __init__(self):
        self.metrics = {}
        self.snapshots = []
    
    def record_metric(self, ai_name: str, metric_name: str, value: float):
        """Record a metric"""
        if ai_name not in self.metrics:
            self.metrics[ai_name] = {}
        
        self.metrics[ai_name][metric_name] = value
    
    def take_snapshot(self) -> Dict:
        """Take a snapshot of all metrics"""
        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'metrics': self.metrics.copy()
        }
        self.snapshots.append(snapshot)
        return snapshot
    
    def get_metrics_summary(self, ai_name: str = None) -> Dict:
        """Get metrics summary"""
        if ai_name:
            return self.metrics.get(ai_name, {})
        return self.metrics
    
    def export_metrics(self, filename: str = 'metrics.json'):
        """Export metrics to file"""
        with open(filename, 'w') as f:
            json.dump({
                'metrics': self.metrics,
                'snapshots': self.snapshots
            }, f, indent=2)
