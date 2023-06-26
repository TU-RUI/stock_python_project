import helper
from config import app
from flask import jsonify, request


@app.route('/hello', methods=['GET'])
def hello_world():
    return 'world'


# Get financial_data API to retrieve records from financial_data table
@app.route('/api/financial_data', methods=['GET'])
def get_financial_data():
    try:
        data, pagination = helper.query(request.args)
        response = {
            'data': data,
            'pagination': pagination,
            'info': {'error': ''}
        }
    except Exception as e:
        response = {
            'data': [],
            'pagination': {},
            'info': {'error': str(e)}
        }
    return jsonify(response)


# Get statistics API to perform the following calculations on the data in given period of time
@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    try:
        data = helper.statistics(request.args)
        response = {
            'data': data,
            'info': {'error': ''}
        }
    except Exception as e:
        response = {
            'data': [],
            'info': {'error': str(e)}
        }
    return jsonify(response)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
