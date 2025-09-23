import sqlite3 as sq
from typing import List, Optional
from appointment.appointment import Salon, Client


class ClientService:
    def __init__(self, conn: sq.Connection, salon: Salon):
        self.conn = conn
        self.salon = salon

    def check_name(self, name: str) -> dict:
        try:
            cur = self.conn.cursor()
            cur.execute('SELECT name FROM clients;')
            if (name,) in cur.fetchall():
                return {"message": "Клиент с таким именем уже существует.", "success": False}
            return {"message": "Имя свободно.", "success": True}
        except Exception as e:
            return {"message": f"Ошибка : {e}", "success": False}

    def check_phone(self, phone: str) -> dict:
        try:
            cur = self.conn.cursor()
            cur.execute('SELECT phone FROM clients;')
            if (phone,) in cur.fetchall():
                return {"message": "Клиент с таким номером уже существует.", "success": False}
            return {"message": "Номер свободен", "success": True}
        except Exception as e:
            return {"message": f"Ошибка : {e}", "success": False}

    def add_client(self, name: str, phone: str, telegram_id: int) -> dict:
        try:
            if self.check_phone(phone)['success']:
                cur = self.conn.cursor()
                cur.execute(
                    'INSERT INTO clients(name, phone, telegram_id) VALUES (?, ?, ?)',
                    (name, phone, telegram_id)
                )
                self.conn.commit()
                client = Client(name, phone, telegram_id)
                self.salon.add_client(client)
                return {"message": "Клиент добавлен", "success": True}
            return {"message": f"Клиент с номером {phone} уже существует!", "success": False}
        except Exception as e:
            return {"message": f"Ошибка при добавлении клиента: {e}", "success": False}

    def update_client(self, name: str, phone: str) -> dict:
        try:
            cur = self.conn.cursor()
            cur.execute('UPDATE clients SET name = ? WHERE phone = ?', (name, phone))
            self.conn.commit()
            return {"message": "Имя клиента изменено", "success": True}
        except Exception as e:
            return {"message": f"Ошибка при изменении имени: {e}", "success": False}

    def get_client_id(self, name_or_telega_id: str) -> dict:
        try:
            cur = self.conn.cursor()
            if not name_or_telega_id.isdigit():
                cur.execute('SELECT id FROM clients WHERE name = ?', (name_or_telega_id,))
            else:
                cur.execute('SELECT id FROM clients WHERE telegram_id = ?', (name_or_telega_id,))
            client_id = cur.fetchone()
            if client_id:
                return {"values": client_id[0], "message": "Получен ID клиента", "success": True}
            else:
                return {"message": "Клиент не найден", "success": False}
        except Exception as e:
            return {"message": f"Ошибка получения ID: {e}", "success": False}

    def get_clients(self) -> Optional[List[Client]]:
        clients = []
        cur = self.conn.cursor()
        cur.execute('SELECT name, phone, telegram_id FROM clients;')
        list_clients = cur.fetchall()
        if list_clients:
            for client_data in list_clients:
                clients.append(Client(*client_data))
            return clients
        return None

    def check_telegram_id(self, telegram_id: int) -> dict:
        try:
            cur = self.conn.cursor()
            cur.execute('SELECT telegram_id FROM clients;')
            list_telegram_id = cur.fetchall()
            if (telegram_id,) in list_telegram_id:
                return {"message": f"Клиент с telegram_id: {telegram_id} уже существует в базе.", "success": False}
            return {"message": f"telegram_id: {telegram_id} нет в базе", "success": True}
        except Exception as e:
            return {"message": f"Ошибка : {e}", "success": False}