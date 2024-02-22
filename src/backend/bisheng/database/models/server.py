from datetime import datetime
from typing import Optional

from bisheng.database.base import session_getter
from bisheng.database.models.base import SQLModelSerializable
from sqlalchemy import Column, DateTime, text
from sqlmodel import Field, select


class ServerBase(SQLModelSerializable):
    """
    这个类作为一个基类，定义了 Server 表的基本结构，但它本身不会直接映射到数据库中的一个表。
    """
    endpoint: str = Field(index=False, unique=True)
    server: str = Field(index=True)
    remark: Optional[str] = Field(index=False)
    create_time: Optional[datetime] = Field(sa_column=Column(
        DateTime, nullable=False, index=True, server_default=text('CURRENT_TIMESTAMP')))
    update_time: Optional[datetime] = Field(
        sa_column=Column(DateTime,
                         nullable=False,
                         server_default=text('CURRENT_TIMESTAMP'),
                         onupdate=text('CURRENT_TIMESTAMP')))


class Server(ServerBase, table=True):
    """
    这个类继承自 ServerBase 并且通过 table=True 参数标记为一个表模型。
    这意味着 Server 类不仅继承了 ServerBase 中定义的字段，还将被 SQLModel 识别为一个数据库表的映射。
    这里的 table=True 参数是告诉 SQLModel 这个类应该被视为一个数据库表的映射，而不仅仅是一个普通的 Python 类或者基类。
    这样，当 SQLModel 或者 SQLAlchemy 执行数据库操作时，就会知道这个类对应于数据库中的一个具体表。
    """
    id: Optional[int] = Field(default=None, primary_key=True)


# 封装业务操作
class ServerDao(ServerBase):
    @classmethod
    def find_server(cls, server_id: int) -> Server | None:
        with session_getter() as session:
            statement = select(Server).where(Server.id == server_id)
            """
            # 在数据库中查询符合条件的第一条记录。
            session.exec(statement)执行查询操作后，返回的是一个结果集（通常是一个迭代器），其中包含了查询到的所有Server实例。
            如果查询到了符合条件的记录，.first()会返回这条记录对应的Server实例；如果没有查询到符合条件的记录，.first()会返回None。

            statement 是一个 SQLAlchemy 的 Select 对象。这个对象不是迭代器，它描述了一个 SQL 选择（SELECT）语句。

            下面返回的类型要么是一个 Server类的实例，要么是 None。

            为何返回可能会是一个server类的实例，而不是数据库里面的数值信息？
                这里涉及到 ORM（Object-Relational Mapping，对象关系映射）的概念，它是一种编程技术，用于在不兼容的类型系统之间转换数据。
                ORM 允许我们将数据库表（通常是关系型数据库中的表）映射为编程语言中的类，表中的记录（行）映射为类的实例，而表的列映射为类实例的属性。

                SQLAlchemy 是 Python 中一个流行的 ORM 框架。当你使用 SQLAlchemy 定义一个模型类（比如 Server 类）时，
                你实际上是在定义数据库表的结构，以及如何将表中的数据转换为 Python 对象。这样，当你从数据库查询数据时，
                SQLAlchemy 能够自动将这些数据转换为相应的 Python 对象，这就是为什么你会得到一个 Server 类的实例，而不是简单的字符串或数值。

                因此，当你从数据库查询数据时，你不是直接得到原始数据（如字符串或数值），而是得到了一个充满了这些数据的 Server 类的实例
            """
            return session.exec(statement).first()  


class ServerRead(ServerBase):
    id: Optional[int]


class ServerQuery(ServerBase):
    id: Optional[int]
    server: Optional[str]


class ServerCreate(ServerBase):
    pass
