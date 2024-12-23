from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship

from app.database import Base


class Hotels(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON)
    rooms_quantity = Column(Integer, nullable=False)
    image_link = Column(String)

    rooms = relationship("Rooms", back_populates="hotel")

    def __str__(self):
        return f"{self.name} {self.location}"



