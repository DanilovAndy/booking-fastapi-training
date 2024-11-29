from sqlalchemy.types import DateTime
from sqlalchemy.sql import expression


class UtcNow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True
