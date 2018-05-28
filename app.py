import easyquotation
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/quote', methods=['GET'])
def get_quote():
    stock_list = request.args['list'].split(',')
    stock_type = request.args.get('type', 'ctp')
    if stock_type in ['stock']:
      quotation = easyquotation.use("sina")
    else:
      quotation = easyquotation.use("ctp")
    data = quotation.real(stock_list)
    return jsonify(data)

if __name__ == '__main__':
    app.run()