#!/usr/bin/env python3
"""
LIVE Bitquery Integration for pump.fun Fresh Tokens
Production-ready token scanner
"""

import requests
import json
from datetime import datetime, timedelta

BITQUERY_API = "https://streaming.bitquery.io/graphql"
BITQUERY_KEY = "ory_at_OXBAjQIM09VDoKdcKK826AxxnpeHO1DSFQluKTUqTUY.bQ9HfWcb6LB2z9TuDjvJgjqKwXdQoSnc61egX_go9Tc"

def get_fresh_pumpfun_trades(limit=20):
    """Get latest pump.fun trades (fresh tokens)"""
    
    query = """
    query {
      Solana {
        DEXTrades(
          where: {
            Trade: {
              Dex: {
                ProtocolName: { is: "pump.fun" }
              }
            }
          }
          orderBy: { descending: Block_Time }
          limit: { count: """ + str(limit) + """ }
        ) {
          Trade {
            Buy {
              Currency {
                Symbol
                MintAddress
              }
              Amount
            }
            Sell {
              Currency {
                Symbol
              }
              Amount
            }
          }
          Block {
            Time
          }
          Transaction {
            Signature
          }
        }
      }
    }
    """
    
    try:
        response = requests.post(
            BITQUERY_API,
            headers={
                "Authorization": f"Bearer {BITQUERY_KEY}",
                "Content-Type": "application/json"
            },
            json={"query": query},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if "data" in data and data["data"]:
                trades = data.get("data", {}).get("Solana", {}).get("DEXTrades", [])
                return parse_trades(trades)
            elif "errors" in data:
                print(f"⚠️ GraphQL error: {data['errors'][0].get('message', 'Unknown')}")
                return []
        else:
            print(f"⚠️ HTTP error: {response.status_code}")
            return []
    
    except Exception as e:
        print(f"❌ Error: {str(e)[:100]}")
        return []

def parse_trades(trades):
    """Convert trades into token list with metrics"""
    tokens = []
    
    for trade in trades:
        if not trade:
            continue
        
        try:
            buy_info = trade.get("Trade", {}).get("Buy", {})
            currency = buy_info.get("Currency", {})
            
            mint = currency.get("MintAddress")
            symbol = currency.get("Symbol", "?")
            
            if not mint or mint == "So11111111111111111111111111111111111111112":  # Skip SOL
                continue
            
            block_time = trade.get("Block", {}).get("Time")
            age_minutes = calculate_age(block_time)
            
            # Skip if too old (> 2 hours)
            if age_minutes > 120:
                continue
            
            token = {
                "mint": mint,
                "symbol": symbol,
                "age_minutes": age_minutes,
                "block_time": block_time,
                "tx_signature": trade.get("Transaction", {}).get("Signature"),
            }
            
            tokens.append(token)
        
        except Exception as e:
            continue
    
    return tokens

def calculate_age(timestamp_str):
    """Calculate token age in minutes"""
    try:
        if not timestamp_str:
            return 9999
        
        token_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        age = (datetime.now(token_time.tzinfo) - token_time).total_seconds() / 60
        return max(age, 0)
    except:
        return 9999

def main():
    """Live test"""
    print("\n🚀 Bitquery LIVE Integration")
    print("=" * 60)
    print()
    
    print("🔍 Fetching fresh pump.fun tokens...")
    tokens = get_fresh_pumpfun_trades(limit=20)
    
    if tokens:
        print(f"✅ Found {len(tokens)} fresh tokens:\n")
        
        for i, token in enumerate(tokens[:10], 1):
            print(f"  [{i}] {token['symbol']}")
            print(f"      Mint: {token['mint'][:12]}...")
            print(f"      Age: {token['age_minutes']:.1f} min")
            print(f"      TX: {token['tx_signature'][:8]}...")
            print()
    else:
        print("⚠️ No fresh tokens found (API issue or no trades)")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
