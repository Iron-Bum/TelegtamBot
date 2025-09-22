import sqlite3 as sq
from typing import List, Optional
from appointment.appointment import Salon, Master


class MasterService:
    def __init__(self, conn: sq.Connection):
        self.conn = conn

    def add_master(self, master: Master) -> dict:
        try:
            cur = self.conn.cursor()
            cur.execute(
                'INSERT INTO masters(name, specialties) VALUES (?, ?)',
                (master.name, master.specialties)
            )
            self.conn.commit()
            return {"message": "Мастер добавлен", "success": True}
        except Exception as e:
            return {"message": f"Ошибка при добавлении мастера: {e}", "success": False}

    def get_masters(self) -> Optional[List[Master]]:
        masters = []
        cur = self.conn.cursor()
        cur.execute('SELECT id, name, specialties FROM masters;')
        rows = cur.fetchall()
        for row in rows:
            master = Master(row[1], row[2])
            master.set_id(row[0])
            masters.append(master)
        return masters if masters else None

    def create_schedule(self, master_name: str) -> dict:
        try:
            master = next((m for m in self.get_masters() if m.name == master_name), None)
            if master:
                master.get_month_free_hours_dict()
                cur = self.conn.cursor()
                for key, free in master.schedule.items():
                    cur.execute(
                        'INSERT INTO bookings(master_id, _date_, free) VALUES (?, ?, ?)',
                        (master.master_id, key, free)
                    )
                self.conn.commit()
                return {"message": f"Расписание для мастера {master_name} сформировано", "success": True}
            return {"message": f"Мастера {master_name} нет в базе, попробуйте другое имя.", "success": False}
        except Exception as e:
            return {"message": f"Ошибка при создании расписания: {e}", "success": False}
