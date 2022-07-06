from datetime import timedelta


def time_converter(time: list):
    int_time = int(time[1])

    time_dict = {
        "minutes": timedelta(minutes=int_time),
        "hours": timedelta(hours=int_time),
        "days": timedelta(days=int_time),
    }

    return time_dict[time[0].lower()]
