from appointment.appointment import Service, Master, Appointment, Salon, Client
from datetime import datetime

alla = Client('Алла', '+79265550077')

haircut = Service('стрижка', '1500')
coloring = Service('покраска', '4500')

home_salon = Salon('На дому')
home_salon.create_master(1,'Инна', ['haircut'])
home_salon.add_client(alla)

dt1 = datetime(2025, 6, 1, 10)
dt5 = datetime(2025, 6, 1, 11, 30)
# inna.book_time(dt1)
# inna.cancel_time(dt5)


