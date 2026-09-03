"""
Capital Management System
Handles budget allocation, risk management, and portfolio optimization
"""

import logging
from datetime import datetime
from typing import Dict, List

logger = logging.getLogger(__name__)


class PortfolioManager:
    """Manages overall portfolio and capital allocation"""
    
    def __init__(self, total_capital: float):
        self.total_capital = total_capital
        self.initial_capital = total_capital
        self.portfolio = {}
        self.daily_performance = []
        self.max_daily_loss = 0.05
        self.stop_loss_pct = 0.05
    
    def add_investment(self, category: str, amount: float) -> bool:
        """Add investment to portfolio"""
        if amount > self.total_capital:
            logger.warning(f"Insufficient capital for {category}")
            return False
        
        if category not in self.portfolio:
            self.portfolio[category] = []
        
        investment = {
            'amount': amount,
            'date': datetime.now().isoformat(),
            'status': 'active',
            'current_value': amount,
            'profit_loss': 0.0
        }
        
        self.portfolio[category].append(investment)
        self.total_capital -= amount
        logger.info(f"💼 Invested ${amount:.2f} in {category}")
        return True
    
    def update_position(self, category: str, position_idx: int, new_value: float) -> float:
        """Update position value and calculate P&L"""
        if category not in self.portfolio or position_idx >= len(self.portfolio[category]):
            return 0.0
        
        position = self.portfolio[category][position_idx]
        original = position['amount']
        profit_loss = new_value - original
        position['current_value'] = new_value
        position['profit_loss'] = profit_loss
        
        # Check stop loss
        loss_pct = abs(profit_loss) / original
        if loss_pct > self.stop_loss_pct and profit_loss < 0:
            position['status'] = 'closed'
            self.total_capital += new_value
            logger.warning(f"⛔ Stop loss triggered on {category}")
        
        return profit_loss
    
    def rebalance_portfolio(self):
        """Rebalance portfolio based on allocation strategy"""
        total_value = self.get_portfolio_value()
        logger.info(f"⚖️ Rebalancing portfolio. Total value: ${total_value:.2f}")
    
    def get_portfolio_value(self) -> float:
        """Get total portfolio value"""
        total = self.total_capital
        for category in self.portfolio.values():
            for position in category:
                if position['status'] == 'active':
                    total += position['current_value']
        return total
    
    def get_portfolio_summary(self) -> Dict:
        """Get portfolio summary"""
        total_value = self.get_portfolio_value()
        total_invested = self.initial_capital - self.total_capital
        total_profit_loss = total_value - self.initial_capital
        
        return {
            'initial_capital': self.initial_capital,
            'current_value': total_value,
            'cash_available': self.total_capital,
            'total_invested': total_invested,
            'profit_loss': total_profit_loss,
            'roi_percentage': (total_profit_loss / self.initial_capital) * 100 if self.initial_capital > 0 else 0,
            'categories': len(self.portfolio)
        }


class RiskManager:
    """Manages risk across all positions"""
    
    def __init__(self, initial_capital: float):
        self.initial_capital = initial_capital
        self.daily_loss_limit = initial_capital * 0.05  # 5% daily loss limit
        self.daily_loss = 0.0
        self.positions = []
        self.alerts = []
    
    def add_position(self, position: Dict) -> bool:
        """Add position with risk assessment"""
        risk_amount = position.get('amount', 0) * 0.02  # 2% risk per position
        
        if self.daily_loss + risk_amount > self.daily_loss_limit:
            logger.warning(f"⚠️ Position exceeds daily risk limit")
            self.alerts.append(f"Risk limit warning: {risk_amount}")
            return False
        
        self.positions.append(position)
        self.daily_loss += risk_amount
        return True
    
    def check_risk_exposure(self) -> Dict:
        """Check overall risk exposure"""
        return {
            'positions': len(self.positions),
            'daily_loss_limit': self.daily_loss_limit,
            'current_daily_loss': self.daily_loss,
            'exposure_percentage': (self.daily_loss / self.daily_loss_limit) * 100,
            'alerts': self.alerts
        }
    
    def reset_daily_loss(self):
        """Reset daily loss counter"""
        self.daily_loss = 0.0
        self.alerts = []


class BudgetOptimizer:
    """Optimizes capital allocation across streams"""
    
    def __init__(self, total_capital: float):
        self.total_capital = total_capital
        self.allocation_strategy = {}
        self.stream_performance = {}
    
    def optimize_allocation(self, stream_roi: Dict[str, float]) -> Dict[str, float]:
        """Optimize capital allocation based on ROI"""
        total_roi = sum(stream_roi.values())
        
        if total_roi == 0:
            # Equal allocation if no ROI data
            allocation = {stream: 1.0 / len(stream_roi) for stream in stream_roi}
        else:
            # Allocate based on ROI (higher ROI = more capital)
            allocation = {stream: roi / total_roi for stream, roi in stream_roi.items()}
        
        # Apply allocations
        result = {}
        for stream, ratio in allocation.items():
            result[stream] = self.total_capital * ratio
        
        logger.info(f"📊 Portfolio optimized based on ROI")
        return result
    
    def dynamic_reallocation(self, current_performance: Dict[str, float]) -> Dict[str, float]:
        """Dynamically reallocate based on current performance"""
        # Move capital from underperforming to outperforming streams
        top_performer = max(current_performance, key=current_performance.get)
        bottom_performer = min(current_performance, key=current_performance.get)
        
        reallocation = {}
        for stream in current_performance:
            if stream == top_performer:
                reallocation[stream] = 1.15  # 15% increase
            elif stream == bottom_performer:
                reallocation[stream] = 0.85  # 15% decrease
            else:
                reallocation[stream] = 1.0
        
        logger.info(f"🔄 Dynamic reallocation triggered")
        return reallocation
