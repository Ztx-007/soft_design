from dataclasses import dataclass, field
from typing import  Self
#frozen的不可变性仅针对于属性，对于属性里的可变容器，还是可以新增的。
#slots= True 强制不可后续新增属性，强制移除实例字典来改善内存使用并加速属性访问
#kw_noly = True 只能通过关键字传参 不可通过posi
#此外，这玩意本质是个类，可以设置类方法来做自定义初始化
#还有，数据类有好用的序列化辅助工具， 如asdict传入对象转为字典 或astuple转为元组
#最后 可以跟抽象基类结合使用
from abc import ABC, abstractmethod

@dataclass(frozen=True, order=True) #对数据类采用frozen参数可以冻结数据类，这样就不能通过post_init对他进行赋值，但是可以绕过
class User:
    name: str
    email: str
    active: bool = True  # 默认值
    tags: list[str] = field(default_factory=list[str])
    slug: str = field(init=False) #与post_init配合 也就是不能通过直接传参进行初始化

    def __post_init__(self):
        # self.name = self.name.strip().title()
        # slugified = self.name.lower().replace(' ','-')
        # self.slug = slugified
        normalized_name = self.name.strip().title()
        slugified = self.name.lower().replace(' ','-')

        object.__setattr__(self,"name", normalized_name)
        object.__setattr__(self,"slug", slugified)

    @classmethod
    def from_email(cls, email:str) -> Self:
        local = email.strip().split('@')[0].replace('.', ' ')
        return cls(name=local, email=email)

    def contact_card(self) -> str:
        return f"{self.name} - {self.email}"


    @property
    def domain(self) -> str:
        return self.email.split('@')[-1]

@dataclass
class Account(ABC):
    owner: str
    base_fee: float

    @property
    @abstractmethod
    def monthly_fee(self) -> float:
        ...

@dataclass
class FreeAccount(Account):
    @property
    def monthly_fee(self) -> float:
        return 0.0

def main():
    u1 = User(name='ztx tony', email="1062536464@qq.com")
    u2 = User(name='llxz', email="tiffanylee010915@gmail.com")
    print(u1 < u2)
    u3 = User.from_email("ztx.pizza@qq.com")
    print(u3)
    a4 = FreeAccount(owner='ztx',base_fee=100.0)
    print(a4.monthly_fee)

if __name__ == '__main__':
    main()
