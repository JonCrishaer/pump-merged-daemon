#!/usr/bin/env python3
"""
pump.fun Trading Bot Configuration
Production settings for live trading
"""

# ===== WALLET =====
PHANTOM_WALLET_ADDRESS = "9T7vj2oBHEcKCCn2nREQzTRr3bCKVv2Vr7dCF6hYDt7n"
SOLANA_RPC = "https://mainnet.helius-rpc.com/?api-key=1c6964fe-c76f-4769-93f3-0cee0b4d14a6"
NETWORK_ID = "solana:mainnet"

# ===== RISK MANAGEMENT =====
RISK_PER_TRADE_PCT = 0.015        # 1.5% risk per trade
MAX_POSITION_SIZE_PCT = 0.10      # Max 10% position size
MAX_CONCURRENT_POSITIONS = 5      # Max 5 open positions
INITIAL_STOP_LOSS_PCT = 0.15      # 15% hard stop
TRAILING_STOP_PCT = 0.10          # 10% trailing stop at 50%+ profit

# ===== TOKEN FILTERS =====
MIN_AGE_MINUTES = 2               # At least 2 minutes old
MAX_AGE_HOURS = 2                 # No older than 2 hours
MIN_HOLDER_COUNT = 50             # Minimum 50 holders
MIN_VOLUME_SOL_24H = 5            # Minimum 5 SOL volume
MIN_QUALITY_SCORE = 65            # Score threshold (0-100)

# ===== BONDING CURVE =====
BONDING_CURVE_CAP_MAX = 1000000   # $1M graduation point
BONDING_PROGRESS_MIN = 10         # Prefer 10%+ progress
BONDING_PROGRESS_MAX = 90         # But not > 90%

# ===== PROFIT TARGETS (cascading exits) =====
TP_TARGETS = [
    {"level": 2.0, "sell_pct": 0.25},    # 2x: sell 25%
    {"level": 5.0, "sell_pct": 0.30},    # 5x: sell 30%
    {"level": 10.0, "sell_pct": 0.25},   # 10x: sell 25%
    {"level": 20.0, "sell_pct": 0.20},   # 20x: sell 20%
]
MOONBAG_PCT = 0.10                 # Keep 10% for moon shot

# ===== TIME MANAGEMENT =====
MAX_HOLD_TIME_MINUTES = 240       # 4 hours max hold
MIN_TIME_BEFORE_EXIT_MINUTES = 30 # Wait 30 min before time stop

# ===== DAILY LIMITS =====
DAILY_LOSS_LIMIT_PCT = 0.05       # Stop trading after 5% daily loss
MAX_DRAWDOWN_PCT = 0.15           # Pause at 15% drawdown
DRAWDOWN_RECOVERY_PCT = 0.10      # Resume at 10% recovery

# ===== TRADE SIZING =====
DEFAULT_ENTRY_SOL = 0.5           # 0.5 SOL per fresh token trade
MIN_ENTRY_SOL = 0.1               # Minimum size
MAX_ENTRY_SOL = 2.0               # Maximum size (will be limited by risk %)

# ===== MARKET CONDITIONS =====
MIN_BUY_VOLUME_RATIO = 1.2        # Buy volume >= 1.2x sell volume
MAX_CONCENTRATION = 0.30          # Max holder concentration 30%
SNIPER_AVOIDANCE = True           # Avoid tokens with high dev/sniper %

# ===== TWITTER =====
TWITTER_BOT_ENABLED = True
TWITTER_POST_ON_ENTRY = True      # Tweet when entering
TWITTER_POST_ON_EXIT = True       # Tweet when exiting
TWITTER_POST_DAILY_SUMMARY = True # Daily P&L summary

# ===== API KEYS =====
BIRDEYE_API_KEY = "4abf00a4b5e647a39cbd1f52f9734a6b"
PUMP_TERMINAL_WS = "wss://pumpportal.fun/api/data"

# ===== LOGGING =====
LOG_FILE = "trading-daemon.log"
TRADE_LOG_FILE = "trades.json"
PERFORMANCE_FILE = "performance.json"
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR

# ===== MODE =====
SIMULATION_MODE = False  # Set to True to test without real trades
DRY_RUN = False         # Set to True for live monitoring without trading
VERBOSE = True          # Print detailed logs

print("✅ Configuration loaded")
print(f"   Wallet: {PHANTOM_WALLET_ADDRESS}")
print(f"   Risk/Trade: {RISK_PER_TRADE_PCT*100}%")
print(f"   Max Positions: {MAX_CONCURRENT_POSITIONS}")
print(f"   Mode: {'SIMULATION' if SIMULATION_MODE else 'LIVE'}")
