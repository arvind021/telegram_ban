# 1. Clone/Folder banao
mkdir telegram_ban_bot && cd telegram_ban_bot

# 2. Files copy karo (upar diye gaye sab)

# 3. API credentials lo
# https://my.telegram.org → API development tools

# 4. Virtual numbers kharido
# SMS-Activate.org (₹5-10 per number)

# 5. config.py edit karo
nano config.py  # phones + API_ID daalo

# 6. Run!
chmod +x run.sh
./run.sh
# 7. 10 accounts  → 1-24hr temp ban
# 8. 25 accounts  → 3-7 days ban
# 9. 50+ accounts → Permanent ban
# 10. Stealth mode → Max evasion
# 1. Play Store → Termux install
# 2. Termux open → Ye commands:
termux-setup-storage
pkg update -y
pkg install python git -y
pip install telethon PySocks faker aiohttp

# 3. Folder banao
mkdir banbot && cd banbot

# 4. Files banao
nano config.py    # Code paste → Ctrl+X → Y → Enter
nano main.py      # Code paste → Ctrl+X → Y → Enter
nano requirements.txt

# 5. Edit config
nano config.py  # Phone + API_ID daalo

# 6. Run! 🔥
python main.py
