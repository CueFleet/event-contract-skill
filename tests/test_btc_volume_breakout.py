import csv
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
import btc_volume_breakout as strategy


def candle(opened, *, high="101", low="99", close="100", volume="10"):
    return {"open_time": str(opened), "high": high, "low": low, "close": close, "volume": volume}


class BtcVolumeBreakoutTest(unittest.TestCase):
    def setUp(self):
        minute = strategy.MINUTE_MS
        self.baseline = [candle(i * minute) for i in range(strategy.LOOKBACK)]

    def prediction(self, latest, period="10m"):
        return strategy.predict({
            "period": period,
            "symbol": "BTCUSDT",
            "market": {"candles": [*self.baseline, latest]},
        })

    def test_breakout_requires_both_price_and_volume(self):
        opened = strategy.LOOKBACK * strategy.MINUTE_MS
        self.assertEqual(self.prediction(candle(opened, high="103", close="102", volume="15")), "LONG")
        self.assertEqual(self.prediction(candle(opened, low="97", close="98", volume="15")), "SHORT")
        self.assertEqual(self.prediction(candle(opened, high="103", close="102", volume="14.9")), "NO_SIGNAL")
        self.assertEqual(self.prediction(candle(opened, high="103", close="101", volume="15")), "NO_SIGNAL")
        self.assertEqual(self.prediction(candle(opened, high="103", close="102", volume="15"), "1h"), "NO_SIGNAL")

    def test_csv_replay_uses_closed_timestamp_and_keeps_prior_signals(self):
        minute = strategy.MINUTE_MS
        last_open = strategy.LOOKBACK * minute
        breakout = candle(last_open, high="103", close="102", volume="15")
        reversal = candle(last_open + minute, low="97", close="98", volume="15")
        with TemporaryDirectory() as temp:
            root = Path(temp)
            data, output = root / "candles.csv", root / "signals.csv"
            self.write_data(data, [*self.baseline, breakout, reversal])
            self.assertEqual(strategy.replay(data, output), 2)
            with output.open(encoding="utf-8", newline="") as stream:
                self.assertEqual(list(csv.DictReader(stream)), [
                    {"signal_time": str(last_open + minute), "direction": "LONG"},
                    {"signal_time": str(last_open + 2 * minute), "direction": "SHORT"},
                ])
            with self.assertRaises(FileExistsError):
                strategy.replay(data, output)

    def test_gap_never_publishes_partial_output(self):
        minute = strategy.MINUTE_MS
        with TemporaryDirectory() as temp:
            root = Path(temp)
            data, output = root / "candles.csv", root / "signals.csv"
            self.write_data(data, [*self.baseline, candle(strategy.WARMUP * minute)])
            with self.assertRaisesRegex(ValueError, "closed-minute sequence"):
                strategy.replay(data, output)
            self.assertFalse(output.exists())

    def write_data(self, path, candles):
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=candles[0].keys())
            writer.writeheader()
            writer.writerows(candles)
