#甚至可以加备用函数集成到装饰器的参数中,然后把全部失败 的返回路径返回return backup_fn()的结果来增强代码健壮性
#改写方面 也可也不传主备用api 不用装饰器,直接传一个函数列表,里面for循环遍历这个列表就行了,这样就不会有什么主api副api之分
#tenacity是一个现成的装饰器库 可以直接用来做api访问重试,增强代码健壮性.
import random 
import httpx
from typing import Callable,Any
from functools import wraps
import time

def retry_decorator[T](retries: int = 3, delay: float = 1.0, backoff:float =2.0):
    def decorator(func: Callable[...,T]) -> Callable[...,T]:
        @wraps(func)
        def warpper(*args:Any, **kwargs:Any) -> T:
            for attemp in range(retries):
                try:
                    return func()
                except Exception as e:
                    print(f"error message:{e}")
                    if attemp == retries-1:
                        raise RuntimeError("achieve max retries")
                    sleep_time = delay * ((backoff)**(attemp)) #指数退避
                    print(f"retrying in {sleep_time} seconds...")
                    time.sleep(delay)    
            raise RuntimeError("all failed")
        return warpper
    return decorator
            
@retry_decorator()
def get_joke() -> str:
    if random.random() < 0.5:
        raise RuntimeError("didn't get it")
    with httpx.Client() as client:
        response = client.get("https://api.chucknorris.io/jokes/random")
        response.raise_for_status()
        data: dict[str, str] = response.json()
        return data["value"]
    
def main():
    joke = get_joke()
    print(joke)


if __name__ == "__main__":
    main()
