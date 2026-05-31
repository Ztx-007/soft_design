from dataclasses import dataclass
from typing import Self, ClassVar, Any, TypeVar, dataclass_transform


#singleton factory

@dataclass(frozen=True, slots=True)
class Config:
    env: str
    debug: bool = False

    #通过数据类做单例工厂 可以内置一个类变量 并用类方法做初始化 别用__init__ 不好搞
    _cache: ClassVar[dict[str, Self]] = {}

    @classmethod
    def for_env(cls, env: str, debug: bool = False) -> Self:
        if env not in cls._cache:
            cls._cache[env] = cls(env=env, debug=debug)
        return cls._cache[env]


#auto-registry

REGISTRY: dict[str, type[Any]] =  {}

T = TypeVar("T")

#用于装饰类的装饰器；它的作用是把类变成 dataclass，并按类名注册到 REGISTRY 中，把类按类名注册，方便后续初始化实例
@dataclass_transform()
def event(cls: type[T]) -> type[T]:
    REGISTRY[cls.__name__] = dataclass(cls)
    return cls

@event
class UserCreated:
    user_id: int

@event
class UserDeleted:
    user_id: int

#


if __name__ == '__main__':
    user = UserCreated(1)
    print(user)
    print(REGISTRY)
