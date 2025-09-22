import sqlite3 as sq
from typing import List, Optional
from datetime import datetime
from appointment.appointment import Salon


class BookingManager:
    def __init__(self, conn: sq.Connection):
        self.conn = conn

    def add_booking(self, client_id: int, service_id: int, date: str) -> dict:
        try:
            cur = self.conn.cursor()
            cur.execute('SELECT _date_ FROM bookings WHERE _date_ = ? AND free = 0;', (date,))
            if cur.fetchall():
                return {"message": "Запись на это время уже существует.", "success": False}
            cur.execute(
                '''
                UPDATE bookings
                SET client_id = ?, service_id = ?, free = ?
                WHERE _date_ = ?
                ''',
                (client_id, service_id, False, date)
            )
            self.conn.commit()
            return {"message": "Запись добавлена.", "success": True}
        except Exception as e:
            return {"message": f"Запись не добавлена, ошибка: {e}", "success": False}

    def get_list_free_time(self, date: datetime) -> List[datetime]:
        cur = self.conn.cursor()
        date_str = date.strftime('%Y-%m-%d')
        cur.execute(
            "SELECT _date_ FROM bookings WHERE _date_ LIKE ? AND free = 1",
            (f"{date_str}%",)
        )
        results = cur.fetchall()
        free_times = []
        for row in results:
            try:
                free_times.append(datetime.strptime(row[0], "%Y-%m-%d %H:%M"))
            except Exception as e:
                print(f"Ошибка конвертации времени: {row} ({e})")
        return free_times

    def del_old_free_time(self) -> dict:
        try:
            cur = self.conn.cursor()
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
            cur.execute(
                'DELETE FROM bookings WHERE _date_ < ? AND confirmed = 0',
                (now_str,)
            )
            self.conn.commit()
            return {"message": f"Удалены старые неподтвержденные записи до {now_str}", "success": True}
        except Exception as e:
            return {"message": f"Ошибка при удалении старых записей: {e}", "success": False}
