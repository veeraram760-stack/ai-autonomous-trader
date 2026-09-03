"""
Trading Strategy Module
Handles crypto and stock trading operations
"""

import random
import logging
from datetime import datetime
from typing import Dict, List

logger = logging.getLogger(__name__)


class TradingStrategy:
    """Base trading strategy class"""
    
    def __init__(self, capital: float, strategy_type: str = "balanced"):
        self.capital = capital
        self.strategy_type = strategy_type
        self.positions = []
        self.trade_history = []
        self.total_profit = 0.0
        self.win_rate = 0.6  # 60% win rate
    
    def place_trade(self, amount: float, direction: str = "buy") -> Dict:
        """Place a trade"""
        if amount > self.capital:
            logger.warning(f"Insufficient capital for trade of ${amount}")
            return None
        
        trade = {
            'timestamp': datetime.now().isoformat(),
            'amount': amount,
            'direction': direction,
            'status': 'open',
            'entry_price': random.uniform(0.9, 1.1),
            'exit_price': None,
            'profit_loss': 0.0
        }
        
        self.positions.append(trade)
        logger.info(f"📊 {direction.upper()} trade placed: ${amount:.2f}")
        return trade
    
    def close_trade(self, trade_id: int) -> float:
        """Close a trade and calculate profit/loss"""
        if trade_id >= len(self.positions):
            return 0.0
        
        trade = self.positions[trade_id]
        
        # Simulate exit price based on win rate
        if random.random() < self.win_rate:
            exit_price = trade['entry_price'] * random.uniform(1.01, 1.05)  # 1-5% profit
            profit = trade['amount'] * (exit_price - trade['entry_price']) / trade['entry_price']
        else:
            exit_price = trade['entry_price'] * random.uniform(0.97, 0.99)  # 1-3% loss
            profit = trade['amount'] * (exit_price - trade['entry_price']) / trade['entry_price']
        
        trade['exit_price'] = exit_price
        trade['profit_loss'] = profit
        trade['status'] = 'closed'
        
        self.capital += profit
        self.total_profit += profit
        self.trade_history.append(trade)
        
        logger.info(f"📈 Trade closed. P/L: ${profit:.2f}")
        return profit
    
    def get_daily_earnings(self) -> float:
        """Calculate daily earnings from trading"""
        # Close 30-50% of open positions daily
        open_positions = [t for t in self.positions if t['status'] == 'open']
        close_count = max(1, len(open_positions) // 3)
        
        daily_earnings = 0.0
        for i in range(close_count):
            daily_earnings += self.close_trade(i)
        
        # Open new trades with 20% of capital
        trade_amount = self.capital * 0.20
        self.place_trade(trade_amount, "buy")
        
        return daily_earnings
    
    def get_strategy_performance(self) -> Dict:
        """Get performance metrics"""
        if not self.trade_history:
            return {'message': 'No trades yet'}
        
        winning_trades = [t for t in self.trade_history if t['profit_loss'] > 0]
        losing_trades = [t for t in self.trade_history if t['profit_loss'] < 0]
        
        return {
            'total_trades': len(self.trade_history),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': f"{(len(winning_trades) / len(self.trade_history)) * 100:.1f}%" if self.trade_history else "N/A",
            'total_profit': self.total_profit,
            'current_capital': self.capital
        }


class CryptoTradingStrategy(TradingStrategy):
    """Crypto trading with higher volatility"""
    
    def __init__(self, capital: float):
        super().__init__(capital, "crypto")
        self.win_rate = 0.55  # 55% win rate for crypto
        self.volatility = 0.08  # 8% volatility
    
    def get_daily_earnings(self) -> float:
        """Crypto specific daily earnings with higher volatility"""
        base_earnings = super().get_daily_earnings()
        # Add volatility component
        volatility_component = self.capital * self.volatility * random.uniform(-1, 1) * 0.1
        return base_earnings + volatility_component


class StockTradingStrategy(TradingStrategy):
    """Stock trading with lower volatility"""
    
    def __init__(self, capital: float):
        super().__init__(capital, "stocks")
        self.win_rate = 0.65  # 65% win rate for stocks
        self.volatility = 0.03  # 3% volatility
    
    def get_daily_earnings(self) -> float:
        """Stock specific daily earnings with lower volatility"""
        base_earnings = super().get_daily_earnings()
        # Add dividend component
        dividend = self.capital * 0.0001  # Small daily dividend
        return base_earnings + dividend
