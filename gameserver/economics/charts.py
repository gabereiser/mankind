from typing import List
from datetime import datetime as dt
from sqlalchemy import and_
from sqlalchemy.orm import Session
from uuid import UUID
import numpy as np
import pandas as pd
import database
import schemas
import models


class ChartOptions:
    def __init__(self, *args, **kwargs) -> None:
        self.options = kwargs


async def gen_chart_for_symbol(
    location_id: UUID,
    symbol: str,
    start_time: dt.datetime,
    end_time: dt.datetime,
    interval: dt.timedelta,
) -> List[schemas.CandleStick]:
    session: Session = next(database.session())
    orders = (
        session.query(models.MarketOrder)
        .filter(
            and_(
                models.MarketOrder.location_id == location_id,
                models.MarketOrder.symbol == symbol,
                models.MarketOrder.created >= start_time,
                models.MarketOrder.created <= end_time,
            )
        )
        .all()
    )
    transactions = []
    for order in orders:
        for t in order.transactions:
            transactions.append(
                {
                    "dt": t.date,
                    "symbol": symbol,
                    "price": order.ask_bid,
                    "volume": t.quantity,
                }
            )
    df = pd.DataFrame(data=transactions, index="dt")
    df.index = pd.to_datetime(df.index, format="%Y-%m-%d %H:%M:%S:%f")
    cdata = df["price"].resample(interval).ohlc(_method="ohlc")
    vdata = df["volume"].resample(interval).sum()
    resampled_data = pd.concat(
        [cdata, vdata],
        axis=1,
    )
    candles = []
    for index, row in resampled_data.iterrows():
        candlestick = schemas.CandleStick(
            symbol=row["symbol"],
            timestamp=row["dt"],
            open_v=row["open"],
            high_v=row["high"],
            low_v=row["low"],
            close_v=row["close"],
            volume=row["volume"],
        )
        candles.append(candlestick)
    return candles
