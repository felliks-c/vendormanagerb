from sqlalchemy import Column, Integer, String, Float
# Предполагаем, что Base импортируется из вашего файла database.py
from .database import Base 

class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    # Имя поставщика - обязательное поле
    name = Column(String, index=True, nullable=False)
    # Контактный email - должен быть уникальным
    contactEmail = Column(String, unique=True, index=True, nullable=False)
    # Категория - например, "Food", "Tech", "Services"
    category = Column(String, index=True, nullable=False)
    # Рейтинг - число с плавающей точкой
    rating = Column(Float, default=0.0)

    # Метод __repr__ для удобного отображения объекта при отладке
    def __repr__(self):
        return f"<Vendor(id={self.id}, name='{self.name}', email='{self.contactEmail}')>"