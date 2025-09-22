import sqlite3 as sq
from typing import List, Optional
from appointment.appointment import Salon
from db_manager.BookingManager import BookingManager
from db_manager.ServiceManager import ServiceManager
from db_manager.ClientService import ClientService
from db_manager.MasterService import MasterService


class DataBase:
    def __init__(self, db_name: str):
        self.conn: Optional[sq.Connection] = None
        self.db_name: str = db_name

        self.salon = Salon('На дому')
        self.clients: Optional[ClientService] = None
        self.masters: Optional[MasterService] = None
        self.services: Optional[ServiceManager] = None
        self.bookings: Optional[BookingManager] = None

    def connect(self):
        try:
            self.conn = sq.connect(self.db_name)
            print('Соединение установлено')
            # Инициализируем сервисы после подключения
            self.clients = ClientService(self.conn, self.salon)
            self.masters = MasterService(self.conn)
            self.services = ServiceManager(self.conn, self.salon)
            self.bookings = BookingManager(self.conn)
        except Exception as e:
            print(f'Ошибка соединения {e}')

    def create_tables(self):
        if self.conn is None:
            raise Exception("Нет соединения с базой данных")

        cur = self.conn.cursor()
        cur.executescript('''
        CREATE TABLE IF NOT EXISTS clients(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            telegram_id INTEGER
        );
        CREATE TABLE IF NOT EXISTS masters(
            id  INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            specialties TEXT
        );
        CREATE TABLE IF NOT EXISTS services(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            duration INT,
            price INTEGER NOT NULL DEFAULT '0.00'
        );
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
        if self.conn:
            self.conn.close()
            print("Соединение закрыто")