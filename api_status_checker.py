#!/usr/bin/env python3
"""
API Status Checker for Forex Trader
This script can be used to check the current API limit status of the forex trader
"""

import json
import sys
from pathlib import Path

def load_trader_config():
    """Load the trader configuration"""
    config_file = Path("config/config.json")
    if config_file.exists():
        with open(config_file, 'r') as f:
            return json.load(f)
    return {}

def get_api_status_from_trader():
    """Get API status by importing the trader class"""
    try:
        from forex_trader2 import ForexTrader
        
        # Load config
        config = load_trader_config()
        
        # Create trader instance (without starting the loop)
        trader = ForexTrader(config)
        
        # Get API limit status
        api_status = trader.get_api_limit_status()
        
        return api_status
        
    except Exception as e:
        return {"error": f"Failed to get API status: {e}"}

def display_api_status(status):
    """Display API status in a readable format"""
    if "error" in status:
        print(f"❌ Error: {status['error']}")
        return
    
    print("🔍 Gemini API Status Check")
    print("=" * 50)
    
    print(f"📊 Total API Keys: {status.get('total_keys', 0)}")
    print(f"🚫 Excluded Keys: {status.get('excluded_keys', 0)}")
    print(f"📈 Current Key Index: {status.get('current_key_index', 0)}")
    print(f"📦 Daily Limit Per Key: {status.get('daily_limit_per_key', 0)}")
    print(f"📋 Total Requests Today: {status.get('total_requests_today', 0)}")
    print(f"⚡ Estimated Remaining: {status.get('estimated_remaining_requests', 0)}")
    
    print("\n🔑 Per-Key Usage:")
    requests_today = status.get('requests_today', {})
    if requests_today:
        for key, count in requests_today.items():
            key_display = f"...{key[-4:]}" if len(key) > 4 else key
            print(f"  • Key {key_display}: {count} requests")
    else:
        print("  • No usage data available")
    
    print("\n📡 Latest Limit Information:")
    limit_info = status.get('last_limit_info', {})
    if limit_info:
        for key, info in limit_info.items():
            key_display = f"...{key[-4:]}" if len(key) > 4 else key
            timestamp = info.get('timestamp', 'Unknown')
            status_code = info.get('status_code', 'Unknown')
            limit_details = info.get('limit_info', {})
            
            print(f"  • Key {key_display} (Status: {status_code}, Time: {timestamp}):")
            if limit_details:
                for desc, value in limit_details.items():
                    print(f"    - {desc}: {value}")
            else:
                print("    - No limit details available")
    else:
        print("  • No limit information available yet")

def main():
    """Main function"""
    print("Checking Gemini API Status...")
    
    # Get API status
    status = get_api_status_from_trader()
    
    # Display results
    display_api_status(status)
    
    # Export to JSON if requested
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        output_file = "api_status.json"
        with open(output_file, 'w') as f:
            json.dump(status, f, indent=2)
        print(f"\n💾 Status exported to {output_file}")

if __name__ == "__main__":
    main()