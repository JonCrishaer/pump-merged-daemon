#!/usr/bin/env python3
"""
pump.fun Terminal WebSocket Integration
Real-time token data directly from pump.fun
"""

import asyncio
import websockets
import json
from datetime import datetime, timedelta
from collections import deque

TERMINAL_WS = "wss://pumpportal.fun/api/data"

class TerminalMonitor:
    """Real-time pump.fun token monitoring via WebSocket"""
    
    def __init__(self):
        self.tokens = {}
        self.new_tokens = deque(maxlen=100)
        self.running = False
    
    async def connect(self):
        """Connect to pump.fun Terminal WebSocket"""
        try:
            async with websockets.connect(TERMINAL_WS) as ws:
                print("✅ Connected to pump.fun Terminal WebSocket")
                self.running = True
                
                # Subscribe to new tokens
                await ws.send(json.dumps({
                    "method": "subscribeNewToken",
                }))
                
                # Listen for data
                while self.running:
                    try:
                        message = await asyncio.wait_for(ws.recv(), timeout=30)
                        await self.handle_message(message)
                    except asyncio.TimeoutError:
                        print("⚠️ WebSocket timeout, reconnecting...")
                        break
                    except Exception as e:
                        print(f"⚠️ Error: {str(e)[:80]}")
                        break
        
        except Exception as e:
            print(f"❌ WebSocket error: {str(e)[:100]}")
    
    async def handle_message(self, message):
        """Process incoming WebSocket messages"""
        try:
            data = json.loads(message)
            
            # New token launch
            if data.get("txType") == "create":
                token = {
                    "mint": data.get("mint"),
                    "symbol": data.get("symbol", "?"),
                    "name": data.get("name", ""),
                    "created_at": datetime.now().isoformat(),
                    "age_minutes": 0,
                    "initial_price": float(data.get("initialBuy", {}).get("usd", 0)),
                    "bonding_curve": True,
                }
                
                self.new_tokens.append(token)
                self.tokens[token["mint"]] = token
                
                print(f"🚀 NEW TOKEN: {token['symbol']}")
                print(f"   Mint: {token['mint']}")
                print(f"   Price: ${token['initial_price']:.10f}")
            
            # Trade update
            elif data.get("txType") == "trade":
                mint = data.get("mint")
                if mint in self.tokens:
                    token = self.tokens[mint]
                    token["last_trade_price"] = float(data.get("solAmount", 0))
                    token["last_update"] = datetime.now().isoformat()
            
            # Graduation (bonding → DEX)
            elif data.get("txType") == "graduation":
                mint = data.get("mint")
                if mint in self.tokens:
                    self.tokens[mint]["bonding_curve"] = False
                    print(f"📈 GRADUATED: {self.tokens[mint]['symbol']}")
        
        except Exception as e:
            pass

def calculate_score(token):
    """Score fresh token"""
    score = 0
    
    age = token.get("age_minutes", 0)
    
    # Age (fresh is good)
    if age < 2:
        score += 30
    elif age < 10:
        score += 25
    elif age < 30:
        score += 15
    elif age < 60:
        score += 8
    
    return score

async def monitor_live():
    """Run live monitoring"""
    monitor = TerminalMonitor()
    
    print("\n🚀 pump.fun Terminal LIVE Monitor")
    print("=" * 70)
    print("Listening for fresh token launches...\n")
    
    # Start WebSocket
    ws_task = asyncio.create_task(monitor.connect())
    
    # Monitor in background
    try:
        while True:
            # Show new tokens
            if monitor.new_tokens:
                token = monitor.new_tokens[-1]
                score = calculate_score(token)
                
                print(f"  {token['symbol']}: Score {score}/100 | Price ${token.get('initial_price', 0):.10f}")
            
            await asyncio.sleep(5)
    
    except KeyboardInterrupt:
        print("\n⛔ Stopped")
        monitor.running = False

def main():
    """Run WebSocket monitor"""
    asyncio.run(monitor_live())

if __name__ == "__main__":
    main()
