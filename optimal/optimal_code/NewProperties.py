import pandas as pd
from functools import cache
import json
import os
from typing import Any, Sequence, Protocol
from dataclasses import dataclass, replace
from itertools import pairwise
from pathlib import Path
@dataclass(frozen=True)
class Sale:
    amount: float
    currency: str
    converted: float | None = None


# expensive csv loading(no cache)
# Cache
@cache
def total_from_file(path: str) -> float:
    print(f"reading file {path}")
    df = pd.read_csv(path, names=['temp', 'pH'], encoding="utf-8", header=None)
    return df['temp'].count()


# Protocol不必显式继承，但类型检查会直接帮你报错如果不符合protocol
class RateFetcher(Protocol):
    def get_rate(self, currency: str) -> float:
        ...


class StaticRateFetcher:
    def get_rate(self, currency: str) -> float:
        rates = {"USD": 1.0, "EUR": 1.1}
        return rates.get(currency, 1.0)


# 通过dataclasses的replace方法去保留源对象不变 返回修改后的新对象
def convert_sale(sale: Sale, fetcher: RateFetcher) -> Sale:
    rate = fetcher.get_rate(sale.currency)
    return replace(sale, converted=rate * sale.amount)


#adjacency algorithms的优化方式 itertools的pairwise,返回n-1个邻接pair(tuplu,)
def compute_sales_deltas(numbers: Sequence[float]) -> list[float]:
    # res: list[float] = []
    # for i in range(len(numbers) - 1):
    #     res.append(numbers[i + 1] - numbers[i])
    # return res

    return [b-a for a,b in pairwise(numbers)]


#赋值表达式，海象运算符 典型场景 因为python没有do while
#允许在表达式内部完成赋值，并且该赋值表达式本身具有返回值，其返回值即为被赋的对象
def read_large_file(path: str) -> int:
    total = 0
    #创建二进制流
    f = open(path, "rb")
    while chunk := f.read(100):
        total += len(chunk)
    return total


def load_all_json_files(dir: str) -> dict[str, Any]:
    res: dict[str, Any] = {}
    for filename in os.listdir(dir):
        if not filename.endswith(".json"):
            continue
        try:
            with open(os.path.join(dir, filename)) as f:
                res[filename[:-5]] = json.load(f)
        except Exception:
            pass
    return res

#用Pathlib库替换
def new_load_all_json_files(dir: str) -> dict[str, Any]:
    res: dict[str, Any] = {}
    for path in Path(dir).glob(".json"):
        data = json.loads(path.read_text())
        res[path.stem] = data
    return res
if __name__ == '__main__':
    print(total_from_file("./do_daye.csv"))
    print(total_from_file("./do_daye.csv"))
