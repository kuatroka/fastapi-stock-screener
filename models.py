from sqlalchemy import Column, Integer, String, Numeric


from database import Base


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    price = Column(Numeric(10, 2))
    forward_pe = Column(Numeric(10, 2))
    forward_eps = Column(Numeric(10, 2))
    dividend_yield = Column(Numeric(10, 2))
    ma50 = Column(Numeric(10, 2))
    ma200 = Column(Numeric(10, 2))


# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")
