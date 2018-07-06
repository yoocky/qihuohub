import easyquotation
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_quote():
    stock_list = request.args['list'].split(',')
    stock_type = request.args.get('type', 'ctp')
    if stock_type in ['stock']:
      quotation = easyquotation.use("sina")
    else:
      quotation = easyquotation.use("ctp")
    data = quotation.real(stock_list)
    return jsonify(data)

@app.route('/codes', methods=['GET'])
def get_codes():
    stock_type = request.args.get('type', 'ctp')
    if stock_type in ['stock']:
      data = jsonify(easyquotation.get_stock_codes(True))
    else:
      data = easyquotation.get_futures_codes(True)
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)