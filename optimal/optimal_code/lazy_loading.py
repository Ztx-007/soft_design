Z#lazy loading, if your data is so large, u can choose to lazy load it with less waiting time
#first way is moving your loading function to the inner of cal function, but it will be terrible if u have many times of operation, because it will reload it again and again
#so we can use the functools's function -> cache to avoid reloading simple use  @cache
#but if u get data from remote server, the data may be outtime when u set cache. so we should set the ttl_cache 用cachetools 库 的TTLcache,cached
#u can choose to return a generator instead of list of dict
#另外，也可通过开辟另一个线程，实现预加载，但要考虑线程安全问题

import csv
from typing import List, Callable, Any
import pandas as pd
import  numpy as np
from functools import cache, wraps
import time

#可以用LRU改一下，这个比较粗糙，可以改一个带缓存条数的。
def ttl_cache(seconds: int) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorate(func: Callable[..., Any]) -> Callable[..., Any]:
        cache_data = {}
        cache_time = {}

        @wraps(func)  #这个装饰器是用来保留原传入函数的元数据 比如函数名__name__ 和__doc__的，如果不加， 你后面调用被装饰的函数，元数据就是wrapper 且信息丢失

        def wapper(*args, **kwargs):
            key = (args, tuple(kwargs.items()))
            now = time.time()

            if key in cache_data and (now - cache_data[key]) < seconds:
                return cache_data[key]
            
            result = func(*args, **kwargs)
            cache_data[key] = result
            cache_time[key] = now
            return result
            
        return wapper
    return decorate

@cache
def load_csv_file(file_name: str) -> list[dict[str, str]]:
    with open(file_name, encoding='utf-8') as f:
        file = csv.DictReader(f)
        return [row for row in file]

def get_conversion_rates() -> dict[str, float]:
    time.sleep(5)
    return {'USD': 1.0, 'EUR': 1.2}

def analyse_water_do(data: list[dict[str, str]]) -> float:
    total = 0.0
    for row in data:
        total += float(row['DO'])
    
    rate = get_conversion_rates()
    total *= rate['USD']
    return total / len(data)

def analyse_water_ph(data: list[dict[str, str]]) -> float:
    total = 0.0
    for row in data:
        total += float(row['pH'])
    return total / len(data)

        


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # slow loading
    
    
    while True:
        print('plz enter num for next res')
        num = input('u should input your choice here:')
        if num == '1':
            data = load_csv_file('./do_daye.csv')
            print(analyse_water_do(data))
        elif num == '2':
            data = load_csv_file('./do_daye.csv')
            print(analyse_water_ph(data))
        else:
            break
    

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
