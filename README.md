# 🚀 PUMP.FUN AUTONOMOUS TRADING SYSTEM

**Real capital trading. Conservative risk. Aggressive opportunity hunting.**

A production-ready trading daemon that combines:
- ✅ Fresh token hunting on pump.fun bonding curve
- ✅ PUMP DOCK's institutional-grade risk management
- ✅ Twitter sentiment + on-chain signals
- ✅ Autonomous execution via Phantom wallet
- ✅ Multi-stage profit cascades
- ✅ Real-time position monitoring

---

## 🎯 Core Features

### Fresh Token Discovery
- **Bonding Curve Focus:** Hunt tokens 30 min - 24 hours old
- **Quality Filtering:** Score 0-100 based on 5 dimensions
- **Twitter Integration:** Hype detection + mention velocity
- **Red Flag Detection:** Auto-reject rugs, whale dumps, bot volume

### Risk Management (PUMP DOCK-Inspired)
- **Position Sizing:** 1.5% risk per trade, max 10% per position
- **Max 5 Concurrent:** Controlled capital deployment
- **Strict Stops:** 15% initial, trailing 10% at 50%+ profit
- **Time Stops:** Exit if flat for 30 min, max 4-hour hold
- **Daily Limits:** 5% daily loss limit + 15% drawdown pause

### Profit Cascade (Multi-Stage Exits)
```
Entry: $1.00
├── TP1: 2x   → Sell 25% | Move SL to breakeven
├── TP2: 5x   → Sell 30% | Move SL to 2x
├── TP3: 10x  → Sell 25% | Move SL to 5x
├── TP4: 20x  → Sell 20% | Move SL to 10x
└── Moonbag:  → Keep 10% with trailing stop
```

### Autonomous Execution
- **No Manual Input:** Daemon runs 24/7 unattended
- **Phantom Integration:** Real wallet execution
- **All Trades Logged:** JSON records + YouTube format
- **Auto-Restart:** Self-healing on error

---

## 📊 System Architecture

```
Fresh Token Scanner
    ↓
Quality Filter (Score >= 65)
    ↓
Twitter Hype Check (Score >= 30)
    ↓
Risk Manager (Can Enter?)
    ↓
Position Open (Phantom)
    ↓
Real-Time Monitor
    ├─→ Check TP Targets
    ├─→ Check Stops
    ├─→ Check Time Limits
    └─→ Execute Exits
    ↓
Trade Log + Performance
```

---

## 🔧 Configuration

Edit `config.py`:

```python
# Fresh token thresholds
MIN_AGE_HOURS = 0.5              # 30 min minimum
MAX_AGE_HOURS = 24               # 24h maximum
MIN_HOLDERS = 50                 # Proven community
MIN_VOLUME_SOL = 5               # Liquidity check
MIN_QUALITY_SCORE = 65           # Quality threshold (0-100)
MIN_TWITTER_HYPE = 30            # Twitter mention score

# Risk management
RISK_PER_TRADE_PCT = 0.015       # 1.5% of portfolio
MAX_POSITION_SIZE_PCT = 0.10     # Max 10%
MAX_CONCURRENT_POSITIONS = 5     # Max 5 open
INITIAL_STOP_PCT = 0.15          # 15% stop loss
TRAILING_STOP_PCT = 0.10         # 10% trailing

# Take profits
TP_TARGETS = [
    (2.0, 0.25),    # 2x: sell 25%
    (5.0, 0.30),    # 5x: sell 30%
    (10.0, 0.25),   # 10x: sell 25%
    (20.0, 0.20),   # 20x: sell 20%
]
MOONBAG_PCT = 0.10               # Keep 10% for moonshot

# Safety limits
MAX_HOLD_TIME_MINUTES = 240      # 4 hours max
DAILY_LOSS_LIMIT_PCT = 0.05      # 5% daily limit
MAX_DRAWDOWN_PCT = 0.15          # 15% drawdown pause
```

---

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/JonCrishaer/pump-merged-daemon.git
cd pump-merged-daemon
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Edit config.py with your settings
cp config.example.py config.py
nano config.py
```

### 3. Set Up Phantom Wallet

```bash
# Ensure Phantom is configured in ~/.openclaw/workspace/TOOLS.md
# System will auto-execute trades via Phantom
```

### 4. Run Daemon

```bash
# Test mode (simulation)
python daemon.py --simulate

# Live mode (real capital)
python daemon.py --live
```

### 5. Monitor

```bash
# Watch the log in real-time
tail -f trading-daemon.log

# Check performance
python stats.py
```

---

## 📈 Example Trade Flow

```
[12:34:56] 🔍 Scanning fresh tokens...
[12:35:02] 📊 Found: MOON token (15 min old, 120 holders)
[12:35:02]    Quality Score: 72/100 ✅
[12:35:02]    Twitter Hype: 45/100 ✅
[12:35:02]    Combined: 68/100 → QUALIFIED
[12:35:03]    Risk Check: APPROVED
[12:35:04] 🔥 EXECUTING BUY
           Entry: $0.000012 | Size: 0.5 SOL | SL: $0.0000102
           Position opened (ID: trade_1708362904_abc123)
[12:36:15]    Current: $0.000018 (+50%) ✅ PARTIAL EXIT
           Sold 25% @ 2x | P&L: +0.003 SOL
[12:37:42]    Current: $0.00003 (+150%) ✅ PARTIAL EXIT
           Sold 30% @ 5x | P&L: +0.012 SOL
[12:45:20]    Price: $0.000025 (flat) ⏰ TIME STOP
           Exited remaining @ time limit
           Total P&L: +0.018 SOL (+45%)
[12:45:21] ✅ TRADE CLOSED | Win Rate: 67% | Daily PnL: +0.125 SOL
```

---

## 📊 Performance Metrics

The system tracks:

- **Win Rate:** % of profitable trades
- **Profit Factor:** Gross gains / Gross losses
- **Average PnL:** Mean return per trade
- **Max Drawdown:** Largest peak-to-trough
- **Sharpe Ratio:** Risk-adjusted returns
- **Daily P&L:** Daily profit/loss summary

---

## 🛡️ Risk Controls

### Hard Stops
- ✅ Stop loss always enforced (no exceptions)
- ✅ Position sizing locked
- ✅ Max concurrent positions capped
- ✅ Daily loss limit with cooldown
- ✅ Drawdown pause at 15%

### Soft Controls
- Trailing stops activate at 50% profit
- Time stops exit flat positions
- Max hold time exits long runners
- Red flag detection (automatic skip)

---

## 📝 Trading Rules

1. **Entry:** Score >= 65, qualified by all filters
2. **Position:** 1.5% risk, max 10% per token, max 5 open
3. **Stop Loss:** 15% below entry (hard stop)
4. **Take Profits:** Cascade at 2x/5x/10x/20x
5. **Exit:** Targets, SL, time stop, or max hold (whichever first)
6. **Safety:** Daily loss limit 5%, drawdown pause at 15%

---

## 🔗 Integration

### Phantom Wallet
```python
from phantom_handler import buy_token_real, sell_token_real

# Auto-executed by daemon
buy_token_real(mint, amount_sol, slippage=2)
```

### Fresh Token Scanner
```python
from token_scanner import get_fresh_tokens, evaluate_token

tokens = get_fresh_tokens()
for token in tokens:
    if evaluate_token(token)['qualified']:
        execute_trade(token)
```

### Twitter Sentiment
```python
from twitter_sentiment import get_hype_score

hype = get_hype_score("TOKEN_SYMBOL")
if hype > 30:
    # Include in selection pool
```

---

## 📚 File Structure

```
pump-merged-daemon/
├── daemon.py              # Main trading loop
├── config.py              # Configuration
├── token_scanner.py       # Fresh token discovery
├── risk_manager.py        # Position management
├── profit_manager.py      # TP/SL logic
├── twitter_integration.py # Sentiment analysis
├── phantom_handler.py     # Wallet execution
├── stats.py              # Performance reporting
├── requirements.txt      # Dependencies
└── README.md            # This file
```

---

## ⚠️ Risk Disclaimer

**Trading crypto carries significant risk of loss.**

This bot:
- Can lose money (backtest before live trading)
- Is not financial advice
- Should be tested with small amounts first
- Requires monitoring and maintenance
- May have bugs or unexpected behavior

**Always:**
- Start with paper trading
- Use funds you can afford to lose
- Monitor positions regularly
- Keep software updated

---

## 🤝 Contributing

Pull requests welcome. Areas for improvement:

- Additional token filters
- Better market regime detection
- Performance optimizations
- More risk strategies
- Dashboard UI
- Backtesting framework

---

## 📄 License

MIT License - Use at your own risk.

---

## 🎯 Status

- ✅ Fresh token scanning
- ✅ PUMP DOCK risk management merged
- ✅ Multi-stage profit cascades
- ✅ Phantom integration
- ✅ Twitter sentiment
- ⏳ Bitquery API integration (in progress)
- ⏳ ML-based token evaluation (planned)
- ⏳ Dashboard UI (planned)

---

**Built with ❤️ for autonomous trading on Solana**

Remember: Past performance does not guarantee future results. Trade responsibly.
