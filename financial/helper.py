import math
import time

from model import FinancialData, db

valid_date_format = "%Y-%m-%d"


def query(args):
    try:
        start_date = time.strptime(args.get('start_date'), valid_date_format)
        end_date = time.strptime(args.get('end_date'), valid_date_format)
        symbol = args.get('symbol')
        limit = int(args.get('limit', 5))
        page = int(args.get('page', 1))
    except Exception as e:
        raise Exception(f'please check params, params={args}, error={str(e)}')
    filters = []
    if start_date:
        filters.append(FinancialData.date >= start_date)
    if end_date:
        filters.append(FinancialData.date <= end_date)
    if symbol:
        filters.append(FinancialData.symbol == symbol)
    query = FinancialData.query.filter(*filters).order_by(FinancialData.date)
    total_count = query.count()
    db_result = query.paginate(page=page, per_page=limit)
    data = [item.get_json() for item in db_result.items]
    pagination = {
        'count': total_count,
        'page': page,
        'limit': limit,
        'pages': math.ceil(total_count / limit)
    },
    return data, pagination


def statistics(args):
    try:
        start_date = time.strptime(args.get('start_date'), valid_date_format)
        end_date = time.strptime(args.get('end_date'), valid_date_format)
        symbols = args.get('symbols', '').split(',')
    except Exception as e:
        raise Exception(f'please check params, params={args}, error={str(e)}')
    filters = []
    if start_date:
        filters.append(FinancialData.date >= start_date)
    if end_date:
        filters.append(FinancialData.date <= end_date)
    if symbols:
        filters.append(FinancialData.symbol.in_(symbols))
    db_result = db.session.query(
        db.func.avg(FinancialData.open_price).label('avg_open_price'),
        db.func.avg(FinancialData.close_price).label('avg_close_price'),
        db.func.avg(FinancialData.volume).label('avg_volume')
    ).filter(*filters).first()
    print(start_date)

    return {
        'start_date': time.strftime(valid_date_format, start_date),
        'end_date': time.strftime(valid_date_format, end_date),
        'symbols': ','.join(symbols),
        'average_daily_open_price': round(db_result.avg_open_price, 2) if db_result.avg_open_price else 0,
        'average_daily_close_price': round(db_result.avg_close_price, 2) if db_result.avg_close_price else 0,
        'average_daily_volume': int(round(db_result.avg_volume)) if db_result.avg_volume else 0
    }
