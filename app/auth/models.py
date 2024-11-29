import uuid
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.auth.utils import UtcNow
from app.database import Base


class BlackListToken(Base):
    __tablename__ = "blacklisttokens"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, index=True, default=uuid.uuid4
    )
    expire: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(server_default=UtcNow())
