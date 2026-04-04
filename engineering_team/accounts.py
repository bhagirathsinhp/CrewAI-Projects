
from datetime import datetime


def get_share_price(symbol: str) -> float:
    prices = {
        "AAPL": 189.30,
        "TSLA": 177.50,
        "GOOGL": 140.25,
    }
    symbol = symbol.upper()
    if symbol not in prices:
        raise ValueError(f"Unknown symbol: '{symbol}'. Available symbols: {list(prices.keys())}")
    return prices[symbol]


class Account:
    def __init__(self, user_id: str, initial_deposit: float) -> None:
        if not user_id or not isinstance(user_id, str):
            raise ValueError("user_id must be a non-empty string.")
        if not isinstance(initial_deposit, (int, float)) or initial_deposit < 0:
            raise ValueError("initial_deposit must be a non-negative number.")
        self.user_id: str = user_id
        self.cash_balance: float = float(initial_deposit)
        self.initial_deposit: float = float(initial_deposit)
        self.holdings: dict = {}
        self.transactions: list = []
        self._record_transaction(action="DEPOSIT", symbol=None, quantity=None, price=None, amount=float(initial_deposit))

    def _record_transaction(self, action, symbol, quantity, price, amount):
        transaction = {
            "action": action, "symbol": symbol, "quantity": quantity,
            "price": price, "amount": amount, "timestamp": datetime.now().isoformat(),
        }
        self.transactions.append(transaction)

    def deposit(self, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            return False
        self.cash_balance += float(amount)
        self._record_transaction(action="DEPOSIT", symbol=None, quantity=None, price=None, amount=float(amount))
        return True

    def withdraw(self, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            return False
        if amount > self.cash_balance:
            return False
        self.cash_balance -= float(amount)
        self._record_transaction(action="WITHDRAWAL", symbol=None, quantity=None, price=None, amount=float(amount))
        return True

    def buy_shares(self, symbol, quantity):
        if not isinstance(quantity, int) or quantity <= 0:
            return False
        symbol = symbol.upper()
        try:
            price = get_share_price(symbol)
        except ValueError:
            return False
        total_cost = price * quantity
        if total_cost > self.cash_balance:
            return False
        self.cash_balance -= total_cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        self._record_transaction(action="BUY", symbol=symbol, quantity=quantity, price=price, amount=total_cost)
        return True

    def sell_shares(self, symbol, quantity):
        if not isinstance(quantity, int) or quantity <= 0:
            return False
        symbol = symbol.upper()
        try:
            price = get_share_price(symbol)
        except ValueError:
            return False
        current_holding = self.holdings.get(symbol, 0)
        if quantity > current_holding:
            return False
        proceeds = price * quantity
        self.cash_balance += proceeds
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        self._record_transaction(action="SELL", symbol=symbol, quantity=quantity, price=price, amount=proceeds)
        return True

    def get_portfolio_value(self):
        shares_value = 0.0
        for symbol, quantity in self.holdings.items():
            try:
                price = get_share_price(symbol)
                shares_value += price * quantity
            except ValueError:
                pass
        return round(self.cash_balance + shares_value, 2)

    def get_profit_or_loss(self):
        return round(self.get_portfolio_value() - self.initial_deposit, 2)

    def get_holdings(self):
        return dict(self.holdings)

    def get_transactions(self):
        return list(self.transactions)
