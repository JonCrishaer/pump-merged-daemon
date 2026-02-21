# 🚀 DEPLOYMENT GUIDE - pump.fun Trading Bot

## Status: PRODUCTION READY

✅ Fresh token scanner (pump.fun Terminal WebSocket)
✅ PUMP DOCK risk management (integrated)
✅ Multi-stage profit cascades (2x/5x/10x/20x)
✅ Phantom wallet execution (ready)
✅ GitHub automation (live)

---

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/JonCrishaer/pump-merged-daemon.git
cd pump-merged-daemon
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configuration

Create `config.py`:
```python
# Risk Management
RISK_PER_TRADE_PCT = 0.015        # 1.5% per trade
MAX_POSITION_SIZE_PCT = 0.10      # Max 10% position
MAX_CONCURRENT = 5                # Max 5 open positions
INITIAL_STOP_PCT = 0.15           # 15% stop loss
TRAILING_STOP_PCT = 0.10          # 10% trailing

# Token Filters
MIN_AGE_MINUTES = 2               # Minimum 2 minutes old
MAX_AGE_HOURS = 2                 # Maximum 2 hours old
MIN_HOLDERS = 50                  # Minimum 50 holders
MIN_VOLUME_SOL = 5                # Minimum 5 SOL volume

# Wallet
PHANTOM_WALLET_ADDRESS = "YOUR_WALLET_ADDRESS_HERE"
SOL_RPC = "https://mainnet.helius-rpc.com/?api-key=YOUR_KEY"

# Initial Capital
INITIAL_SOL = 2.0                 # Start with 2 SOL (scale as needed)
```

### 4. Test WebSocket Connection
```bash
python3 terminal_websocket.py
```

Should print: `✅ Connected to pump.fun Terminal WebSocket`

### 5. Run Bot

**SIMULATION MODE** (safe testing):
```bash
python3 daemon.py --simulate
```

**LIVE MODE** (real capital):
```bash
python3 daemon.py --live
```

---

## How It Works

### Real-Time Data Flow
```
pump.fun Terminal WebSocket
        ↓
    New token launch detected
        ↓
    Quality scoring (0-100)
        ↓
    Entry criteria met?
        ↓
    Risk check via PUMP DOCK
        ↓
    Phantom executes BUY
        ↓
    Real-time monitoring
        ↓
    TP1/TP2/TP3/TP4 exits
        ↓
    Trade closed, P&L logged
```

### Entry Criteria (ALL must pass)
- ✅ Token age: 2-120 minutes old
- ✅ Still on bonding curve (< $1M cap)
- ✅ Score >= 65/100
- ✅ Volume > 5 SOL (24h)
- ✅ Holders >= 50
- ✅ Can execute trade (position limit check)

### Risk Management
- **Max Risk per Trade:** 1.5% of portfolio
- **Max Position Size:** 10% of portfolio
- **Max Concurrent:** 5 positions
- **Stop Loss:** 15% (hard stop, no exceptions)
- **Trailing Stop:** 10% at 50%+ profit
- **Time Stop:** Exit if flat > 30 min
- **Daily Loss Limit:** 5% (automatic cooldown)

### Profit Targets
```
Entry: $1.00
├── TP1: +50%  → Sell 25%, move SL to breakeven
├── TP2: +100% → Sell 30%, move SL to entry
├── TP3: +200% → Sell 25%, move SL to TP1
├── TP4: +300% → Sell 20%, move SL to TP2
└── Moonbag: 10% (trailing stop)
```

---

## Monitoring

### Watch Logs
```bash
tail -f trading-daemon.log
```

### Performance Stats
```bash
python3 stats.py
```

Shows: Win rate, P&L, ROI, max drawdown

### Twitter Updates
Bot posts on @Montty_agent:
- New positions opened
- TP targets hit
- Stop losses triggered
- Daily summary

---

## Safety Checks

Before launch:
- [ ] Phantom wallet funded with 2-5 SOL
- [ ] RPC endpoint working
- [ ] Risk parameters reviewed
- [ ] Test mode passed
- [ ] Daily stop loss understood (no trading after 5% loss)

---

## Troubleshooting

**WebSocket not connecting:**
```bash
python3 -c "import websockets; print('WebSocket OK')"
```

**Phantom not executing:**
```bash
python3 -c "from phantom_handler import test; test()"
```

**Token data missing:**
```bash
python3 terminal_websocket.py --debug
```

---

## Capital Requirements

| Setup | Min Capital | Recommended |
|-------|-------------|-------------|
| Testing | 0 SOL (sim) | 0 SOL |
| Conservative | 1 SOL | 2-5 SOL |
| Aggressive | 2 SOL | 5-10 SOL |

**Why small amounts first:**
- Test system reliability
- Learn token patterns
- Adjust risk parameters
- Prove profitability
- Scale with profits

---

## Performance Targets (Realistic)

**Month 1:**
- Win Rate: 40-50%
- P&L: +10-20% (or small loss, that's OK)
- Trades: 20-50
- Goal: Proof of concept

**Month 2:**
- Win Rate: 50-60%
- P&L: +20-40%
- Trades: 50-100
- Goal: Consistent profits

**Month 3+:**
- Win Rate: 55-65%
- P&L: +50%+
- Trades: 100+
- Goal: Scale capital

---

## Do NOT Do

❌ Trade during high-risk windows (5% daily loss limit)
❌ Override stop losses (SL is sacred)
❌ Add more capital mid-trade (let system manage size)
❌ Trade illiquid tokens (volume < 5 SOL)
❌ Ignore the daily P&L log
❌ Run multiple instances (will conflict)

---

## Next Steps

1. **Fund Phantom wallet** (2-5 SOL)
2. **Run test mode** (verify everything works)
3. **Deploy live** (start trading)
4. **Monitor daily** (check logs, P&L)
5. **Scale on profits** (only if profitable)

---

## Support

Bot logs to:
- `trading-daemon.log` — All activity
- `trades.json` — Trade history
- `performance.json` — Stats

All trades are permanent record. Always auditable.

---

**Built for autonomous, disciplined trading on Solana.**

Start small. Prove the edge. Scale wins.

Let's go. 🤑
