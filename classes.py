from datetime import datetime
from typing import List, Optional

# 1. Мероприятие
class Event:
    def __init__(self, name: str, date_time: datetime, venue: 'Venue'):
        self.name = name  # Название мероприятия
        self.date_time = date_time  # Дата и время проведения
        self.venue = venue  # Место проведения (объект Venue)
        self.tickets: List['Ticket'] = []  # Список всех билетов на мероприятие

# 2. Место проведения
class Venue:
    def __init__(self, name: str, address: str, capacity: int):
        self.name = name  
        self.address = address  
        self.capacity = capacity  # Вместимость
        self.seats: List['Seat'] = []  

    def add_seat(self, seat: 'Seat'):
        self.seats.append(seat)  # Добавление места в список мест


# 3. Место (в зале)
class Seat:
    def __init__(self, row: int, number: int):
        self.row = row  
        self.number = number  
        self.is_available = True  

    def book(self):
        if not self.is_available:
            raise ValueError("Seat is already booked")  #  место занято
        self.is_available = False  # Устанавливаем, что место занято

# 4. Билет
class Ticket:
    def __init__(self, event: Event, seat: Optional['Seat'], category: 'Category'):
        self.event = event  # Событие, к которому относится билет
        self.seat = seat  
        self.category = category  
        self.is_booked = False  

    def book(self):
        if self.is_booked:
            raise ValueError("Ticket is already booked")  # ошибка, билет забронирован
        self.is_booked = True  # билет забронирован

# 5. Категория билетов
class Category:
    def __init__(self, name: str, price: float):
        self.name = name  # Название категории (например, VIP, стандарт)
        self.price = price  # Цена билета этой категории

# 6. Пользователь
class User:
    def __init__(self, name: str):
        self.name = name  
        self.orders: List['Order'] = []  # Список заказов пользователя

    def place_order(self, order: 'Order'):
        self.orders.append(order)  # Добавление заказа в список заказов пользователя

# 7. Заказ
class Order:
    def __init__(self, user: User, tickets: List[Ticket]):
        self.user = user  
        self.tickets = tickets
        self.is_paid = False 

    def apply_discount(self, discount: 'Discount'):
        self.total_price -= discount.apply(self.total_price)  # Применение скидки к общему заказу

    def pay(self):
        if self.is_paid:
            raise ValueError("Order is already paid")  # заказ уже оплачен
        self.is_paid = True  #  заказ оплачен

# 8. Платеж
class Payment:
    def __init__(self, order: Order, amount: float):
        self.order = order  
        self.amount = amount 
        self.is_successful = False  
        self.payment_date = None  # Дата платежа

    def process(self):
        self.is_successful = True  # Считаем, что платеж успешен
        self.payment_date = datetime.now()  # Устанавливаем дату платежа
        self.order.pay()  # Помечаем заказ как оплаченный

# 9. Скидка
class Discount:
    def __init__(self, code: str, percentage: float):
        self.code = code  # Код скидки
        self.percentage = percentage  # Процент скидки

    def apply(self, total_price: float) -> float:
        return total_price * (self.percentage / 100)  # Возвращает сумму скидки

#10. Отзыв
class Feedback:
    def __init__(self, user: User, event: Event, rating: int, comment: Optional[str] = None):
        self.user = user 
        self.event = event  
        self.rating = rating  
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")
        self.comment = comment  # Текст отзыва (опционально)

    def __str__(self):
        return f"Feedback by {self.user.name} for {self.event.name} - Rating: {self.rating}, Comment: {self.comment or 'No comment'}"


