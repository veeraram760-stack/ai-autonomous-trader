"""
AI Cloning System - Spawn and manage child AI instances
Handles exponential growth through AI multiplication
"""

import json
from datetime import datetime
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class AIClone:
    """Represents a cloned AI instance"""
    
    def __init__(self, parent_id: str, clone_id: str, capital: float, generation: int = 1):
        self.parent_id = parent_id
        self.clone_id = clone_id
        self.capital = capital
        self.generation = generation
        self.created_at = datetime.now().isoformat()
        self.total_earned = 0.0
        self.child_clones = []
        self.status = 'active'
        self.performance_metrics = {
            'days_active': 0,
            'total_income': 0.0,
            'average_daily_income': 0.0
        }
    
    def update_earnings(self, earnings: float):
        """Update clone earnings"""
        self.total_earned += earnings
        self.capital += earnings
        self.performance_metrics['total_income'] += earnings
    
    def to_dict(self) -> Dict:
        """Convert clone to dictionary"""
        return {
            'clone_id': self.clone_id,
            'parent_id': self.parent_id,
            'generation': self.generation,
            'capital': self.capital,
            'total_earned': self.total_earned,
            'created_at': self.created_at,
            'status': self.status,
            'child_count': len(self.child_clones),
            'performance': self.performance_metrics
        }


class CloneManager:
    """Manages AI cloning and family tree"""
    
    def __init__(self, parent_ai_id: str):
        self.parent_ai_id = parent_ai_id
        self.clones: Dict[str, AIClone] = {}
        self.clone_counter = 0
        self.family_tree = {}
        self.total_clones_created = 0
        self.commission_rate = 0.15  # 15% commission from child earnings
    
    def create_clone(self, capital: float, generation: int = 1) -> AIClone:
        """Create a new AI clone with allocated capital"""
        self.clone_counter += 1
        clone_id = f"{self.parent_ai_id}_Clone_{self.clone_counter}"
        
        clone = AIClone(
            parent_id=self.parent_ai_id,
            clone_id=clone_id,
            capital=capital,
            generation=generation
        )
        
        self.clones[clone_id] = clone
        self.total_clones_created += 1
        
        logger.info(f"✅ Created clone: {clone_id} (Gen {generation}) with ${capital:.2f}")
        return clone
    
    def get_clone(self, clone_id: str) -> AIClone:
        """Retrieve a clone by ID"""
        return self.clones.get(clone_id)
    
    def list_all_clones(self) -> List[Dict]:
        """List all clones with their details"""
        return [clone.to_dict() for clone in self.clones.values()]
    
    def calculate_total_clone_wealth(self) -> Dict:
        """Calculate total wealth from all clones"""
        total_capital = 0.0
        total_earned = 0.0
        active_clones = 0
        
        for clone in self.clones.values():
            if clone.status == 'active':
                total_capital += clone.capital
                total_earned += clone.total_earned
                active_clones += 1
        
        return {
            'total_capital': total_capital,
            'total_earned': total_earned,
            'active_clones': active_clones,
            'total_clones': len(self.clones)
        }
    
    def collect_commissions(self) -> float:
        """Collect commission (15%) from all active clones"""
        total_commission = 0.0
        
        for clone in self.clones.values():
            if clone.status == 'active' and clone.total_earned > 0:
                commission = clone.total_earned * self.commission_rate
                total_commission += commission
                # Reset earned for next collection period
                clone.total_earned = 0.0
        
        logger.info(f"💰 Collected ${total_commission:.4f} commission from clones")
        return total_commission
    
    def get_family_statistics(self) -> Dict:
        """Get comprehensive family statistics"""
        wealth_data = self.calculate_total_clone_wealth()
        
        return {
            'parent_ai': self.parent_ai_id,
            'total_clones_created': self.total_clones_created,
            'active_clones': wealth_data['active_clones'],
            'total_clone_capital': wealth_data['total_capital'],
            'total_clone_earnings': wealth_data['total_earned'],
            'commission_rate': f"{self.commission_rate * 100}%",
            'generations': self._count_generations()
        }
    
    def _count_generations(self) -> int:
        """Count number of generations in clone family"""
        if not self.clones:
            return 1
        return max(clone.generation for clone in self.clones.values()) + 1


class CloneNetwork:
    """Manages entire AI network with multiple family trees"""
    
    def __init__(self):
        self.ai_families: Dict[str, CloneManager] = {}
        self.network_created_at = datetime.now().isoformat()
        self.total_network_wealth = 0.0
        self.network_statistics = {
            'total_ai_instances': 0,
            'total_active_streams': 0,
            'network_roi': 0.0
        }
    
    def register_ai(self, ai_id: str) -> CloneManager:
        """Register a new AI as parent with its clone manager"""
        manager = CloneManager(ai_id)
        self.ai_families[ai_id] = manager
        logger.info(f"📡 Registered AI family: {ai_id}")
        return manager
    
    def get_manager(self, ai_id: str) -> CloneManager:
        """Get clone manager for specific AI"""
        return self.ai_families.get(ai_id)
    
    def get_network_wealth(self) -> Dict:
        """Calculate total network wealth across all AI families"""
        total_capital = 0.0
        total_earned = 0.0
        total_instances = 0
        
        for manager in self.ai_families.values():
            wealth = manager.calculate_total_clone_wealth()
            total_capital += wealth['total_capital']
            total_earned += wealth['total_earned']
            total_instances += wealth['total_clones']
        
        return {
            'total_network_capital': total_capital,
            'total_network_earnings': total_earned,
            'total_ai_instances': total_instances,
            'total_families': len(self.ai_families),
            'average_capital_per_instance': total_capital / total_instances if total_instances > 0 else 0
        }
    
    def get_network_report(self) -> Dict:
        """Generate comprehensive network report"""
        wealth = self.get_network_wealth()
        
        families_data = []
        for ai_id, manager in self.ai_families.items():
            families_data.append({
                'ai_id': ai_id,
                'statistics': manager.get_family_statistics()
            })
        
        return {
            'network_created_at': self.network_created_at,
            'network_wealth': wealth,
            'families': families_data,
            'network_status': 'active'
        }
    
    def export_network_data(self, filename: str = 'network_report.json'):
        """Export entire network data to JSON"""
        report = self.get_network_report()
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        logger.info(f"✅ Network data exported to {filename}")


class CloneStrategy:
    """Intelligent cloning strategy based on performance"""
    
    def __init__(self, parent_capital: float, clone_capital: float = 1.50):
        self.parent_capital = parent_capital
        self.clone_capital = clone_capital
        self.cloning_history = []
    
    def should_clone(self, current_balance: float) -> bool:
        """Determine if we should create a new clone"""
        return current_balance >= (self.clone_capital * 1.5)  # Need 1.5x the clone capital
    
    def calculate_optimal_clone_capital(self, available_capital: float) -> float:
        """Calculate optimal capital allocation for new clone"""
        # Allocate 20-25% of available capital to clone
        allocation = available_capital * 0.20
        # But don't exceed base clone capital * 2
        return min(allocation, self.clone_capital * 2)
    
    def get_cloning_schedule(self, initial_capital: float, days: int = 30) -> List[Dict]:
        """Generate optimal cloning schedule for given period"""
        schedule = []
        current_capital = initial_capital
        day = 0
        daily_roi = 0.008  # 0.8% daily average
        
        while day < days:
            current_capital += current_capital * daily_roi
            
            if current_capital >= self.clone_capital * 1.5:
                clone_capital = self.calculate_optimal_clone_capital(current_capital)
                current_capital -= clone_capital
                
                schedule.append({
                    'day': day,
                    'action': 'spawn_clone',
                    'clone_capital': clone_capital,
                    'remaining_capital': current_capital
                })
            
            day += 1
        
        return schedule
    
    def log_clone_event(self, event: Dict):
        """Log cloning event"""
        self.cloning_history.append({
            'timestamp': datetime.now().isoformat(),
            'event': event
        })


def simulate_clone_network():
    """Simulate a network of cloned AIs"""
    
    print("\n" + "="*70)
    print("🧬 AI CLONING NETWORK SIMULATION")
    print("="*70 + "\n")
    
    # Create network
    network = CloneNetwork()
    
    # Register main AI
    main_manager = network.register_ai("MainAI_v1")
    
    # Create cloning strategy
    strategy = CloneStrategy(parent_capital=10.0, clone_capital=1.50)
    
    # Simulate cloning over 30 days
    current_capital = 10.0
    daily_roi = 0.008
    
    print(f"Initial Capital: ${current_capital:.2f}")
    print(f"Daily ROI: {daily_roi * 100}%\n")
    
    for day in range(1, 31):
        # Simulate earnings
        daily_income = current_capital * daily_roi
        current_capital += daily_income
        
        # Check if should clone
        if strategy.should_clone(current_capital):
            clone_capital = strategy.calculate_optimal_clone_capital(current_capital)
            current_capital -= clone_capital
            
            clone = main_manager.create_clone(capital=clone_capital, generation=1)
            strategy.log_clone_event({
                'type': 'clone_created',
                'clone_id': clone.clone_id,
                'capital': clone_capital
            })
            
            print(f"Day {day}: 🧬 Clone spawned! Capital: ${clone_capital:.2f}")
        
        if day % 5 == 0:
            stats = main_manager.get_family_statistics()
            print(f"Day {day}: Balance: ${current_capital:.2f}, Clones: {stats['active_clones']}")
    
    # Final report
    print("\n" + "="*70)
    print("📊 NETWORK FINAL REPORT")
    print("="*70)
    
    final_stats = main_manager.get_family_statistics()
    print(f"Parent AI: {final_stats['parent_ai']}")
    print(f"Total Clones Created: {final_stats['total_clones_created']}")
    print(f"Active Clones: {final_stats['active_clones']}")
    print(f"Total Clone Capital: ${final_stats['total_clone_capital']:.2f}")
    print(f"Commission Rate: {final_stats['commission_rate']}")
    print(f"Generations: {final_stats['generations']}")
    print("="*70 + "\n")


if __name__ == "__main__":
    simulate_clone_network()
