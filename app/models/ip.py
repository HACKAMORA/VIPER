# models/ip.py

from sqlalchemy import Column, Integer, String
from database.base import Base


class IP(Base):
    __tablename__ = "ips"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    reverse_dns = Column(String)
    asn = Column(String)
    country = Column(String)