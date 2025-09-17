from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional


class Service:
    def __init__(self, name: str, price: int, duration: int = 1):
        self.service_id: Optional[int] = None
        self.name: str = name
        self.duration: int = duration
        self.price: int = price

    def __repr__(self):
        return f"Service(id={self.service_id}, name={self.name}, price={self.price}, duration={self.duration})"

    def set_id(self, service_id: int):
        self.service_id = service_id


class Master:
    def __init__(self, name: str, specialties: str = 'Парикмахер'):
        self.master_id: Optional[int] = None
        self.name: str = name
        self.specialties: str = specialties
        self.schedule: Dict[Any, Any] = {}

    def __repr__(self):
        return f"Master(id={self.master_id}, name={self.name}, specialties={self.specialties})"

    def set_id(self, master_id: int):
        self.master_id = master_id

    def get_month_free_hours_dict(self, start=10, end=21, slot=90, year=None, month=None) -> dict:
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
        dct = self.schedule
        return dct

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
    def __init__(self, name: str, phone: str, client_id: int):
        self.name: str = name
        self.phone: str = phone
        self.client_id: int = client_id
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

    def add_master(self, master: Master) -> None:
        self.masters.append(master)

    def find_master(self, time: datetime, specialty: str = 'Парикмахер', master: Master = None):
        for m in self.masters:
            if (
                    (master is None or m == master)
                    and specialty in m.specialties
                    and m.is_available(time)
            ):
                return m
        return None

    def add_book_master(self, time: datetime, master: Master):
        for i in self.masters:
            if i == master:
                i.book_time(time)
                return

    def cancel_book_master(self, time: datetime, master: Master):
        for i in self.masters:
            if i == master:
                i.cancel_time(time)
                return

    def add_client(self, client: Client) -> None:
        self.clients.append(client)

    def add_book_client(self, appointment: Appointment, client: Client) -> None:
        for i in self.clients:
            if i == client:
                i.add_appointment(appointment)
                return

    def book_appointment(
            self,
            service: Service,
            master: Master,
            client: Client,
            appointment_time: datetime,
            specialty: str = None,
            description: str = ''
    ) -> Optional[Appointment]:
        free_master = self.find_master(appointment_time, specialty, master)
        if not free_master:
            return None
        appointment = Appointment(appointment_time, master, client, service, description)
        self.appointments.append(appointment)
        self.add_book_client(appointment, client)
        self.add_book_master(appointment_time, master)
        return appointment

# Test


# Hom = Salon('Home')
# Inna = Master('Inna')
# Inna.get_month_free_hours_dict()
# hardress = Service('hardress', 1200)
# Anna = Client('Anna', '12345678', 777)
# time = datetime.strptime('2025-09-15 13:00', '%Y-%m-%d %H:%M')
# ap = Appointment(time, Inna, Anna, hardress)
# Hom.add_client(Anna)
# Hom.add_master(Inna)
# Hom.add_book_master(time, Inna)
# Hom.add_book_client(ap, Anna)



