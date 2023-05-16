from datetime import datetime


def base_url():
    return 'https://cloud-platform.migu.cn/#/'


def current_time():
    time = "%a %b %d %H:%M:%S %Y"
    return datetime.now().strftime(time)


def time_diff(start, end):
    time = "%a %b %d %H:%M:%S %Y"
    return datetime.strptime(end, time) - datetime.strptime(start, time)
