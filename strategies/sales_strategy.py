"""
Sales & E-Commerce Strategy Module
Handles dropshipping, arbitrage, and product sales
"""

import random
import logging
from datetime import datetime
from typing import Dict, List

logger = logging.getLogger(__name__)


class SalesStrategy:
    """Base sales strategy"""
    
    def __init__(self, capital: float, strategy_type: str = "dropshipping"):
        self.capital = capital
        self.strategy_type = strategy_type
        self.inventory = []
        self.sales_history = []
        self.total_revenue = 0.0
        self.conversion_rate = 0.05  # 5% conversion
    
    def create_product(self, cost: float, retail_price: float) -> Dict:
        """Create/stock a product"""
        product = {
            'id': len(self.inventory) + 1,
            'cost': cost,
            'retail_price': retail_price,
            'margin': (retail_price - cost) / retail_price,
            'quantity': max(1, int(self.capital / cost)),
            'created_at': datetime.now().isoformat(),
            'sales': 0
        }
        
        inventory_cost = product['quantity'] * cost
        if inventory_cost <= self.capital:
            self.capital -= inventory_cost
            self.inventory.append(product)
            logger.info(f"📦 Product created: {product['id']} (${cost} cost, ${retail_price} retail)")
            return product
        
        return None
    
    def get_daily_sales(self) -> float:
        """Simulate daily sales"""
        daily_revenue = 0.0
        
        for product in self.inventory:
            # Simulate customer visits and conversions
            visitors = random.randint(50, 200)
            conversions = int(visitors * self.conversion_rate)
            
            if conversions > 0 and product['quantity'] > 0:
                sold = min(conversions, product['quantity'])
                revenue = sold * product['retail_price']
                cost = sold * product['cost']
                profit = revenue - cost
                
                product['quantity'] -= sold
                product['sales'] += sold
                daily_revenue += profit
                
                self.capital += profit
                self.total_revenue += revenue
        
        # Restock low inventory
        self._restock_inventory()
        
        return daily_revenue
    
    def _restock_inventory(self):
        """Automatically restock products with low inventory"""
        for product in self.inventory:
            if product['quantity'] < 5 and self.capital > product['cost'] * 10:
                new_stock = int((self.capital * 0.10) / product['cost'])
                stock_cost = new_stock * product['cost']
                
                if stock_cost <= self.capital:
                    product['quantity'] += new_stock
                    self.capital -= stock_cost
                    logger.info(f"📦 Restocked product {product['id']}: +{new_stock} units")
    
    def get_sales_performance(self) -> Dict:
        """Get sales metrics"""
        total_units = sum(p['sales'] for p in self.inventory)
        total_profit = self.total_revenue - sum(p['sales'] * p['cost'] for p in self.inventory)
        
        return {
            'active_products': len(self.inventory),
            'total_units_sold': total_units,
            'total_revenue': self.total_revenue,
            'total_profit': total_profit,
            'current_capital': self.capital,
            'average_margin': sum(p['margin'] for p in self.inventory) / len(self.inventory) if self.inventory else 0
        }


class DropshippingStrategy(SalesStrategy):
    """Dropshipping specific strategy"""
    
    def __init__(self, capital: float):
        super().__init__(capital, "dropshipping")
        self.conversion_rate = 0.04  # 4% conversion for dropshipping
        self._setup_products()
    
    def _setup_products(self):
        """Setup initial dropshipped products"""
        products = [
            {'cost': 5, 'retail': 15},    # 66% margin
            {'cost': 10, 'retail': 35},   # 71% margin
            {'cost': 2, 'retail': 8},     # 75% margin
            {'cost': 8, 'retail': 25},    # 68% margin
        ]
        
        for p in products:
            self.create_product(p['cost'], p['retail'])


class ArbitrageStrategy(SalesStrategy):
    """Buy low, sell high arbitrage"""
    
    def __init__(self, capital: float):
        super().__init__(capital, "arbitrage")
        self.conversion_rate = 0.08  # 8% conversion for arbitrage
        self.flip_speed = 3  # Flip inventory every 3 days
    
    def get_daily_sales(self) -> float:
        """Quick turnaround on arbitrage"""
        daily_revenue = super().get_daily_sales()
        
        # More aggressive pricing for quick sales
        for product in self.inventory:
            if product['sales'] > 20:  # High demand = increase price
                product['retail_price'] *= 1.05
        
        return daily_revenue
