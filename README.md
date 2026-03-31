# 🔮 Penny Stock Oracle — Daily AI-Powered Penny Stock Research & Tracking

An automated daily penny stock research system powered by OpenClaw AI on a Mac mini. The system conducts morning research, generates daily stock picks across three risk categories, publishes them to a web dashboard, and tracks hypothetical performance over time.

---

## ⚠️ IMPORTANT DISCLAIMER

**This is NOT financial advice.** This system is for educational and entertainment purposes only. Penny stocks are extremely high-risk investments. The vast majority of day traders lose money. Never invest money you cannot afford to lose. Always do your own research and consult a licensed financial advisor before making any investment decisions.

---

## 📋 Overview

### What It Does
Each trading day (Mon-Fri), the system:
1. **Researches** penny stocks by scanning Reddit communities, financial news, pre-market data, and stock screeners
2. **Selects 3 picks** across categories:
   - 🔥 **High Risk / High Reward** — volatile momentum plays with explosive potential
   - 🛡️ **Sure Bet** — relatively stable penny stocks with solid fundamentals
   - 🃏 **Maverick** — contrarian or unconventional wild card picks
3. **Sets entry/exit prices** for each pick (day trade targets)
4. **Publishes** a daily dashboard webpage
5. **Tracks performance** — simulates $100 day trades using the previous day's picks and keeps a running tally

### Optimal Schedule (All times Eastern)
| Time | Task |
|------|------|
| 6:00 AM | Scan Reddit (r/pennystocks, r/wallstreetbets, r/smallstreetbets, r/RaceToTenMillion) for overnight sentiment |
| 7:00 AM | Check pre-market movers, news catalysts, volume spikes |
| 8:00 AM | Cross-reference with stock screeners, compile candidate list |
| 8:30 AM | Final analysis, select 3 picks, set entry/exit prices |
| 8:45 AM | Publish daily page to GitHub Pages |
| 5:00 PM | After market close — pull actual closing prices, calculate performance, update tracking ledger |

---

## 🗂️ Project Structure

```
penny-stock-oracle/
├── README.md                    # This file
├── OPENCLAW_INSTRUCTIONS.md     # Detailed instructions for OpenClaw AI agent
├── research-prompt.md           # The research prompt template OpenClaw uses
├── scoring-prompt.md            # The scoring/selection prompt template  
├── performance-prompt.md        # End-of-day performance tracking prompt
├── data/
│   ├── picks-history.json       # All historical picks + results
│   ├── ledger.json              # Running $100 portfolio tracker
│   └── research-sources.json    # Curated list of research sources
├── site/
│   ├── index.html               # Main dashboard (GitHub Pages)
│   ├── archive.html             # Historical picks browser
│   └── style.css                # Shared styles
├── scripts/
│   ├── morning-research.sh      # Cron: triggers OpenClaw morning research
│   ├── evening-update.sh        # Cron: triggers OpenClaw evening performance check
│   ├── publish.sh               # Pushes updated site to GitHub Pages
│   └── setup-cron.sh            # Installs the cron jobs
└── templates/
    └── daily-page-template.html # Template for daily pick pages
```

---

## 🚀 Setup Instructions

### Prerequisites
- Mac mini with OpenClaw installed and running
- GitHub account with a repo for GitHub Pages (e.g., `penny-stock-oracle`)
- Git configured on the Mac mini
- OpenClaw configured with Anthropic API access

### Step 1: Clone & Configure
```bash
# Create project directory
mkdir -p ~/penny-stock-oracle
cd ~/penny-stock-oracle

# Copy all files from this package into ~/penny-stock-oracle/

# Initialize git repo (or clone your existing GitHub Pages repo)
git init
git remote add origin git@github.com:YOUR_USERNAME/penny-stock-oracle.git

# Create data directory
mkdir -p data site/daily
```

### Step 2: Initialize Data Files
```bash
# Create initial ledger
echo '{"starting_balance": 100, "current_balance": 100, "trades": [], "last_updated": ""}' > data/ledger.json

# Create initial picks history
echo '{"picks": []}' > data/picks-history.json
```

### Step 3: Install Cron Jobs
```bash
chmod +x scripts/*.sh
./scripts/setup-cron.sh
```

### Step 4: Configure OpenClaw
Add the project context to OpenClaw's knowledge base or configure it as a subagent task. See `OPENCLAW_INSTRUCTIONS.md` for detailed agent configuration.

---

## 📊 Research Sources (Ranked by Value)

### Tier 1 — Primary Reddit Communities
| Source | URL | Why |
|--------|-----|-----|
| r/pennystocks | reddit.com/r/pennystocks | 2M+ members, dedicated penny stock DD |
| r/wallstreetbets | reddit.com/r/wallstreetbets | Momentum plays, short squeeze targets |
| r/smallstreetbets | reddit.com/r/smallstreetbets | Small account traders, penny focus |
| r/RaceToTenMillion | reddit.com/r/RaceToTenMillion | Aggressive growth strategies |

### Tier 2 — Stock Screeners & Pre-Market Data
| Source | URL | Why |
|--------|-----|-----|
| Finviz Screener | finviz.com/screener.ashx | Free penny stock screener with filters |
| TradingView Pre-Market | tradingview.com/markets/stocks-usa/market-movers-pre-market-most-active/ | Pre-market movers |
| StockAnalysis Pre-Market | stockanalysis.com/markets/premarket/ | Clean pre-market data |
| MarketChameleon | marketchameleon.com/Reports/PremarketTrading | Pre-market activity |
| Benzinga Penny Stocks | benzinga.com/money/best-penny-stocks | Daily updated penny stock charts |

### Tier 3 — Sentiment & Mention Tracking
| Source | URL | Why |
|--------|-----|-----|
| AltIndex Trending | altindex.com/trending-penny-stocks | Real-time Reddit mention tracking |
| Quiver Quant | quiverquant.com | Reddit mention aggregator |

### Tier 4 — Free Stock Data APIs
| API | Free Tier | Best For |
|-----|-----------|----------|
| Alpha Vantage | 25 req/day | Historical + intraday quotes |
| Finnhub | 60 req/min | Real-time quotes, news |
| yfinance (Python) | Unlimited | Historical data, quick lookups |

### Tier 5 — News & Catalysts
| Source | Why |
|--------|-----|
| SEC EDGAR | New filings, insider trading |
| PR Newswire | Corporate announcements |
| GlobeNewsWire | Press releases from small caps |
| Seeking Alpha | Analysis pieces on penny stocks |

---

## 🧠 Stock Selection Criteria

### 🔥 High Risk / High Reward
- Price under $5/share (ideally under $2)
- Float under 50M shares
- Pre-market volume spike (3x+ average)
- Breaking news catalyst (FDA, earnings, contract)
- High Reddit mention velocity (trending in last 24h)
- Target: 10-30% gain potential

### 🛡️ Sure Bet
- Price under $5/share
- Listed on NASDAQ or NYSE (not OTC)
- Positive revenue trend or profitability
- Institutional ownership > 10%
- Lower volatility (beta < 2 if possible)
- Target: 3-8% gain potential

### 🃏 Maverick
- Contrarian play — stock everyone is bearish on
- OR unusual sector (space, quantum, psychedelics, etc.)
- OR recovery play after recent significant drop
- OR tiny company with outsized catalyst
- The "fun" pick — could go either way dramatically
- Target: unpredictable, but reasoning must be solid

---

## 📈 Performance Tracking Logic

Each day after market close:
1. Pull the actual high/low/close for each pick
2. Determine if the entry price was hit during the trading day
3. If entry was hit, check if exit target was hit
4. Calculate result:
   - **Win**: Entry hit, exit hit → profit = (exit - entry) / entry × $100
   - **Partial**: Entry hit, exit not hit → use closing price as exit
   - **Miss**: Entry never hit → $0 gain/loss
5. Update the ledger with the net result across all 3 picks
6. Running balance tracks what $100 would be worth if you followed every trade

---

## 🌐 Dashboard Features

The published web page shows:
- Today's 3 picks with entry/exit prices and reasoning
- Live-ish status (pre-market / market open / closed)
- Running portfolio balance chart
- Win/loss record and hit rate
- Last 7 days of picks with results
- Link to full archive

---

## License

MIT — Use at your own risk. This is not financial advice.
