from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class FinancialData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    open_price = db.Column(db.DECIMAL(20, 4), nullable=False)
    close_price = db.Column(db.DECIMAL(20, 4), nullable=False)
    volume = db.Column(db.Integer, nullable=False)

    def get_json(self):
        return {
            'symbol': self.symbol,
            'date': self.date.strftime('%Y-%m-%d'),
            'open_price': str(self.open_price),
            'close_price': str(self.close_price),
            'volume': self.volume,
        }

    def __repr__(self):
        return f"<FinancialData({self.get_json()})>"
