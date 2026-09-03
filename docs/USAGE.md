# AI Autonomous Trader - Usage Guide

## Quick Start

### Installation

```bash
git clone https://github.com/veeraram760-stack/ai-autonomous-trader.git
cd ai-autonomous-trader
pip install -r requirements.txt
```

### Run the System

```bash
python run.py
```

## Configuration

Edit `config/config.yaml` to customize:

- Initial capital
- Capital allocation percentages
- Daily ROI targets
- Cloning parameters
- Risk management settings

## Module Documentation

### Core Modules

**`core/trader.py`** - Main autonomous trader
- Capital management
- Multi-stream earning allocation
- Daily simulation
- Performance tracking

**`core/cloner.py`** - AI cloning system
- Spawn child AI instances
- Family tree management
- Network coordination
- Commission collection

**`core/manager.py`** - Capital management
- Portfolio optimization
- Risk management
- Budget allocation
- Rebalancing

### Strategy Modules

**`strategies/trading_strategy.py`** - Trading operations
- Crypto trading
- Stock trading
- Trade execution and P&L

**`strategies/sales_strategy.py`** - E-commerce and sales
- Dropshipping
- Product inventory
- Arbitrage trading

**`strategies/content_strategy.py`** - Content monetization
- YouTube strategy
- TikTok strategy
- Blog strategy
- Content platform management

**`strategies/affiliate_strategy.py`** - Affiliate marketing
- Affiliate programs
- Referral programs
- Commission collection

### Utilities

**`dashboard/dashboard.py`** - Real-time monitoring
- AI performance dashboard
- Network overview
- Report generation

**`utils/logger.py`** - Performance logging
- Event tracking
- Metrics collection
- Export functionality

**`utils/config.py`** - Configuration management
- Load/save settings
- Dynamic configuration
- Config validation

## Output Files

After running the system, check:

- `main_ai_report.json` - Detailed AI performance report
- `dashboard_report.json` - Dashboard snapshot
- `logs/` - Detailed event logs
- `network_report.json` - Full network statistics

## Examples

### Create Custom Trader

```python
from core.trader import AutonomousTrader

trader = AutonomousTrader(initial_capital=10.0, name="CustomAI")
trader.run_day_simulation()
print(trader.get_balance())
```

### Spawn Clones

```python
from core.cloner import CloneNetwork

network = CloneNetwork()
manager = network.register_ai("MainAI")

if trader.should_spawn_clone():
    clone = trader.spawn_clone("Clone_1")
```

### Monitor Performance

```python
from dashboard.dashboard import Dashboard

dashboard = Dashboard("MainAI")
dashboard.update_data(trader.get_balance())
dashboard.display_summary()
dashboard.export_dashboard()
```

## Troubleshooting

### Low earnings
- Increase daily ROI in config
- Allocate more capital to high-ROI streams
- Enable more revenue streams

### Clones not spawning
- Check minimum capital requirement ($2.0)
- Verify cloning is enabled in config
- Check commission settings

### Performance degradation
- Review risk management settings
- Check for position conflicts
- Rebalance portfolio

## Advanced Features

### Custom Strategies

Extend strategy classes:

```python
from strategies.trading_strategy import TradingStrategy

class CustomStrategy(TradingStrategy):
    def get_daily_earnings(self):
        # Your custom logic
        pass
```

### Network Scaling

Manage multiple AI families:

```python
from core.cloner import CloneNetwork

network = CloneNetwork()
manager1 = network.register_ai("AI_1")
manager2 = network.register_ai("AI_2")

network_wealth = network.get_network_wealth()
```

## Performance Tips

1. **Start conservative** - Begin with 0.5-1% daily ROI, increase gradually
2. **Diversify** - Use all 8+ earning streams for stability
3. **Clone early** - Spawn clones as soon as you have $2.0
4. **Monitor closely** - Check daily reports and logs
5. **Optimize allocation** - Use dynamic reallocation based on performance

## Support

For issues or questions:
- Check logs in `logs/` directory
- Review configuration in `config/config.yaml`
- See exported reports for detailed metrics

---

**Goal: Turn $10 into $10,000+ in 12 months! 🚀**
