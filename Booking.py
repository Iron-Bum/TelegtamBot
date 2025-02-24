from datetime import datetime, timedelta


class Booking:
    def __init__(self):
        self.date_now = datetime.now()
        self.time_block = [
            '9:00:00', '10:30:00', '12:00:00', '13:30:00', '15:00:00', '16:30:00', '18:00:00', '19:30:00', '21:00:00'
        ]

    def get_datetime_block(self, target_date):
        date_times = []
        for i in self.time_block:
            date_times.append(target_date + ' ' + i)
        return date_times

    def get_list_date(self, num_days=30, start_date=None):
        if start_date is None:
            start_date = self.date_now
        list_dates = []
        for i in range(num_days):
            new_date = start_date + timedelta(days=i)
            list_dates.append(new_date.strftime('%d-%m-%Y'))
        return list_dates


b = Booking()
dates = b.get_list_date()
#dates += b.get_list_date(3)
print(dates)
print(b.get_datetime_block(dates[17]))
