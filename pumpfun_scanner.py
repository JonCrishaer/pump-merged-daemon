#!/usr/bin/env python3
"""
pump.fun Direct API Scanner
Fresh tokens on bonding curve - LIVE DATA
No dependencies, no auth required
"""

import requests
import json
import time
from datetime import datetime, timedelta

PUMPFUN_API = "https://frontend-api.pump.fun"
HELIUS_RPC = "https://mainnet.helius-rpc.com/?api-key=1c6964fe-c76f-4769-93f3-0cee0b4d14a6"

def get_fresh_tokens(min_age_minutes=30, max_age_hours=24, min_holders=50):
    """Get fresh tokens currently on pump.fun bonding curve"""
    
    print(f"🔍 Querying pump.fun API...")
    
    try:
        # pump.fun bonding curve tokens
        response = requests.get(
            f"{PUMPFUN_API}/tokens?sort=created&limit=100&offset=0",
            timeout=15
        )
        
        if response.status_code == 200:
            tokens = response.json()
            
            if isinstance(tokens, list):
                return parse_fresh_tokens(tokens, min_age_minutes, max_age_hours, min_holders)
            elif isinstance(tokens, dict) and "tokens" in tokens:
                return parse_fresh_tokens(tokens["tokens"], min_age_minutes, max_age_hours, min_holders)
    
    except Exception as e:
        print(f"⚠️  API Error: {str(e)[:100]}")
    
    return []

def parse_fresh_tokens(tokens, min_age_minutes, max_age_hours, min_holders):
    """Filter and parse token list"""
    fresh = []
    
    now = datetime.utcnow()
    
    for token in tokens[:100]:
        try:
            # Get token age
            created_at = token.get("createdAt") or token.get("created_timestamp")
            
            if not created_at:
                continue
            
            if isinstance(created_at, str):
                token_time = datetime.fromisoformat(created_at.replace('Z', '+00:00')).replace(tzinfo=None)
            else:
                token_time = datetime.fromtimestamp(created_at)
            
            age_minutes = (now - token_time).total_seconds() / 60
            
            # Filter by age
            if age_minutes < min_age_minutes or age_minutes > (max_age_hours * 60):
                continue
            
            # Get token data
            mint = token.get("mint") or token.get("address")
            symbol = token.get("symbol") or "?"
            name = token.get("name") or symbol
            
            if not mint or mint == "So11111111111111111111111111111111111111112":  # Skip SOL
                continue
            
            # Market cap & price
            market_cap = float(token.get("usd_market_cap") or token.get("market_cap") or 0)
            price = float(token.get("price") or 0)
            volume_24h = float(token.get("volume_24h") or 0)
            
            # Skip if no data
            if market_cap == 0 and price == 0:
                continue
            
            # Holders (estimate from volume)
            holder_count = token.get("holder_count") or estimate_holders(volume_24h)
            
            if holder_count < min_holders:
                continue
            
            fresh.append({
                "mint": mint,
                "symbol": symbol,
                "name": name,
                "age_minutes": age_minutes,
                "market_cap": market_cap,
                "price": price,
                "volume_24h": volume_24h,
                "holder_count": holder_count,
                "created_at": str(token_time),
                "is_bonding_curve": market_cap < 1000000,  # Bonding curve < $1M
                "bonding_progress_pct": min((market_cap / 1000000) * 100, 100),
            })
        
        except Exception as e:
            continue
    
    return sorted(fresh, key=lambda x: x['age_minutes'])

def estimate_holders(volume_24h):
    """Rough estimate of holders from volume"""
    if volume_24h < 100:
        return 10
    elif volume_24h < 1000:
        return 25
    elif volume_24h < 10000:
        return 100
    else:
        return max(150, int(volume_24h / 100))

def calculate_token_score(token):
    """Score token for trading (0-100)"""
    score = 0
    
    # Age (30 pts) - prefer 1-6 hour window
    age = token['age_minutes']
    if 60 <= age <= 360:
        score += 25
    elif 30 <= age <= 720:
        score += 15
    else:
        score += 0
    
    # Bonding curve progress (25 pts) - prefer 10-80% progress
    progress = token['bonding_progress_pct']
    if 20 <= progress <= 80:
        score += 20
    elif 10 <= progress <= 90:
        score += 12
    else:
        score += 0
    
    # Volume (25 pts) - demand signal
    vol = token['volume_24h']
    if vol > 50000:
        score += 25
    elif vol > 10000:
        score += 18
    elif vol > 1000:
        score += 12
    elif vol > 100:
        score += 6
    
    # Holder count (20 pts) - community strength
    holders = token['holder_count']
    if holders > 200:
        score += 18
    elif holders > 100:
        score += 14
    elif holders > 50:
        score += 8
    
    return min(score, 100)

def main():
    """Live scan test"""
    print("\n🚀 pump.fun LIVE Scanner")
    print("=" * 70)
    print()
    
    print("🔍 Scanning fresh tokens on bonding curve...")
    tokens = get_fresh_tokens(min_age_minutes=30, max_age_hours=24, min_holders=50)
    
    if tokens:
        print(f"✅ Found {len(tokens)} fresh tokens:\n")
        
        # Score and sort
        scored = []
        for token in tokens:
            token['score'] = calculate_token_score(token)
            scored.append(token)
        
        scored = sorted(scored, key=lambda x: x['score'], reverse=True)
        
        print(f"{'#':<3} {'Symbol':<10} {'Age':<8} {'Cap':<12} {'Vol 24h':<12} {'Holders':<8} {'Score':<7} {'Status':<15}")
        print("-" * 70)
        
        for i, token in enumerate(scored[:15], 1):
            status = "🚀 BONDING" if token['is_bonding_curve'] else "📈 GRADUATED"
            cap_str = f"${token['market_cap']:,.0f}"
            
            print(f"{i:<3} {token['symbol']:<10} {token['age_minutes']:<7.0f}m ${cap_str:<11} ${token['volume_24h']:,.0f}".ljust(40) + f"{token['holder_count']:<8} {token['score']:<7.0f} {status:<15}")
        
        print("\n📊 TOP OPPORTUNITY:")
        top = scored[0]
        print(f"   Symbol: {top['symbol']}")
        print(f"   Market Cap: ${top['market_cap']:,.0f}")
        print(f"   Age: {top['age_minutes']:.1f} minutes")
        print(f"   Score: {top['score']:.0f}/100")
        print(f"   Status: {'BONDING CURVE (early entry)' if top['is_bonding_curve'] else 'JUST GRADUATED'}")
        print(f"   Holders: {top['holder_count']}")
        print()
    else:
        print("⚠️  No fresh tokens found")
    
    print("=" * 70)
    print()

if __name__ == "__main__":
    main()
