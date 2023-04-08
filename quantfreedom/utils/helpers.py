import os
import numpy as np
import pandas as pd

from pathlib import Path
import plotly.graph_objects as go

from quantfreedom._typing import pdFrame

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))


def delete_dir(p):
    for sub in p.iterdir():
        if sub.is_dir():
            delete_dir(sub)
        else:
            sub.unlink()
    p.rmdir()


def clear_cache():
    for p in Path(dir_path).parent.parent.rglob("numba_cache"):
        delete_dir(p)
    for p in Path(__file__).parent.parent.rglob("__pycache__"):
        delete_dir(p)
    for p in Path(__file__).parent.parent.rglob("*.py[co]"):
        p.unlink()


def pretty(object) -> None:
    try:
        object._fields[0]
        items = []
        indent = str("    ")
        for x in range(len(object)):
            items.append(indent + object._fields[x] + " = " + str(object[x]) + ",\n")
        print(type(object).__name__ + "(" + "\n" + "".join(items) + ")")
    except:
        print(object)


def generate_candles(
    number_of_candles: int,
    seed=None,
) -> pdFrame:
    np.random.seed(seed)

    periods = number_of_candles * 48

    prices = np.around(5000 + np.random.normal(scale=1.5, size=periods).cumsum(), 2)

    data = pd.DataFrame(
        prices,
        index=pd.Index(
            pd.date_range("01/01/2000", periods=periods, freq="30min"),
            name="open_time",
        ),
        columns=["price"],
    )
    data = data.price.resample("D").ohlc()

    data.columns = pd.MultiIndex.from_tuples(
        tuples=[
            ("QuantFreedom", "open"),
            ("QuantFreedom", "high"),
            ("QuantFreedom", "low"),
            ("QuantFreedom", "close"),
        ],
        name=["symbol", "candle_info"],
    )
    fig = go.Figure(
        data=go.Candlestick(
            x=data.index,
            open=data.iloc[:, 0],
            high=data.iloc[:, 1],
            low=data.iloc[:, 2],
            close=data.iloc[:, 3],
        )
    )
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.show()

    return data