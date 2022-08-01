from datetime import timedelta, datetime, date

def get_data_formatada():
    data = date.today()
    data = data.strftime('%d/%m/%Y')
    return data

def get_data():
    return date.today()