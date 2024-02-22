import orjson
from sqlmodel import SQLModel


def orjson_dumps(v, *, default=None, sort_keys=False, indent_2=True):
    option = orjson.OPT_SORT_KEYS if sort_keys else None
    if indent_2:
        # orjson.dumps returns bytes, to match standard json.dumps we need to decode
        # option
        # To modify how data is serialized, specify option. Each option is an integer constant in orjson.
        # To specify multiple options, mask them together, e.g., option=orjson.OPT_STRICT_INTEGER | orjson.OPT_NAIVE_UTC
        if option is None:
            option = orjson.OPT_INDENT_2
        else:
            option |= orjson.OPT_INDENT_2
    if default is None:
        return orjson.dumps(v, option=option).decode()
    return orjson.dumps(v, default=default, option=option).decode()


class SQLModelSerializable(SQLModel):
    """
    这个类继承自 SQLModel。SQLModel 是一个库，它结合了 SQLAlchemy 和 Pydantic 的特性，用于同时处理数据库模型和数据验证。
    SQLModelSerializable 类通过定义 Config 子类并设置 orm_mode 为 True，使得其实例可以像 ORM 对象一样使用，
    同时还可以享受 Pydantic 提供的数据序列化和验证功能。此外，它还自定义了 JSON 的序列化和反序列化方法，使用 orjson 库来提高性能。
    """
    class Config:
        orm_mode = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
