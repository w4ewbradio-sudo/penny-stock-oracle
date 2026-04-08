#!/usr/bin/env python3
import json
import re
from copy import deepcopy
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path("/Users/bot/penny-stock-oracle")
LEDGER_PATH = PROJECT_DIR / "data" / "ledger.json"
PICKS_HISTORY_PATH = PROJECT_DIR / "data" / "picks-history.json"
INDEX_PATH = PROJECT_DIR / "index.html"
SITE_INDEX_PATH = PROJECT_DIR / "site" / "index.html"

CATEGORY_ORDER = [
    ("high_risk", "🔥 High Risk"),
    ("sure_bet", "🛡️ Sure Bet"),
    ("maverick", "🃏 Maverick"),
]
PICK_KEYS = [key for key, _ in CATEGORY_ORDER]
RESULT_CLASS_MAP = {
    "win": "var(--green)",
    "partial": "var(--green)",
    "loss": "var(--red)",
    "stopped": "var(--red)",
    "stopped_out": "var(--red)",
    "pending": "var(--accent-gold)",
    "miss": "var(--text-dim)",
}


def load_json(path: Path):
    return json.loads(path.read_text())


def save_json(path: Path, data):
    path.write_text(json.dumps(data, indent=4) + "\n")


def money(value: float, show_plus: bool = False) -> str:
    if show_plus:
        return f"{value:+.2f}"
    return f"{value:.2f}"


def percent(value: float) -> str:
    return f"{value:+.2f}%"


def short_date(date_str: str) -> str:
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return f"{dt.month}/{dt.day}"


def build_ledger_maps(ledger):
    by_date = {}
    for day in ledger.get("trades", []):
        picks = {}
        for pick in day.get("picks", []):
            category = pick.get("category")
            if category in PICK_KEYS:
                picks[category] = pick
        by_date[day["date"]] = {"day": day, "picks": picks}
    return by_date


def sync_picks_history(picks_history, ledger):
    ledger_by_date = build_ledger_maps(ledger)
    changed = False
    synced_entries = []

    for entry in picks_history.get("picks", []):
        ledger_day = ledger_by_date.get(entry.get("date"))
        updated = deepcopy(entry)

        if ledger_day:
            for category in PICK_KEYS:
                hist_pick = updated.get(category)
                ledger_pick = ledger_day["picks"].get(category)
                if not hist_pick or not ledger_pick:
                    continue

                desired_result = ledger_pick.get("actual_result", hist_pick.get("result", "pending"))
                if hist_pick.get("result") != desired_result:
                    hist_pick["result"] = desired_result
                    changed = True

                for hist_key, ledger_key in (("actual_exit", "actual_exit"), ("profit", "profit"), ("notes", "notes")):
                    desired_value = ledger_pick.get(ledger_key)
                    if desired_value is not None and hist_pick.get(hist_key) != desired_value:
                        hist_pick[hist_key] = desired_value
                        changed = True

            daily_profit = ledger_day["day"].get("daily_total")
            if daily_profit is not None and updated.get("daily_profit") != daily_profit:
                updated["daily_profit"] = daily_profit
                changed = True

            start_balance = updated.get("daily_balance")
            if start_balance is not None and daily_profit is not None:
                end_balance = round(float(start_balance) + float(daily_profit), 2)
                if updated.get("daily_balance_end") != end_balance:
                    updated["daily_balance_end"] = end_balance
                    changed = True

        synced_entries.append(updated)

    if changed:
        picks_history["picks"] = synced_entries
    return changed


def compute_stats(ledger):
    starting = float(ledger.get("starting_balance", 0) or 0)
    current = float(ledger.get("current_balance", 0) or 0)
    wins = int(ledger.get("wins", 0) or 0)
    losses = int(ledger.get("losses", 0) or 0)
    partials = int(ledger.get("partials", 0) or 0)
    triggered = wins + losses + partials
    total_return = ((current - starting) / starting * 100) if starting else 0.0
    win_rate = (wins / triggered * 100) if triggered else 0.0
    trading_days = len({day.get("date") for day in ledger.get("trades", []) if day.get("date")})
    best_day = float((ledger.get("best_day") or {}).get("profit", 0) or 0)
    worst_day = float((ledger.get("worst_day") or {}).get("profit", 0) or 0)
    return {
        "portfolio": current,
        "total_return": total_return,
        "win_rate": win_rate,
        "trading_days": trading_days,
        "best_day": best_day,
        "worst_day": worst_day,
    }


def build_history_rows(ledger, picks_history):
    ledger_by_date = build_ledger_maps(ledger)
    rows = []

    for entry in picks_history.get("picks", []):
        date = entry.get("date")
        if not date:
            continue

        ledger_day = ledger_by_date.get(date)
        cells = []
        for category in PICK_KEYS:
            pick = entry.get(category) or {}
            ticker = pick.get("ticker", "—")
            if ledger_day and category in ledger_day["picks"]:
                result = (ledger_day["picks"][category].get("actual_result") or "pending").lower()
            else:
                result = (pick.get("result") or "pending").lower()
            color = RESULT_CLASS_MAP.get(result, "var(--accent-gold)")
            cells.append(f'<span class="ticker" style="color:{color}">{ticker}</span>')

        if ledger_day:
            daily_total = float(ledger_day["day"].get("daily_total", 0) or 0)
            pnl_color = "var(--green)" if daily_total > 0 else "var(--red)" if daily_total < 0 else "var(--text)"
            pnl_html = f'<span style="color:{pnl_color}">{money(daily_total, show_plus=True)}</span>'
        else:
            pnl_html = '<span style="color:var(--accent-gold)">PRE-MKT</span>'

        rows.append({"date": date, "cells": cells, "pnl_html": pnl_html})

    rows.sort(key=lambda item: item["date"], reverse=True)
    return rows[:7]


def render_history_table(rows):
    html = [
        '<div class="history-row"><span>Date</span><span>🔥 High Risk</span><span>🛡️ Sure Bet</span><span>🃏 Maverick</span><span>Daily P&amp;L</span></div>'
    ]
    for row in rows:
        html.append(
            "<div class=\"history-row\">"
            f"<span>{short_date(row['date'])}</span>"
            f"{''.join(row['cells'])}"
            f"<span>{row['pnl_html']}</span>"
            "</div>"
        )
    return "".join(html)


def replace_stat_block(html, stat_id, value):
    pattern = re.compile(
        rf'(<div class="stat-value[^\"]*" id="{re.escape(stat_id)}">)(.*?)(</div>)',
        re.DOTALL,
    )
    return pattern.sub(lambda m: f"{m.group(1)}{value}{m.group(3)}", html, count=1)


def replace_stat_with_class(html, stat_id, value, klass):
    pattern = re.compile(
        rf'(<div class="stat-value)(?: positive| negative)?(" id="{re.escape(stat_id)}">)(.*?)(</div>)',
        re.DOTALL,
    )
    return pattern.sub(lambda m: f"{m.group(1)} {klass}{m.group(2)}{value}{m.group(4)}", html, count=1)


def replace_history_table(html, history_html):
    pattern = re.compile(r'(<div id="history-table">)(.*?)(</div>\s*</div>)', re.DOTALL)
    return pattern.sub(lambda m: f"{m.group(1)}{history_html}{m.group(3)}", html, count=1)


def rebuild_index(index_html, stats, history_rows):
    updated = index_html
    updated = replace_stat_with_class(
        updated,
        "portfolio-value",
        f'${money(stats["portfolio"])}',
        "positive" if stats["portfolio"] >= 0 else "negative",
    )
    updated = replace_stat_with_class(
        updated,
        "total-return",
        percent(stats["total_return"]),
        "positive" if stats["total_return"] >= 0 else "negative",
    )
    updated = replace_stat_block(updated, "win-rate", f'{stats["win_rate"]:.1f}%')
    updated = replace_stat_block(updated, "trading-days", str(stats["trading_days"]))
    updated = replace_stat_with_class(
        updated,
        "best-day",
        money(stats["best_day"], show_plus=True),
        "positive" if stats["best_day"] >= 0 else "negative",
    )
    updated = replace_stat_with_class(
        updated,
        "worst-day",
        money(stats["worst_day"], show_plus=True),
        "positive" if stats["worst_day"] >= 0 else "negative",
    )
    updated = replace_history_table(updated, render_history_table(history_rows))
    return updated


def main():
    ledger = load_json(LEDGER_PATH)
    picks_history = load_json(PICKS_HISTORY_PATH)
    index_html = INDEX_PATH.read_text()

    if sync_picks_history(picks_history, ledger):
        save_json(PICKS_HISTORY_PATH, picks_history)

    stats = compute_stats(ledger)
    history_rows = build_history_rows(ledger, picks_history)
    updated_html = rebuild_index(index_html, stats, history_rows)

    INDEX_PATH.write_text(updated_html)
    SITE_INDEX_PATH.write_text(updated_html)

    print("Rebuilt index.html and site/index.html")
    print(f"Portfolio: ${money(stats['portfolio'])}")
    print(f"Total return: {percent(stats['total_return'])}")
    print(f"Win rate: {stats['win_rate']:.1f}%")
    print(f"Trading days: {stats['trading_days']}")


if __name__ == "__main__":
    main()
