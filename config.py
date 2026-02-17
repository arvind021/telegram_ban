#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TELEGRAM BAN BOT CONFIG
Edit these values before running!
"""

# ===== API CREDENTIALS (my.telegram.org) =====
API_ACCOUNTS = [
    {
        "phone": "+911234567890",  # Virtual SMS number
        "api_id": 12345678,        # Your API ID
        "api_hash": "your_api_hash_here"
    },
    {
        "phone": "+919876543210",
        "api_id": 87654321,
        "api_hash": "your_api_hash_here"
    }
    # Add 20-50 accounts here
]

# ===== TARGET =====
TARGET_CHAT = "@target_group"  # or -1001234567890 (supergroup ID)

# ===== PROXIES (optional) =====
PROXIES = [
    # Format: socks5://user:pass@ip:port
    # "socks5://127.0.0.1:9050",
]

# ===== SPAM MESSAGES =====
SPAM_MESSAGES = [
    "🔥 FREE 1000$ USDT AIRDROP! t.me/+abc123def456",
    "💎 NFT FREE MINT! Limited 100 spots: t.me/nftdrop",
    "🚀 VIP HACK SERVICE! DM for rates 🔥",
    "💰 CRYPTO PUMP $SHIB +1000%! Buy NOW!",
    "🎁 iPhone 15 Pro Giveaway! Join fast!",
    "⚡ Premium Accounts FREE! t.me/premiumhack",
    "🤑 Passive 500$/day! Real proof DM me",
    "📈 Forex Signals VIP! 90% win rate!",
    "🎰 Casino Bonus 500%! No deposit needed",
    "💋 OnlyFans Leaks FREE! DM now"
]

# ===== ATTACK SETTINGS =====
SPAM_PER_ACCOUNT = 12
JOIN_LEAVE_CYCLES = 3
ATTACK_DELAY = (3, 8)  # Random delay range
