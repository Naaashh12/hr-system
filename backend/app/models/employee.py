from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base
from sqlalchemy.orm import relationship
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    department = Column(String)
    position = Column(String)
    salary = Column(Float)
    hire_date = Column(Date)

    leaves = relationship("Leave", back_populates="employee")