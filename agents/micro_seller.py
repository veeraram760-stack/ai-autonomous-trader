"""
Micro-Seller AI - Dropshipping automation with $20-30 investment
MEDIUM RISK - Only pay when customer buys (no upfront inventory)
"""

import random
import logging
from datetime import datetime
from typing import Dict, List

logger = logging.getLogger(__name__)


class MicroSeller:
    """Automates dropshipping with minimal investment"""
    
    def __init__(self, email: str = "gadetingormer@gmail.com", initial_investment: float = 25.0):
        self.email = email
        self.name = "MicroSeller_AI"
        self.daily_earnings = 0.0
        self.total_earnings = 0.0
        self.status = 'active'
        self.investment = initial_investment
        self.remaining_budget = initial_investment
        
        # Store setup
        self.store_name = "AmazonDeals_Store"
        self.store_url = f"https://shop.{self.store_name.lower()}.com"
        self.store_setup_cost = 10  # Shopify basic = $10
        self.remaining_budget -= self.store_setup_cost
        
        # Products database
        self.products = [
            {'name': 'Wireless Earbuds', 'supplier_cost': 8, 'retail_price': 25, 'margin': 0.68},
            {'name': 'Phone Stand', 'supplier_cost': 2, 'retail_price': 12, 'margin': 0.83},
            {'name': 'USB-C Cable', 'supplier_cost': 1.5, 'retail_price': 8, 'margin': 0.81},
            {'name': 'Bluetooth Speaker', 'supplier_cost': 12, 'retail_price': 35, 'margin': 0.66},
            {'name': 'Phone Case', 'supplier_cost': 2, 'retail_price': 10, 'margin': 0.80},
            {'name': 'Screen Protector', 'supplier_cost': 0.50, 'retail_price': 4, 'margin': 0.88},
            {'name': 'Laptop Cooling Pad', 'supplier_cost': 5, 'retail_price': 18, 'margin': 0.72},
            {'name': 'Webcam', 'supplier_cost': 15, 'retail_price': 45, 'margin': 0.67},
        ]
        
        self.listed_products = []
        self.orders = []
        self.total_orders = 0
        self.total_spent_on_inventory = 0
        
        logger.info(f"📋 Micro-Seller initialized with ${initial_investment:.2f} budget")
    
    def list_products_on_store(self) -> List[Dict]:
        """List products on dropshipping store"""
        # List 4-6 products
        selected_products = random.sample(self.products, random.randint(4, 6))
        
        for product in selected_products:
            listing = {
                'id': len(self.listed_products) + 1,
                'name': product['name'],
                'supplier_cost': product['supplier_cost'],
                'retail_price': product['retail_price'],
                'margin': product['margin'],
                'views': 0,
                'added_to_cart': 0,
                'sales': 0,
                'revenue': 0.0,
                'profit': 0.0,
                'listed_date': datetime.now().isoformat(),
            }
            
            self.listed_products.append(listing)
            logger.info(f"📋 Listed: {product['name']} at ${product['retail_price']}")
        
        return selected_products
    
    def simulate_store_traffic(self) -> Dict:
        """Simulate daily store visitors and purchases"""
        daily_revenue = 0.0
        daily_orders = 0
        
        for listing in self.listed_products:
            # Simulate daily views
            daily_views = random.randint(20, 150)
            listing['views'] += daily_views
            
            # 3-8% add to cart rate
            add_to_cart = int(daily_views * random.uniform(0.03, 0.08))
            listing['added_to_cart'] += add_to_cart
            
            # 20-40% of add to cart convert to sales
            conversions = int(add_to_cart * random.uniform(0.20, 0.40))
            
            if conversions > 0:
                # For each conversion, purchase from supplier and ship to customer
                for _ in range(conversions):
                    # You pay supplier cost
                    supplier_payment = listing['supplier_cost']
                    
                    # Customer pays retail
                    customer_payment = listing['retail_price']
                    
                    # Your profit
                    profit_per_order = customer_payment - supplier_payment
                    
                    # Only complete order if you have budget for supplier
                    if self.remaining_budget >= supplier_payment:
                        self.remaining_budget -= supplier_payment
                        self.total_spent_on_inventory += supplier_payment
                        
                        order = {
                            'order_id': len(self.orders) + 1,
                            'product': listing['name'],
                            'customer_paid': customer_payment,
                            'supplier_cost': supplier_payment,
                            'profit': profit_per_order,
                            'order_date': datetime.now().isoformat(),
                            'status': 'shipped'
                        }
                        
                        self.orders.append(order)
                        listing['sales'] += 1
                        listing['revenue'] += customer_payment
                        listing['profit'] += profit_per_order
                        
                        daily_revenue += profit_per_order
                        daily_orders += 1
                        
                        logger.info(f"📦 Sale: {listing['name']} - Profit: ${profit_per_order:.2f}")
        
        self.daily_earnings += daily_revenue
        self.total_earnings += daily_revenue
        self.total_orders += daily_orders
        
        return {
            'daily_sales': daily_orders,
            'daily_revenue': daily_revenue,
            'budget_remaining': self.remaining_budget
        }
    
    def reinvest_profits(self) -> float:
        """Reinvest 30% of profits into more inventory"""
        if self.total_earnings > 20:
            reinvestment = self.total_earnings * 0.30
            self.remaining_budget += reinvestment
            logger.info(f"💵 Reinvested ${reinvestment:.2f} into inventory")
            return reinvestment
        return 0.0
    
    def scale_store(self) -> bool:
        """Scale store if profitable enough"""
        if self.total_earnings > 50 and len(self.listed_products) < 20:
            # Add more products
            new_products = random.sample(self.products, min(3, len(self.products) - len(self.listed_products)))
            for product in new_products:
                if product not in [p for p in self.listed_products]:
                    listing = {
                        'id': len(self.listed_products) + 1,
                        'name': product['name'],
                        'supplier_cost': product['supplier_cost'],
                        'retail_price': product['retail_price'],
                        'margin': product['margin'],
                        'views': 0,
                        'added_to_cart': 0,
                        'sales': 0,
                        'revenue': 0.0,
                        'profit': 0.0,
                        'listed_date': datetime.now().isoformat(),
                    }
                    self.listed_products.append(listing)
            
            logger.info(f"🚀 Store scaled! Now listing {len(self.listed_products)} products")
            return True
        return False
    
    def get_daily_report(self) -> Dict:
        """Get daily earnings report"""
        return {
            'date': datetime.now().isoformat(),
            'agent': self.name,
            'daily_earnings': self.daily_earnings,
            'total_earnings': self.total_earnings,
            'total_orders': self.total_orders,
            'products_listed': len(self.listed_products),
            'budget_remaining': self.remaining_budget,
            'total_spent': self.total_spent_on_inventory,
            'status': self.status
        }
    
    def run_daily_cycle(self) -> Dict:
        """Run one complete daily cycle"""
        self.daily_earnings = 0.0
        
        # Simulate store traffic and sales
        self.simulate_store_traffic()
        
        # Reinvest profits
        self.reinvest_profits()
        
        # Try to scale
        self.scale_store()
        
        logger.info(f"💰 Daily earnings: ${self.daily_earnings:.2f}")
        return self.get_daily_report()


if __name__ == "__main__":
    seller = MicroSeller(initial_investment=25.0)
    seller.list_products_on_store()
    
    print("\n" + "="*60)
    print("📋 MICRO-SELLER AI - DAILY REPORT")
    print("="*60 + "\n")
    
    for day in range(1, 8):
        report = seller.run_daily_cycle()
        print(f"Day {day}:")
        print(f"  Daily Earnings: ${report['daily_earnings']:.2f}")
        print(f"  Total Earnings: ${report['total_earnings']:.2f}")
        print(f"  Total Orders: {report['total_orders']}")
        print(f"  Budget Left: ${report['budget_remaining']:.2f}")
        print(f"  Products: {report['products_listed']}")
        print()
    
    print("\n" + "="*60)
    print(f"📊 WEEKLY SUMMARY")
    print("="*60)
    print(f"Total Earnings: ${seller.total_earnings:.2f}")
    print(f"Average Daily: ${seller.total_earnings/7:.2f}")
    print(f"Total Sales: {seller.total_orders}")
    print(f"Budget Remaining: ${seller.remaining_budget:.2f}")
    print(f"Status: {seller.status}")
    print("="*60 + "\n")
