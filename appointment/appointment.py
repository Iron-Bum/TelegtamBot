from datetime import datetime, timedelta


class Service:
    def __init__(self, name: str, cost: str, duration: str = '1'):
        self.name = name
        self.duration = duration
        self.cost = cost


class Master:
    def __init__(self, name: str, specialties: list):
        self.name = name
        self.specialties = specialties
        self.schedule = {}

    def get_month_free_hours_dict(self, start=10, end=21, slot=90, year=None, month=None):
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

    def is_available(self, appointment_time: datetime):
        dt_form = appointment_time.strftime("%Y-%m-%d %H:%M")
        return self.schedule.get(dt_form, False)

    def book_time(self, appointment_time: datetime):
        dt_form = appointment_time.strftime("%Y-%m-%d %H:%M")
        self.schedule[dt_form] = False

    def cancel_time(self, appointment_time: datetime):
        dt_form = appointment_time.strftime("%Y-%m-%d %H:%M")
        if dt_form in self.schedule:
            self.schedule[dt_form] = True


class Client:
    def __init__(self, name: str, phone: str):
        self.name = name
        self.phone = phone
        self.appointments = []

    def add_appointment(self, appointment):
        self.appointments.append(appointment)

    def view_appointments(self):
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
        self.appointment_time = appointment_time
        self.master = master
        self.client = client
        self.service = service
        self.description = description
        self.confirmed = False

    def confirm(self):
        self.confirmed = True

    def cancel(self):
        self.confirmed = False


class Salon:
    def __init__(self, name: str):
        self.name = name
        self.clients = []
        self.masters = []
        self.appointments = []

    def add_master(self, master: Master):
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

    def add_client(self, client: Client):
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


