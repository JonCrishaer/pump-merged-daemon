#!/usr/bin/env python3
"""
Birdeye API Scanner for pump.fun Fresh Tokens
Real-time Solana token data - PRODUCTION READY
"""

import requests
import json
import time
from datetime import datetime, timedelta

BIRDEYE_API = "https://public-api.birdeye.so"
BIRDEYE_KEY = "4abf00a4b5e647a39cbd1f52f9734a6b"

def get_fresh_tokens(limit=50):
    """Get fresh pump.fun tokens via Birdeye"""
    
    print(f"🔍 Querying Birdeye for fresh tokens...")
    
    try:
        # Get latest Solana tokens sorted by creation time
        headers = {
            "X-API-KEY": BIRDEYE_KEY,
            "User-Agent": "Mozilla/5.0"
        }
        
        response = requests.get(
            f"{BIRDEYE_API}/defi/token_list?sort_by=created_at&sort_type=desc&limit={limit}",
            headers=headers,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success") and "data" in data:
                tokens_data = data.get("data", {})
                
                if "tokens" in tokens_data:
                    return parse_fresh_tokens(tokens_data["tokens"])
                elif isinstance(tokens_data, list):
                    return parse_fresh_tokens(tokens_data)
            
            return []
        else:
            print(f"⚠️  Birdeye error: {response.status_code}")
            if response.text:
                print(f"    {response.text[:100]}")
            return []
    
    except Exception as e:
        print(f"❌ Error querying Birdeye: {str(e)[:100]}")
        return []

def parse_fresh_tokens(tokens):
    """Parse and filter fresh tokens"""
    fresh = []
    now = datetime.utcnow()
    
    for token in tokens[:100]:
        try:
            # Extract token data
            mint = token.get("mint") or token.get("address")
            if not mint:
                continue
            
            # Skip SOL
            if mint == "So11111111111111111111111111111111111111112":
                continue
            
            symbol = token.get("symbol") or "?"
            name = token.get("name") or symbol
            
            # Get creation time
            created_at = token.get("createdAt")
            if not created_at:
                continue
            
            if isinstance(created_at, (int, float)):
                token_time = datetime.fromtimestamp(created_at / 1000 if created_at > 10**10 else created_at)
            else:
                token_time = datetime.fromisoformat(str(created_at).replace('Z', '+00:00').split('+')[0])
            
            age_minutes = (now - token_time).total_seconds() / 60
            
            # Get metrics
            price = float(token.get("price") or token.get("lastPrice") or 0)
            market_cap = float(token.get("mc") or token.get("marketCap") or 0)
            volume_24h = float(token.get("v24hUSD") or token.get("volume24h") or 0)
            holder_count = int(token.get("holder") or token.get("holderCount") or 0)
            
            # Skip if no useful data
            if price == 0 and market_cap == 0:
                continue
            
            fresh.append({
                "mint": mint,
                "symbol": symbol,
                "name": name,
                "age_minutes": age_minutes,
                "price": price,
                "market_cap": market_cap,
                "volume_24h": volume_24h,
                "holder_count": holder_count,
                "created_at": str(token_time),
                "is_bonding_curve": market_cap < 1000000,
                "bonding_progress_pct": min((market_cap / 1000000) * 100, 100) if market_cap > 0 else 0,
            })
        
        except Exception as e:
            continue
    
    return fresh

def calculate_fresh_score(token):
    """Score token for trading (0-100)"""
    score = 0
    
    # Age (30 pts) - sweet spot: 1-6 hours
    age = token['age_minutes']
    if 60 <= age <= 360:
        score += 28
    elif 30 <= age <= 720:
        score += 18
    
    # Bonding curve progress (25 pts) - 10-80% is best
    progress = token['bonding_progress_pct']
    if 20 <= progress <= 80:
        score += 23
    elif 10 <= progress <= 90:
        score += 14
    
    # Volume (25 pts) - high volume = demand
    vol = token['volume_24h']
    if vol > 50000:
        score += 25
    elif vol > 10000:
        score += 18
    elif vol > 1000:
        score += 12
    elif vol > 100:
        score += 6
    
    # Holder count (20 pts) - proven community
    holders = token['holder_count']
    if holders > 200:
        score += 18
    elif holders > 100:
        score += 14
    elif holders > 50:
        score += 8
    
    return min(score, 100)

def main():
    """LIVE scan"""
    print("\n🚀 Birdeye LIVE Scanner - pump.fun Fresh Tokens")
    print("=" * 80)
    print()
    
    tokens = get_fresh_tokens(limit=50)
    
    if not tokens:
        print("⚠️  No fresh tokens found")
        return
    
    print(f"✅ Found {len(tokens)} fresh tokens\n")
    
    # Score and rank
    scored = []
    for token in tokens:
        token['score'] = calculate_fresh_score(token)
        scored.append(token)
    
    scored = sorted(scored, key=lambda x: x['score'], reverse=True)
    
    print(f"{'#':<3} {'Symbol':<10} {'Age (m)':<8} {'Cap':<15} {'Vol 24h':<15} {'Holders':<8} {'Score':<7} {'Status':<15}")
    print("-" * 80)
    
    for i, token in enumerate(scored[:20], 1):
        status = "🚀 BONDING" if token['is_bonding_curve'] else "📈 GRADUATED"
        cap_str = f"${token['market_cap']:,.0f}"
        vol_str = f"${token['volume_24h']:,.0f}"
        
        print(f"{i:<3} {token['symbol']:<10} {token['age_minutes']:<7.0f} {cap_str:<15} {vol_str:<15} {token['holder_count']:<8} {token['score']:<7.0f} {status:<15}")
    
    print()
    if scored:
        print("📊 TOP 3 OPPORTUNITIES:")
        for i, token in enumerate(scored[:3], 1):
            print(f"  [{i}] {token['symbol']} (Score: {token['score']:.0f}/100)")
            print(f"      Mint: {token['mint']}")
            print(f"      Age: {token['age_minutes']:.1f}m | Cap: ${token['market_cap']:,.0f} | Holders: {token['holder_count']}")
            print()
    
    print("=" * 80)
    return scored

if __name__ == "__main__":
    main()
