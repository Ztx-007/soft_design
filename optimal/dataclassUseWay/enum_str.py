from enum import StrEnum
from dataclasses import dataclass
from typing import Protocol

#同一个枚举成员，在程序运行期间通常是单例
class AccountStatus(StrEnum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

#这里用Protocal可以用编译器检查 不用显示继承AccountDataView，
class AccountDataView(Protocol):
    account_id: int
    _account_name: str
    _account_status: AccountStatus

    @property
    def is_active(self) -> bool:
        ...

    @is_active.setter
    def is_active(self, is_active: bool) -> None:
        ...


@dataclass
class Account:
    account_id: int
    _account_name: str
    _account_status: AccountStatus

    @property
    def is_active(self) -> bool:
        return self._account_status is AccountStatus.ACTIVE

    @is_active.setter
    def is_active(self, is_active: bool) -> None:
        self._account_status = AccountStatus.ACTIVE if is_active else AccountStatus.INACTIVE

def get_user_view(user: AccountDataView) -> None:
    print(user.account_id)
    print(user.is_active)

if __name__ == '__main__':
    account_a = Account(1, "ztx", AccountStatus.ACTIVE)
    account_a.is_active = False
    #不建议在property和is_active里面做一些持久化io操作，违背了属性简单化的原则 可以单独设一个save或者update函数的实例方法 可以来做这种时间密集型io操作
    print(account_a)

    #如果需要异步访问数据库或者一些时间io操作，可以用@classmethod async def load:定义异步函数 或者async def save(self)定义更新实例所对应在数据库种的数据 用await调用即可， 或者await asyncio.gather(要调用的异步函数)
    get_user_view(account_a)