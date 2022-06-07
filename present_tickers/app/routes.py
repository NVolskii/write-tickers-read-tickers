from flask import request, render_template, make_response, jsonify
from datetime import datetime as dt
from flask import current_app as app
from .models import db, Ticker, TickerValue


@app.route('/', methods=['GET'])
def homepage():
    return 'Yo man'

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
                'tickername': existing_ticker.tickername,
                'id': existing_ticker.id,
                'val': val.ticker_value if val else 0
            }
        new_ticker = Ticker(
            tickername=tickername,
        )
        db.session.add(new_ticker)  # Adds new User record to database
        db.session.commit()  # Commits all changes
    return {'tickername': existing_ticker.tickername, 'id': existing_ticker.id}

@app.route('/ticker_value/', methods=['POST'])
def add_ticker_value():
    ticker_id = request.json.get('ticker_id')
    ticker_value = request.json.get('ticker_value')
    if ticker_id and ticker_value:
        new_value = TickerValue(
            ticker_id=ticker_id,
            ticker_value=ticker_value
        )
        db.session.add(new_value)
        db.session.commit()
        return make_response(f"{new_value} posted to db")
    return make_response(f'error posting to db')