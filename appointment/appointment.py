from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional


class Service:
    def __init__(self, name: str, cost: int, duration: int = 1):
        self.name: str = name
        self.duration: int = duration
        self.cost: int = cost

    def __repr__(self):
        return self.name


class Master:
    def __init__(self, master_id: int, name: str, specialties: List[str]):
        self.master_id: int = master_id
        self.name: str = name
        self.specialties: List[str] = specialties
        self.schedule: Dict[Any, Any] = {}

    def __repr__(self):
        return self.name

    def get_month_free_hours_dict(self, start=10, end=21, slot=90, year=None, month=None) -> None:
        now = datetime.now()
        year = year or now.year
        month = month or now.month

        # Находим первый день месяца
        first_day = datetime(year, month, 1)
        # Находим первый день следующего месяца
        if month == 12:
            next_month = datetime(year + 1, 1, 1)
        else:
            next_month = datetime(year, month + 1, 1)

        day = first_day
        while day < next_month:
            slot_time = day.replace(hour=start, minute=0, second=0, microsecond=0)
            end_time = day.replace(hour=end, minute=0, second=0, microsecond=0)
            while slot_time < end_time:
                key = slot_time.strftime("%Y-%m-%d %H:%M")
                self.schedule[key] = True
                slot_time += timedelta(minutes=slot)
            day += timedelta(days=1)

    def is_available(self, appointment_time: datetime) -> bool:
        dt_form = appointment_time.strftime("%Y-%m-%d %H:%M")
        return self.schedule.get(dt_form, False)

    def book_time(self, appointment_time: datetime) -> None:
        dt_form = appointment_time.strftime("%Y-%m-%d %H:%M")
        self.schedule[dt_form] = False

    def cancel_time(self, appointment_time: datetime) -> None:
        dt_form = appointment_time.strftime("%Y-%m-%d %H:%M")
        if dt_form in self.schedule:
            self.schedule[dt_form] = True


class Client:
    def __init__(self, name: str, phone: str):
        self.name: str = name
        self.phone: str = phone
        self.appointments: List[Appointment] = []

    def __repr__(self):
        return self.name

    def add_appointment(self, appointment: 'Appointment') -> None:
        self.appointments.append(appointment)

    def get_appointments(self) -> List['Appointment']:
        return self.appointments


class Appointment:
    def __init__(
            self,
            appointment_time: datetime,
            master: Master,
            client: Client,
            service: Service,
            description: str = ''
    ):
        self.appointment_time: datetime = appointment_time
        self.master: Master = master
        self.client: Client = client
        self.service: Service = service
        self.description: str = description
        self.confirmed: bool = False

    def confirm(self):
        self.confirmed = True

    def cancel(self):
        self.confirmed = False


class Salon:
    def __init__(self, name: str):
        self.name: str = name
        self.clients: List[Client] = []
        self.masters: List[Master] = []
        self.appointments: List[Appointment] = []
        self.services: List[Service] = []

    HAIRDRESER = 'Парикмахер'

    def create_master(self, master_id: int, master_name: str, specialties: List[str]) -> Master:
        master = Master(master_id, master_name, specialties)
        self.add_master(master)
        return master

    def add_master(self, master: Master) -> None:
        self.masters.append(master)

    def find_master(self, time: datetime, specialty: Service, master: Master = None):
        for m in self.masters:
            if (
                    (master is None or m == master)
                    and specialty in m.specialties
                    and m.is_available(time)
            ):
                return m
        return None

    def add_client(self, client: Client) -> None:
        self.clients.append(client)

    def book_appointment(
            self,
            service: Service,
            master: Master,
            client: Client,
            appointment_time: datetime,
            description: str = ''
    ):
        free_master = self.find_master(appointment_time, service, master)
        if not free_master:
            return None
        appointment = Appointment(appointment_time, master, client, service, description)
        self.appointments.append(appointment)
        client.add_appointment(appointment)
        master.book_time(appointment_time)
        return appointment
