#!/usr/bin/env python3
"""
PUMP MERGED DAEMON - Unified Trading System
============================================
Combines:
- Fresh token scanning (pump.fun bonding curve)
- PUMP DOCK's institutional-grade risk management
- Twitter sentiment + on-chain signals
- Autonomous execution via Phantom

Real capital trading. Conservative risk. Aggressive opportunity hunting.
"""

import json
import subprocess
import time
import random
import asyncio
from datetime import datetime, timedelta
from collections import defaultdict

# Configuration
PUMP_PROGRAM_ID = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"

class MergedDaemon:
    """Unified trading daemon"""
    
    def __init__(self):
        self.config = {
            # Fresh token thresholds (bonding curve focus)
            "min_age_hours": 0.5,          # At least 30 min old
            "max_age_hours": 24,            # But not too old
            "min_holders": 50,
            "preferred_holders": 150,
            "min_volume_sol": 5,
            "preferred_volume_sol": 20,
            
            # Quality scoring
            "min_quality_score": 65,        # Score 0-100
            "min_twitter_hype": 30,         # Twitter mention score
            
            # Risk management (PUMP DOCK inspired)
            "risk_per_trade_pct": 0.015,    # 1.5% of portfolio
            "max_position_size_pct": 0.10,  # Max 10%
            "max_concurrent": 5,            # Max 5 positions
            "initial_stop_pct": 0.15,       # 15% stop loss
            "trailing_stop_pct": 0.10,      # 10% trailing stop
            
            # Take profit targets
            "tp_targets": [
                {"level": 2.0, "sell_pct": 0.25},    # 2x: sell 25%
                {"level": 5.0, "sell_pct": 0.30},    # 5x: sell 30%
                {"level": 10.0, "sell_pct": 0.25},   # 10x: sell 25%
                {"level": 20.0, "sell_pct": 0.20},   # 20x: sell 20%
            ],
            "moonbag_pct": 0.10,
            
            # Position management
            "max_hold_time_minutes": 240,   # 4 hours max
            "daily_loss_limit_pct": 0.05,   # 5% daily loss limit
            "max_drawdown_pct": 0.15,       # 15% max drawdown
        }
        
        self.positions = {}
        self.trade_log = []
        self.balance_sol = 0  # Will be set by Phantom
        self.peak_balance = 0
        self.daily_pnl = 0
        self.start_time = datetime.now()
        
    def calculate_quality_score(self, token_data):
        """PUMP DOCK-style quality scoring (0-100)"""
        score = 0
        
        # Volume consistency (25 pts)
        if token_data['volume_24h'] >= 50:
            score += 15
        elif token_data['volume_24h'] >= 20:
            score += 10
        elif token_data['volume_24h'] >= 5:
            score += 5
        
        # Holder growth (25 pts)
        growth_1h = token_data.get('holder_growth_1h', 0)
        if growth_1h >= 50:
            score += 10
        elif growth_1h >= 30:
            score += 7
        elif growth_1h >= 10:
            score += 4
        
        growth_24h = token_data.get('holder_growth_24h', 0)
        if growth_24h >= 150:
            score += 10
        elif growth_24h >= 100:
            score += 7
        elif growth_24h >= 50:
            score += 3
        
        # Buy/sell pressure (20 pts)
        buy_vol = token_data.get('buy_volume_1h', 0)
        sell_vol = token_data.get('sell_volume_1h', 0)
        if buy_vol > 0 and sell_vol > 0:
            ratio = buy_vol / sell_vol
            if ratio >= 2.0:
                score += 12
            elif ratio >= 1.5:
                score += 8
            elif ratio >= 1.2:
                score += 5
        
        # Price action (15 pts)
        price_change_1h = token_data.get('price_change_1h_pct', 0)
        if 5 <= price_change_1h <= 50:
            score += 8
        elif price_change_1h > 0:
            score += 4
        
        price_change_24h = token_data.get('price_change_24h_pct', 0)
        if 20 <= price_change_24h <= 200:
            score += 7
        elif price_change_24h > 0:
            score += 3
        
        # Holder quality (15 pts)
        if token_data['holder_count'] >= 200:
            score += 8
        elif token_data['holder_count'] >= 100:
            score += 5
        
        top_holder = token_data.get('top_holder_pct', 0)
        if top_holder < 10:
            score += 7
        elif top_holder < 15:
            score += 4
        
        return min(score, 100)
    
    def calculate_twitter_hype(self, token_symbol):
        """Score based on Twitter sentiment (0-100)"""
        # In production: use Twitter API
        # For now: return demo score
        return random.randint(20, 80)
    
    def can_execute_trade(self, token_data, capital_sol):
        """Check if trade can be executed (PUMP DOCK risk checks)"""
        
        # Check concurrent positions
        if len(self.positions) >= self.config["max_concurrent"]:
            return False, "Max concurrent positions reached"
        
        # Check if already in position
        if token_data['mint'] in self.positions:
            return False, "Already have position in this token"
        
        # Calculate position size
        risk_amount = self.balance_sol * self.config["risk_per_trade_pct"]
        max_position = self.balance_sol * self.config["max_position_size_pct"]
        position_size = min(risk_amount, max_position, capital_sol)
        
        if position_size < 0.1:
            return False, "Position too small"
        
        # Check risk/reward
        entry_price = token_data['price_in_sol']
        stop_price = entry_price * (1 - self.config["initial_stop_pct"])
        risk = entry_price - stop_price
        
        first_target = entry_price * 2.0
        reward = first_target - entry_price
        
        rr_ratio = reward / risk if risk > 0 else 0
        if rr_ratio < 2.0:
            return False, f"Risk/reward {rr_ratio:.2f} insufficient"
        
        return True, {"position_size": position_size, "stop_price": stop_price}
    
    def execute_buy(self, token_data, position_size):
        """Execute buy via Phantom"""
        print(f"\n🔥 EXECUTING BUY")
        print(f"   Token: {token_data['symbol']}")
        print(f"   Price: ${token_data['price_in_sol']:.10f}")
        print(f"   Size: {position_size:.3f} SOL")
        
        # In production: use phantom_buy_token here
        # For demo: simulate execution
        
        trade_id = f"trade_{int(time.time())}_{token_data['mint'][:8]}"
        
        position = {
            "trade_id": trade_id,
            "mint": token_data['mint'],
            "symbol": token_data['symbol'],
            "entry_price": token_data['price_in_sol'],
            "entry_sol": position_size,
            "tokens": position_size / token_data['price_in_sol'],
            "entry_time": time.time(),
            "highest_price": token_data['price_in_sol'],
            "targets_hit": [],
            "stops_active": False,
        }
        
        self.positions[token_data['mint']] = position
        print(f"   ✅ Position opened (ID: {trade_id})\n")
        
        return position
    
    def check_exits(self, current_prices):
        """Monitor all positions for exits (PUMP DOCK cascade)"""
        closed_trades = []
        
        for mint, position in list(self.positions.items()):
            if mint not in current_prices:
                continue
            
            current_price = current_prices[mint]
            entry_price = position['entry_price']
            profit_multiple = current_price / entry_price
            holding_minutes = (time.time() - position['entry_time']) / 60
            
            # Check stop loss
            stop_price = entry_price * (1 - self.config["initial_stop_pct"])
            if current_price <= stop_price:
                self._close_position(mint, current_price, "STOP_LOSS", closed_trades)
                continue
            
            # Check max hold time
            if holding_minutes > self.config["max_hold_time_minutes"]:
                self._close_position(mint, current_price, "MAX_HOLD_TIME", closed_trades)
                continue
            
            # Check profit targets
            for target in self.config["tp_targets"]:
                if profit_multiple >= target['level'] and target['level'] not in position['targets_hit']:
                    position['targets_hit'].append(target['level'])
                    
                    # Take partial profit
                    tokens_to_sell = position['tokens'] * target['sell_pct']
                    exit_sol = tokens_to_sell * current_price
                    
                    self.balance_sol += exit_sol
                    position['tokens'] -= tokens_to_sell
                    
                    pnl_pct = (current_price - entry_price) / entry_price * 100
                    print(f"✅ PARTIAL EXIT: {position['symbol']} at {target['level']}x (+{pnl_pct:.1f}%)")
            
            # Check trailing stop
            if profit_multiple >= 1.5:
                position['stops_active'] = True
                trail_stop = position['highest_price'] * (1 - self.config["trailing_stop_pct"])
                if current_price <= trail_stop:
                    self._close_position(mint, current_price, "TRAILING_STOP", closed_trades)
        
        return closed_trades
    
    def _close_position(self, mint, exit_price, reason, closed_trades):
        """Close a position and log the trade"""
        if mint not in self.positions:
            return
        
        position = self.positions[mint]
        entry_price = position['entry_price']
        
        # P&L calculation
        pnl_pct = (exit_price - entry_price) / entry_price * 100
        exit_sol = position['tokens'] * exit_price
        pnl_sol = exit_sol - position['entry_sol']
        
        self.balance_sol += exit_sol
        self.daily_pnl += pnl_sol
        
        # Update peak balance
        if self.balance_sol > self.peak_balance:
            self.peak_balance = self.balance_sol
        
        # Log trade
        trade = {
            "id": position['trade_id'],
            "symbol": position['symbol'],
            "entry_price": entry_price,
            "exit_price": exit_price,
            "pnl_pct": pnl_pct,
            "pnl_sol": pnl_sol,
            "reason": reason,
            "holding_minutes": (time.time() - position['entry_time']) / 60,
        }
        
        self.trade_log.append(trade)
        closed_trades.append(trade)
        
        status = "✅ WIN" if pnl_pct > 0 else "❌ LOSS"
        print(f"{status}: {position['symbol']} | {pnl_pct:+.1f}% ({pnl_sol:+.4f} SOL) | Reason: {reason}")
        
        del self.positions[mint]
    
    def get_status(self):
        """Get trading status"""
        total_trades = len(self.trade_log)
        wins = sum(1 for t in self.trade_log if t['pnl_pct'] > 0)
        losses = total_trades - wins
        total_pnl = sum(t['pnl_sol'] for t in self.trade_log)
        
        status = {
            "uptime": str(datetime.now() - self.start_time),
            "balance": self.balance_sol,
            "peak_balance": self.peak_balance,
            "positions_open": len(self.positions),
            "total_trades": total_trades,
            "wins": wins,
            "losses": losses,
            "win_rate": wins / total_trades * 100 if total_trades > 0 else 0,
            "total_pnl_sol": total_pnl,
            "daily_pnl_sol": self.daily_pnl,
        }
        
        return status


# Daemon instance
daemon = MergedDaemon()

def scan_fresh_tokens():
    """Scan for fresh tokens on bonding curve"""
    # Placeholder: would query Bitquery/Birdeye API
    return []

def evaluate_token(token_data):
    """Full evaluation pipeline"""
    
    # Quality score
    quality = daemon.calculate_quality_score(token_data)
    
    # Twitter hype
    twitter = daemon.calculate_twitter_hype(token_data.get('symbol', '?'))
    
    # Combined score
    combined = (quality * 0.6) + (twitter * 0.4)
    
    return {
        "quality": quality,
        "twitter_hype": twitter,
        "combined_score": combined,
        "qualified": combined >= daemon.config["min_quality_score"],
    }

def main():
    """Main daemon loop"""
    print(f"\n{'='*60}")
    print("🚀 PUMP MERGED DAEMON - Starting")
    print(f"{'='*60}\n")
    
    cycle = 0
    
    while True:
        cycle += 1
        
        # Scan for tokens
        fresh_tokens = scan_fresh_tokens()
        
        # Evaluate and trade
        for token in fresh_tokens:
            eval_result = evaluate_token(token)
            
            if eval_result["qualified"]:
                can_trade, result = daemon.can_execute_trade(token, 0.5)
                
                if can_trade:
                    position_size = result['position_size']
                    daemon.execute_buy(token, position_size)
        
        # Check exits
        current_prices = {}  # Would be populated from price feed
        closed = daemon.check_exits(current_prices)
        
        # Print status every N cycles
        if cycle % 60 == 0:
            status = daemon.get_status()
            print(f"\n📊 Status (Cycle {cycle}):")
            print(f"   Balance: {status['balance']:.3f} SOL")
            print(f"   Open: {status['positions_open']} | Trades: {status['total_trades']}")
            print(f"   PnL: {status['total_pnl_sol']:+.4f} SOL | Daily: {status['daily_pnl_sol']:+.4f} SOL")
            print(f"   Win Rate: {status['win_rate']:.1f}%\n")
        
        time.sleep(1)

if __name__ == "__main__":
    main()
