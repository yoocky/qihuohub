import easyquotation
from flask import Flask, request, jsonify, Response
from flask_cache import Cache
from flask_apscheduler import APScheduler
import json

class Config(object):
    JOBS = [
            {
              'id':'quote',
              'func':'__main__:get_all_quotes_from_cache',
              'args': '',
              'trigger': 'interval',
              'seconds': 5
            }
        ]
       
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
# init cache
cache = Cache()
cache = Cache(config={
    "CACHE_TYPE":"simple"
})
cache.init_app(app)

def make_cache_key(*args, **kwargs):
    """Dynamic creation the request url."""

    path = request.path
    args = str(hash(frozenset(request.args.items())))
    return (path + args).encode('utf-8')

@cache.cached(timeout=100000, key_prefix='codes')
def get_all_codes_list():
    codes = []
    data = json.loads(easyquotation.get_futures_codes(True))
    for val in data.values():
      for item in val:
        codes.append(item[1])
    return codes

@cache.cached(timeout=5, key_prefix='quotes')
def get_all_quotes():
    codes = get_all_codes_list()
    quotation = easyquotation.use("ctp")
    quotes = quotation.real(codes)
    return quotes

def get_all_quotes_from_cache():
    with app.app_context():
      return get_all_quotes()

@app.route('/', methods=['GET'])
@cache.cached(timeout=5, key_prefix=make_cache_key)
def get_quote():
    stock_list = request.args['list'].split(',')
    stock_type = request.args.get('type', 'ctp')
    if stock_type in ['stock']:
      quotation = easyquotation.use("sina")
      data = quotation.real(stock_list)
    else:
      quotes = get_all_quotes_from_cache()
      data = {key:value for key,value in quotes.items() if key in stock_list}
    return jsonify(data)

@app.route('/codes', methods=['GET'])
@cache.cached(timeout=100000, key_prefix=make_cache_key)
def get_codes():
    stock_type = request.args.get('type', 'ctp')
    if stock_type in ['stock']:
      data = easyquotation.get_stock_codes(True)
      return jsonify(data)
    else:
      data = easyquotation.get_futures_codes(True)
      resp = Response(data)
      resp.headers['Content-Type'] = 'application/json;charset=UTF-8'
      return resp
    

if __name__ == '__main__':
    # init scheduler
    scheduler = APScheduler()
    app.config.from_object(Config())
    scheduler.init_app(app)
    scheduler.start()
    app.run(host='0.0.0.0', port=5000)