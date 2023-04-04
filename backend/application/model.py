from application import Base

Cafeteria = Base.classes.Cafeteria
#这段代码是在 Python 中使用 SQLAlchemy 库时常见的一种写法。
# 它的意思是从 application 模块中导入 Base 对象，并使用该对象中的 classes 属性来获取名为 Cafeteria 的类。
#Base 是 SQLAlchemy 中的一个基础类，用于定义数据库中的表格结构。
# Base 中的 classes 属性是一个字典，包含了所有在数据库中定义的表格类，这些类都继承自 Base。
# 因此，通过 Base.classes 可以访问到所有表格类的属性。
#在这段代码中，Cafeteria 是数据库中的一个表格类，
# 通过 Base.classes.Cafeteria 可以访问该类。
# 这样做的好处是，在使用 SQLAlchemy 进行数据库操作时，可以方便地使用这些表格类来进行 CRUD 操作，而无需手动编写 SQL 语句。