#代码重构
#少用try except结构 让他直接崩溃，在测试阶段方便找bug
#首先编写测试，保证重构后满足当前逻辑的基础
#采用卫语句扁平化else结构 让函数提前返回
#用函数包装长条件语句 方便解耦
#合并拒绝逻辑


from dataclasses import dataclass, field

@dataclass
class Item:
    name : str
    price : float

@dataclass 
class Order:
    amount : float
    has_discount : bool
    region: str
    currency: str
    type :str
    items: list[Item] = field(default_factory=list)

@dataclass
class User:
    is_premiun: bool
    is_admin: bool
    is_trial: bool
    region: str
#重构复杂的if else逻辑要从最外层开始拆,把一些else分支 用卫语句替代,也就是提前检查直接返回的语句

def is_eligible_amount(order: Order, user: User) -> bool:
    return order.amount > 1000 or (order.type != "bulk" and not user.is_trial)


Valid_country_currency = {
    ("EU","EUR") : True,
    ("US", "USD") : True
}
def has_valid_currency(order: Order, user: User) -> bool:
    return Valid_country_currency.get((order.region, order.currency), False)

def approve_order(order: Order, user: User):
    if user.is_admin:
        return "approve"
    
    rejection_rules = [
        lambda: not user.is_premiun,
        lambda: order.amount is None,
        lambda: not is_eligible_amount(order, user),
        lambda: order.has_discount,
        lambda: not has_valid_currency(order, user),
        lambda: any(item.price <0 for item in order.items)
    ]

    if any(rule() for rule in rejection_rules):
        return "reject"
    # if not user.is_premiun:
    #     return "reject"
    # if order.amount is None:
    #     return "reject"
    # if not is_eligible_amount(order, user):
    #     return "reject"
    # if order.has_discount:
    #     return "reject"
    # if not has_valid_currency(order, user):
    #     return "reject"
    # if any(item.price <0 for item in order.items):
    #     return "reject"

    return "approve"


if __name__ == "__main__":
    main()
