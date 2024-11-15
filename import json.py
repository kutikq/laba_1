import json
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Optional

# 1. Мероприятие
class Event:
    def __init__(self, name: str, date_time: datetime, venue: 'Venue'):
        self.name = name  # Название мероприятия
        self.date_time = date_time  # Дата и время проведения
        self.venue = venue  # Место проведения (объект Venue)


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
    
    def calculate_total_price(self) -> float:
        return sum(ticket.category.price for ticket in self.tickets)

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
    def __init__(self, user: User, event: Event):
        self.user = user
        self.event = event
        self.rating = None
        self.comment = None

    def set_rating(self):
        while True:
            try:
                grade = input("Введите рейтинг (от 1 до 5): ")
                gradeInt = int(grade)
                if 1 <= gradeInt <= 5:
                    self.rating = gradeInt
                    break
                else:
                    print("\nРейтинг должен быть от 1 до 5!")
            except ValueError:
                print("\nОшибка: введено не число. Попробуйте снова.")

    def set_comment(self):
        self.comment = input("Введите комментарий (необязательно): ")

    def __str__(self):
        return f"Feedback by {self.user.name} for {self.event.name} - Rating: {self.rating}, Comment: {self.comment or 'No comment'}"


venue = Venue("Concert Hall", "123 Main St", 100)
seat = Seat(1, 1)
venue.add_seat(seat)
category = Category("VIP", 100.0)
event = Event("Concert", datetime(2024, 12, 31, 20, 0), venue)
ticket = Ticket(event, seat, category)
user = User("John Doe")
order = Order(user, [ticket])

print(f"Order Total: {order.calculate_total_price()}")
payment = Payment(order, order.calculate_total_price())
payment.process()


# Функции для работы с JSON
def write_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def read_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


# Функции для работы с XML
def write_xml(data, filename):
    root = ET.Element("events")
    
    for event in data['events']:
        event_elem = ET.SubElement(root, "event")
        ET.SubElement(event_elem, "name").text = event['name']
        ET.SubElement(event_elem, "date_time").text = event['date_time']
        
        venue_elem = ET.SubElement(event_elem, "venue")
        ET.SubElement(venue_elem, "name").text = event['venue']['name']
        ET.SubElement(venue_elem, "address").text = event['venue']['address']
        ET.SubElement(venue_elem, "capacity").text = str(event['venue']['capacity'])
        
        seats_elem = ET.SubElement(venue_elem, "seats")
        for seat in event['venue']['seats']:
            seat_elem = ET.SubElement(seats_elem, "seat")
            ET.SubElement(seat_elem, "row").text = str(seat['row'])
            ET.SubElement(seat_elem, "number").text = str(seat['number'])
            ET.SubElement(seat_elem, "is_available").text = str(seat['is_available']).lower()
        
        tickets_elem = ET.SubElement(event_elem, "tickets")
        for ticket in event['tickets']:
            ticket_elem = ET.SubElement(tickets_elem, "ticket")
            category_elem = ET.SubElement(ticket_elem, "category")
            ET.SubElement(category_elem, "name").text = ticket['category']['name']
            ET.SubElement(category_elem, "price").text = str(ticket['category']['price'])
            seat_elem = ET.SubElement(ticket_elem, "seat")
            ET.SubElement(seat_elem, "row").text = str(ticket['seat']['row'])
            ET.SubElement(seat_elem, "number").text = str(ticket['seat']['number'])
            ET.SubElement(ticket_elem, "is_booked").text = str(ticket['is_booked']).lower()
    
    tree = ET.ElementTree(root)
    tree.write(filename, encoding='utf-8', xml_declaration=True)


def read_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    data = {"events": []}
    
    for event_elem in root.findall("event"):
        event = {
            "name": event_elem.find("name").text,
            "date_time": event_elem.find("date_time").text,
            "venue": {
                "name": event_elem.find("venue/name").text,
                "address": event_elem.find("venue/address").text,
                "capacity": int(event_elem.find("venue/capacity").text),
                "seats": []
            },
            "tickets": []
        }
        for seat_elem in event_elem.find("venue/seats").findall("seat"):
            event["venue"]["seats"].append({
                "row": int(seat_elem.find("row").text),
                "number": int(seat_elem.find("number").text),
                "is_available": seat_elem.find("is_available").text == "true"
            })
        for ticket_elem in event_elem.find("tickets").findall("ticket"):
            ticket = {
                "category": {
                    "name": ticket_elem.find("category/name").text,
                    "price": float(ticket_elem.find("category/price").text)
                },
                "seat": {
                    "row": int(ticket_elem.find("seat/row").text),
                    "number": int(ticket_elem.find("seat/number").text)
                },
                "is_booked": ticket_elem.find("is_booked").text == "true"
            }
            event["tickets"].append(ticket)
        data["events"].append(event)
    
    return data


# Тестирование
data = {
    "events": [
        {
            "name": "Concert",
            "date_time": "2024-12-31T20:00:00",
            "venue": {
                "name": "Concert Hall",
                "address": "123 Main St",
                "capacity": 100,
                "seats": [
                    {"row": 1, "number": 1, "is_available": True},
                    {"row": 1, "number": 2, "is_available": False}
                ]
            },
            "tickets": [
                {
                    "category": {"name": "VIP", "price": 100.0},
                    "seat": {"row": 1, "number": 1},
                    "is_booked": False
                }
            ]
        }
    ]
}

# Сохранение данных
write_json(data, "events.json")
write_xml(data, "events.xml")

# Чтение данных
json_data = read_json("events.json")
xml_data = read_xml("events.xml")

# Проверка результатов
print("JSON Data:", json_data)
print("XML Data:", xml_data)
