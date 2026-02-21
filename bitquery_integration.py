#!/usr/bin/env python3
"""
Bitquery Integration for pump.fun Real-Time Data
Queries fresh tokens on bonding curve
"""

import requests
import json
from datetime import datetime, timedelta

BITQUERY_API = "https://streaming.bitquery.io/graphql"
BITQUERY_KEY = "ory_at_OXBAjQIM09VDoKdcKK826AxxnpeHO1DSFQluKTUqTUY.bQ9HfWcb6LB2z9TuDjvJgjqKwXdQoSnc61egX_go9Tc"

PUMP_PROGRAM_ID = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"

def get_fresh_pumpfun_tokens(min_age_minutes=30, max_age_hours=24, limit=50):
    """Get fresh tokens currently on pump.fun bonding curve"""
    
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
            Seller
          }
          Block {
            Time
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
            return parse_tokens(data)
        else:
            print(f"⚠️ Bitquery error: {response.status_code}")
            return []
    
    except Exception as e:
        print(f"❌ Error querying Bitquery: {str(e)[:100]}")
        return []

def get_token_metrics(mint_address):
    """Get real-time metrics for a token"""
    
    query = f"""
    query {{
      Solana {{
        Transfers(
          where: {{
            Mint: {{ Address: {{ is: "{mint_address}" }} }}
          }}
          orderBy: {{ descending: Block_Time }}
          limit: {{ count: 100 }}
        ) {{
          Block {{
            Time
          }}
          Transfer {{
            Amount
            Sender
            Receiver
          }}
          Transaction {{
            Fee
          }}
        }}
      }}
    }}
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
            return analyze_metrics(data, mint_address)
        else:
            return None
    
    except Exception as e:
        print(f"⚠️ Error fetching metrics: {str(e)[:80]}")
        return None

def parse_tokens(data):
    """Parse Bitquery response into token list"""
    tokens = []
    
    try:
        instructions = data.get("data", {}).get("Solana", {}).get("Instructions", [])
        
        for instr in instructions:
            token = {
                "mint": instr.get("Instruction", {}).get("Parsed", {}).get("Account", {}).get("Address"),
                "name": instr.get("Instruction", {}).get("Parsed", {}).get("Account", {}).get("Name", "?"),
                "created_at": instr.get("Block", {}).get("Time"),
                "age_minutes": calculate_age(instr.get("Block", {}).get("Time")),
                "tx_signature": instr.get("Transaction", {}).get("Signature"),
            }
            
            if token["mint"]:
                tokens.append(token)
    
    except Exception as e:
        print(f"⚠️ Error parsing tokens: {str(e)[:80]}")
    
    return tokens

def calculate_age(timestamp_str):
    """Calculate token age in minutes"""
    try:
        if not timestamp_str:
            return 0
        
        token_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        age = (datetime.now(token_time.tzinfo) - token_time).total_seconds() / 60
        return max(age, 0)
    except:
        return 0

def analyze_metrics(data, mint_address):
    """Analyze token metrics from transfer data"""
    
    metrics = {
        "mint": mint_address,
        "volume_sol": 0,
        "holder_count": 0,
        "buy_count": 0,
        "sell_count": 0,
        "unique_traders": set(),
    }
    
    try:
        transfers = data.get("data", {}).get("Solana", {}).get("Transfers", [])
        
        for transfer in transfers:
            # Count volume
            amount = transfer.get("Transfer", {}).get("Amount", 0)
            metrics["volume_sol"] += float(amount) if amount else 0
            
            # Track traders
            sender = transfer.get("Transfer", {}).get("Sender")
            receiver = transfer.get("Transfer", {}).get("Receiver")
            
            if sender:
                metrics["unique_traders"].add(sender)
                metrics["buy_count"] += 1
            
            if receiver:
                metrics["unique_traders"].add(receiver)
                metrics["sell_count"] += 1
        
        metrics["holder_count"] = len(metrics["unique_traders"])
        metrics["unique_traders"] = None  # Don't return the set
        
        return metrics
    
    except Exception as e:
        print(f"⚠️ Error analyzing metrics: {str(e)[:80]}")
        return metrics

def main():
    """Test Bitquery integration"""
    print("\n🚀 Bitquery Integration Test")
    print("=" * 50)
    print()
    
    print("🔍 Fetching fresh pump.fun tokens...")
    tokens = get_fresh_pumpfun_tokens(limit=10)
    
    if tokens:
        print(f"✅ Found {len(tokens)} fresh tokens:\n")
        
        for token in tokens[:5]:
            print(f"  {token['name']}")
            print(f"     Mint: {token['mint'][:8]}...")
            print(f"     Age: {token['age_minutes']:.1f} min")
            print()
            
            # Get metrics for first token
            if token['mint']:
                print(f"  📊 Fetching metrics for {token['name']}...")
                metrics = get_token_metrics(token['mint'])
                
                if metrics:
                    print(f"     Volume: {metrics['volume_sol']:.2f} SOL")
                    print(f"     Holders: {metrics['holder_count']}")
                    print(f"     Buys: {metrics['buy_count']} | Sells: {metrics['sell_count']}")
                    print()
    else:
        print("⚠️ No fresh tokens found")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
