from . import db
import datetime


class Ticker(db.Model):
    __tablename__ = 'tickers'    
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    tickername = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )

    def __repr__(self):
        return f'{self.tickername} id: {self.id}'


class TickerValue(db.Model):
    __tablename__ = 'tickers_values'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    ticker_id = db.Column(
        db.Integer,
        db.ForeignKey('tickers.id'),
        index=True,
        nullable=False
    )
    
    ticker_value = db.Column(
        db.Integer,
        index=False,
        nullable=False
    )
    
    processed_dttm = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        index=True,
        nullable=False
    )

    def __repr__(self):
        return f'Id: {self.ticker_id}, Value: {self.ticker_value}, Time: {self.processed_dttm}'
