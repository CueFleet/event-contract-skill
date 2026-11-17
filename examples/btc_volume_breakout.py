"""BTC event-contract example with one strategy for replay and signal service."""

import argparse
from collections import deque
import csv
from decimal import Decimal
from pathlib import Path
from shutil import copyfileobj
from statistics import median
from tempfile import TemporaryDirectory


MINUTE_MS = 60_000
LOOKBACK = 30
WARMUP = LOOKBACK + 1
VOLUME_MULTIPLE = Decimal("1.5")


def predict(request):
    """Check the latest closed minute for a volume-confirmed range break."""
    if request["symbol"] != "BTCUSDT" or request["period"] != "10m":
        return "NO_SIGNAL"
    candles = request["market"]["candles"]
    if len(candles) < WARMUP:
        return "NO_SIGNAL"

    previous = candles[-WARMUP:-1]
    latest = candles[-1]
    typical_volume = median(Decimal(bar["volume"]) for bar in previous)
    if typical_volume <= 0 or Decimal(latest["volume"]) < typical_volume * VOLUME_MULTIPLE:
        return "NO_SIGNAL"

    close = Decimal(latest["close"])
    if close > max(Decimal(bar["high"]) for bar in previous):
        return "LONG"
    if close < min(Decimal(bar["low"]) for bar in previous):
        return "SHORT"
    return "NO_SIGNAL"


def replay(candles_path, signals_path):
    columns = {"open_time", "high", "low", "close", "volume"}
    window = deque(maxlen=WARMUP)
    previous_open = None
    count = 0
    signals_path.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=signals_path.parent) as temporary:
        pending = Path(temporary) / "signals.csv"
        with candles_path.open(encoding="utf-8-sig", newline="") as source, pending.open(
            "w", encoding="utf-8", newline=""
        ) as destination:
            reader = csv.DictReader(source)
            if not columns.issubset(reader.fieldnames or []):
                raise ValueError("Input CSV requires open_time, high, low, close, volume")
            writer = csv.writer(destination)
            writer.writerow(("signal_time", "direction"))
            for candle in reader:
                opened = int(candle["open_time"])
                if opened < 0 or opened % MINUTE_MS or (
                    previous_open is not None and opened != previous_open + MINUTE_MS
                ):
                    raise ValueError(f"Input row {reader.line_num} breaks the closed-minute sequence")
                previous_open = opened
                window.append(candle)
                direction = predict({
                    "symbol": "BTCUSDT",
                    "period": "10m",
                    "market": {"candles": list(window)},
                })
                if direction != "NO_SIGNAL":
                    writer.writerow((opened + MINUTE_MS, direction))
                    count += 1
        with pending.open("rb") as source, signals_path.open("xb") as destination:
            copyfileobj(source, destination)
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candles", type=Path, required=True, help="UTC Binance BTCUSDT minute CSV")
    parser.add_argument("--signals", type=Path, required=True, help="new signal CSV path")
    args = parser.parse_args()
    print(f"{replay(args.candles, args.signals)} signals written to {args.signals}")


if __name__ == "__main__":
    main()
