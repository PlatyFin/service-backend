# #### imports ####
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
from datetime import date, timedelta
import logging
import os
import json

# #### class definition ####
class DarkFlow():
    def __init__(self):
        try:
            # Initialize Alpaca API
            self.alpaca_api = tradeapi.REST(os.environ.get('ALPACA_API_KEY'), os.environ.get('ALPACA_SECRET_KEY'), base_url='https://paper-api.alpaca.markets', api_version='v2')
            
            # Configure logging
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
            
            # Momentum threshold
            self.MOMENTUM_THRESHOLD = 0.02  # 2%

            # Predefined list of S&P 500 symbols (partial list; add all S&P 500 tickers here)
            self.SP500_SYMBOLS = [
                'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'NVDA', 'TSLA', 'BRK.B', 'UNH', 'JNJ',
                'XOM', 'JPM', 'V', 'PG', 'MA', 'HD', 'INTC', 'CSCO', 'AMD', 'PYPL', 'CRM',
                'GOOG', 'ORCL', 'IBM', 'NVDA', 'TWTR', 'SNAP', 'INTU', 'ADBE', 'VZ',
                'NFLX', 'MSFT', 'GOOG', 'FB', 'AMZN', 'NVDA', 'TSLA', 'GOOG', 'AAPL',
                'PYPL', 'UBER', 'SHOP', 'ROKU', 'SPOT', 'Z', 'DDOG', 'ALGN', 'STNE', 'COIN',
                'LULU', 'T', 'ETSY', 'TWLO', 'SQ', 'MTCH', 'MELI', 'DOCU', 'NOW', 'TEAM',
                'MANH', 'OKTA', 'NET', 'ZS', 'SE', 'SNPS', 'ATVI', 'BIDU', 'VRSN', 'NVDA',
                'RBLX', 'SQ', 'EXPE', 'CHKP', 'SQ', 'V', 'CHWY', 'ROST', 'TGT', 'LOW',
                'WMT', 'AMAT', 'ASML', 'LRCX', 'TSM', 'TXN', 'QCOM', 'ADI', 'AVGO', 'SWKS',
                'KLAC', 'MU', 'Xilinx', 'ON', 'STX', 'WDAY', 'ORLY', 'AON', 'ALL', 'AXP',
                'SPLK', 'CDW', 'MCO', 'SPGI', 'EQIX', 'REGN', 'ISRG', 'LMT', 'RTX', 'BA',
                'BABA', 'BNTX', 'MRNA', 'VRTX', 'IDXX', 'AMGN', 'ESRX', 'CNC', 'CI'
            ]
        except Exception as e:
            print(f"Error during initialization: {e}")

    # Fetch only S&P 500 stocks listed in the U.S. from Alpaca's active assets
    def get_sp500_stocks(self):
        try:
            assets = self.alpaca_api.list_assets(status='active')
            # Filter the active S&P 500 stocks
            sp500_stocks = [asset.symbol for asset in assets if asset.symbol in self.SP500_SYMBOLS]
            logging.info(f"Found {len(sp500_stocks)} active S&P 500 stocks.")
            return sp500_stocks
        except Exception as e:
            logging.error(f"Error fetching S&P 500 assets: {e}")
            return []

    # Calculate weekly momentum for a stock
    def calculate_momentum(self, symbol):
        try:
            end_date = date.today() - timedelta(days=1)
            start_date = end_date - timedelta(days=5)

            bars = self.alpaca_api.get_bars(
                symbol, TimeFrame.Day,
                start=start_date.strftime('%Y-%m-%d'),
                end=end_date.strftime('%Y-%m-%d')
            ).df

            if bars.empty or len(bars) < 2:
                logging.warning(f"Insufficient data for {symbol}.")
                return None

            momentum = (bars['close'].iloc[-1] - bars['close'].iloc[0]) / bars['close'].iloc[0]
            return momentum if momentum >= self.MOMENTUM_THRESHOLD else None

        except Exception as e:
            logging.error(f"Error calculating momentum for {symbol}: {e}")
            return None

    # Monitor S&P 500 stocks and return JSON
    def monitor_sp500_stocks(self):
        sp500_stocks = self.get_sp500_stocks()
        if not sp500_stocks:
            return json.dumps({"error": "No S&P 500 stocks found."})

        response = []

        for symbol in sp500_stocks:
            momentum = self.calculate_momentum(symbol)
            if momentum is not None:
                response.append({
                    "symbol": f"{symbol}",
                    "momentum": f"{momentum:.2%}"
                })
        return response

