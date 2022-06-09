from flask import request, make_response
from flask import current_app as app
from .models import db, Ticker, TickerValue


@app.route('/', methods=['GET'])
def homepage():
    return """<html>
        <body>
            <p><a href="/tickerboard/">Check out this tickerboard</a></p>
        </body>
    </html>"""

@app.route('/ticker/', methods=['POST'])
def add_ticker():
    tickername = request.json.get('tickername')
    if tickername:
        existing_ticker = Ticker.query.filter(Ticker.tickername == tickername).first()
        if existing_ticker:
            val = TickerValue\
                .query\
                .filter(TickerValue.ticker_id == existing_ticker.id)\
                .order_by(TickerValue.processed_dttm.desc())\
                .first()
            return {
                'ticker_id': existing_ticker.id,
                'ticker_value': val.ticker_value if val else 0
            }
        new_ticker = Ticker(
            tickername=tickername,
        )
        db.session.add(new_ticker)
        db.session.commit()
        new_ticker = Ticker.query.filter(Ticker.tickername == tickername).first()
        return {'ticker_id': new_ticker.id, 'ticker_value': 0}
    return 'bad request', 500


@app.route('/ticker_value/', methods=['POST'])
def add_ticker_value():
    if 'ticker_id' and 'ticker_value' in request.json:
        db.session.add(TickerValue(**request.json))
        db.session.commit()
        return 'success', 200
    return 'bad request', 500

@app.route('/tickers_values/', methods=['POST'])
def add_tickers_values_batch():
    try:
        db.session.add_all([TickerValue(**t) for t in request.json])
        db.session.commit()
        return 'success', 200
    except:
        return 'bad request', 500
