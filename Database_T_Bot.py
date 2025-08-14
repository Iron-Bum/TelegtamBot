import sqlite3 as sq
from appointment.appointment import Master, Appointment, Service, Client, Salon
from typing import List, Optional


Hom = Salon('На дому')
# Hom.sync_up()


class Database:
    def __init__(self, db_name: str):
        self.conn: Optional[sq.Connection] = None
        self.db_name: str = db_name

    def connect(self) -> None:
        try:
            self.conn = sq.connect(self.db_name)
            print('Соединение установленно')
        except Exception as e:
            print(f'Ошибка соединения {e}')

    def create_tables(self):
        cur = self.conn.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS clients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT
        ); 
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS masters(
        id  INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        specialties TEXT
        );
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS services(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        duration INT,
        price INTEGER NOT NULL DEFAULT '0.00'
        ); 
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS bookings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        master_id INT,
        _date_ TEXT NOT NULL,
        client_id INT,
        service_id INT,
        description TEXT,
        confirmed BOOL NOT NULL DEFAULT FALSE,
        free BOOL NOT NULL DEFAULT TRUE 
        );
        ''')
        self.conn.commit()

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
            print("Соединение закрыто")

    def check_name(self, name: str) -> dict:
        try:
            cur = self.conn.cursor()
            cur.execute('SELECT name FROM clients;')
            list_clients_name = cur.fetchall()
            if (name,) in list_clients_name:
                return {"message": "Клиент с таким именем уже существует.", "success": False}
            return {"message": "Имя свободно.", "success": True}
        except Exception as e:
            return {"message": f"Ошибка : {e}", "success": False}

    def check_phone(self, phone: str) -> dict:
        try:
            cur = self.conn.cursor()
            cur.execute('SELECT phone FROM clients;')
            list_phone_clients = cur.fetchall()
            if (phone,) in list_phone_clients:
                return {"message": "Клиент с таким номером уже существует.", "success": False}
            return {"message": "Номер свободен", "success": True}
        except Exception as e:
            return {"message": f"Ошибка : {e}", "success": False}

    def check_service(self, service_name: str) -> dict:
        try:
            cur = self.conn.cursor()
            cur.execute('SELECT name FROM services;')
            list_name_service = cur.fetchall()
            print(list_name_service)
            if (service_name,) in list_name_service:
                return {"message": f"Услуга {service_name} уже существует.", "success": False}
            return {"message": "Название услуги свободно", "success": True}
        except Exception as e:
            return {"message": f"Ошибка : {e}", "success": False}

    def add_master(self, name: str, specialties: str = 'Парикмахер') -> dict:
        try:
            cur = self.conn.cursor()
            cur.execute('INSERT INTO masters(name, specialties) VALUES (?, ?)', (name, specialties))
            self.conn.commit()
            print('Мастер добавлен')
            return {"message": "Мастер добавлен", "success": True}
        except Exception as e:
            print(f'Ошибка при добавлении клиента :{e}')
            return {"message": f"Ошибка при добавлении мастера: {e}", "success": False}

    def add_client(self, name: str, phone: str) -> dict:
        try:
            if self.check_phone(phone)['success']:
                cur = self.conn.cursor()
                cur.execute('INSERT INTO clients(name, phone) VALUES (?, ?)', (name, phone))
                self.conn.commit()
                print('Клиент добавлен')
                return {"message": "Клиент добавлен", "success": True}
            return {"message": f"Клиент с номером {phone} уже существует!", "success": False}
        except Exception as e:
            print(f'Ошибка при добавлении клиента :{e}')
            return {"message": f"Ошибка при добавлении клиента: {e}", "success": False}

    def update_client(self, name: str, phone: str) -> dict:
        try:
            cur = self.conn.cursor()
            cur.execute('UPDATE clients SET name = ? WHERE phone = ?', (name, phone))
            self.conn.commit()
            print('Имя клиента изменено')
            return {"message": "Имя клиента изменено", "success": True}
        except Exception as e:
            print(f'Ошибка при изменении имени :{e}')
            return {"message": f"Ошибка при изменении имени: {e}", "success": False}

    def add_service(self, name, price) -> dict:
        try:
            if self.check_service(name)['success']:
                cur = self.conn.cursor()
                cur.execute('INSERT INTO services(name, price) VALUES (?, ?)', (name, price))
                self.conn.commit()
                print('Услуга добавлена')
                return {"message": "Услуга добавлена", "success": True}
            return {"message": f"Услуга {name} уже существует!", "success": False}
        except Exception as e:
            return {"message": f"Ошибка при добавлении услуги: {e}", "success": False}

    def upd_price(self, name, price) -> dict:
        try:
            cur = self.conn.cursor()
            cur.execute('UPDATE services SET price = ? WHERE name = ?', (price, name))
            self.conn.commit()
            print('Цена изменена')
            return {"message": f"Цена {name} изменена", "success": True}
        except Exception as e:
            print(f'Ошибка при изменении цены :{e}')
            return {"message": f"Ошибка при изменении цены : {e}", "success": False}

    def get_client_id(self, name_or_phone: str) -> dict:
        try:
            cur = self.conn.cursor()
            if not name_or_phone.isdigit():
                cur.execute('SELECT id FROM clients WHERE name = ?', (name_or_phone,))
                client_id = cur.fetchone()
                if client_id:
                    print(f'ID клиента : {client_id[0]}')
                    return {
                        "values": client_id[0],
                        "message": "Получен ID по имени",
                        "success": True
                    }
            else:
                cur.execute('SELECT id FROM clients WHERE phone = ?', (name_or_phone,))
                client_id = cur.fetchone()
                if client_id:
                    print(f'ID клиента : {client_id[0]}')
                    return {
                        "values": client_id[0],
                        "message": f"Получен ID по номеру телефона",
                        "success": True
                    }
            return {"message": "Клиент не найден", "success": False}
        except Exception as e:
            return {"mesage": f"Ошибка получения ID: {e}", "success": False}

    def add_booking(self, client_id: int, service_id: int, date: str) -> None:
        try:
            cur = self.conn.cursor()
            cur.execute('SELECT _date_ FROM bookings;')
            list_booking = cur.fetchall()
            if (date,) in list_booking:
                print('Запись на это время ужу существует')
            else:
                cur.execute(
                    'INSERT INTO bookings(client_id, service_id, _date_) VALUES (?, ?, ?)',
                    (client_id, service_id, date)
                )
                self.conn.commit()
                print('Запись добавлена')
        except Exception as e:
            print(f'Запись не добавленна, ошибка :{e}')

    def get_masters(self) -> List[Master]:
        masters = []
        cur = self.conn.cursor()
        cur.execute('SELECT id, name, specialties FROM masters;')
        list_masters = cur.fetchall()
        if list_masters:
            for master in list_masters:
                val = list(master)
                masters.append(Master(val[0], val[1], val[2]))
            return masters

    def get_clients(self) -> List[Client]:
        clients = []
        cur = self.conn.cursor()
        cur.execute('SELECT name, phone FROM clients;')
        list_clients = cur.fetchall()
        if list_clients:
            for client in list_clients:
                lst = list(client)
                clients.append(Client(lst[0], lst[1]))
            return clients

    def create_schedule(self, master_name: str) -> dict:
        try:
            master = next((m for m in self.get_masters() if m.name == master_name), None)
            if master:
                master.get_month_free_hours_dict()
                print(master.schedule)
                for key, free in master.schedule.items():
                    print(master.master_id, key, free)
                    cur = self.conn.cursor()
                    cur.execute(
                        'INSERT INTO bookings(master_id, _date_, free) VALUES (?, ?, ?)',
                        (master.master_id, key, free)
                    )
                    self.conn.commit()
                print('Расписание сформировано')
                return {"message": f"Расписание для мастера {master_name} сформировано", "success": True}
            return {"message": f"Мастера {master_name} нет в базе, попробуйте другое имя. "}
        except Exception as e:
            return {"message": f"Ошибка при создании расписания: {e}", "success": False}

    def create_service(self, name: str, cost: int, duration: int = 1) -> Service:
        cur = self.conn.cursor()
        cur.execute(
            'INSERT INTO services(name, cost, duration) VALUES (?, ?, ?)',
            (name, cost, duration)
        )
        self.conn.commit()
        service = Service(name, cost, duration)
        Hom.services.append(service)
        return service





# _data_ = Database('tables.db')
# _data_.connect()
# _data_.create_tables()
# _data_.add_client('Анна', 1035)
# _data_.add_service('Стрижка', 800)
# _data_.add_booking(2, 1, '2024-03-15 14:00:00')
# _data_.close_connection()
