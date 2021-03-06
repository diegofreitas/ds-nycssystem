__author__ = 'diego'

from datetime import datetime
import numpy as np

def compute_r_squared(data, predictions):
    mean = np.mean(data)
    r_squared = 1 - (np.sum(np.square(data-predictions)) /np.sum(np.square(data-mean)))

    return r_squared

def get_day_week(date):
    return datetime.strptime(date,'%Y-%m-%d').date().isoweekday()

def convert_hour(hour):
    if hour <= 12:
        return hour
    else:
        return hour - 12

def ampm_hour(hour):
    if hour <= 12:
        return 'am'
    else:
        return 'pm'

def normalize(values):
    return values / np.linalg.norm(values)
