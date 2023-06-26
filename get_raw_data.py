import json
import logging
import os
from datetime import datetime, timedelta

import requests
from financial.config import app
from model import FinancialData, db

DAYS = 14
BASE_URL = 'https://www.alphavantage.co/query'
API_KEY = os.environ["API_KEY"]


logger = logging.getLogger(__name__)


def get_data_from_api(symbol):
    params = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'symbol': symbol,
        'apikey': API_KEY,
    }
    result = requests.get(BASE_URL, params)
    if result.status_code != requests.codes.ok:
        logger.error(
            f'get data fail! symbol={symbol}, status_code={result.status_code}')
        return {}
    logger.info(f'get data succ, symbol={symbol}, data_size={len(result.content)}')
    return json.loads(result.content)


def parse_data(symbol, content):
    now = datetime.now().date()
    model_list = []
    try:
        daily_data = content.get('Time Series (Daily)')
        for i in range(DAYS):
            _time = now - timedelta(days=i)
            date_str = _time.strftime('%Y-%m-%d')
            cur_data = daily_data.get(date_str)
            if not cur_data:
                continue
            cur_model = FinancialData(
                symbol=symbol,
                date=date_str,
                open_price=float(cur_data['1. open']),
                close_price=float(cur_data['4. close']),
                volume=int(cur_data['6. volume'])
            )

            model_list.append(cur_model)
        return model_list
    except Exception as e:
        logger.error(f'parse data fail! symbol={symbol}, content={content}', e)
        return {}


def upsert_to_db(model_list):
    for model in model_list:
        exist_model = FinancialData.query\
            .filter_by(symbol=model.symbol, date=model.date).first()
        if exist_model:
            exist_model.open_price = model.open_price
            exist_model.close_price = model.close_price
            exist_model.volume = model.volume
        else:
            db.session.add(model)
        db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        symbol_list = ['IBM', 'AAPL']
        for symbol in symbol_list:
            content = get_data_from_api(symbol)
            model_list = parse_data(symbol, content)
            upsert_to_db(model_list)
            logger.info(f'get data symbol={symbol}, size={len(model_list)}')
        logger.info('get data complete!')
