import sqlite3 as sq
from typing import List, Optional
from appointment.appointment import Salon, Service


class ServiceManager:
    def __init__(self, conn: sq.Connection, salon: Salon):
        self.conn = conn
        self.salon = salon

    def check_service(self, service_name: str) -> dict:
        try:
            cur = self.conn.cursor()
            cur.execute('SELECT name FROM services;')
            if (service_name,) in cur.fetchall():
                return {"message": f"Услуга {service_name} уже существует.", "success": False}
            return {"message": "Название услуги свободно", "success": True}
        except Exception as e:
            return {"message": f"Ошибка : {e}", "success": False}

    def add_service(self, service: Service) -> dict:
        try:
            if self.check_service(service.name)['success']:
                cur = self.conn.cursor()
                cur.execute(
                    'INSERT INTO services(name, price) VALUES (?, ?)',
                    (service.name, service.price)
                )
                self.conn.commit()
                self.salon.services.append(service)
                return {"message": "Услуга добавлена", "success": True}
            return {"message": f"Услуга {service.name} уже существует!", "success": False}
        except Exception as e:
            return {"message": f"Ошибка при добавлении услуги: {e}", "success": False}

    def upd_price(self, name: str, price: int) -> dict:
        try:
            cur = self.conn.cursor()
            cur.execute('UPDATE services SET price = ? WHERE name = ?', (price, name))
            self.conn.commit()
            return {"message": f"Цена {name} изменена", "success": True}
        except Exception as e:
            return {"message": f"Ошибка при изменении цены : {e}", "success": False}
