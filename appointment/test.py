from appointment import Service, Master, Appointment, Salon, Client
from datetime import datetime

alla = Client('Алла', '+79265550077')

haircut = Service('стрижка', '1500')
coloring = Service('покраска', '4500')

inna = Master('Инна', [haircut])

home_salon = Salon('На дому')
home_salon.add_master(inna)
home_salon.add_client(alla)

dt1 = datetime(2025, 6, 1, 10)
dt5 = datetime(2025, 6, 1, 11, 30)
inna.get_month_free_hours_dict()
print(inna.schedule)
# inna.book_time(dt1)
# inna.cancel_time(dt5)
print(inna.is_available(dt1))
home_salon.book_appointment(haircut, inna, alla, dt1)
print(inna.is_available(dt1))
print(inna.schedule)

