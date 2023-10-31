from datetime import datetime, timedelta


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def fill_missing_dates(labels, dataset, start_date, end_date, group_type):
    if group_type == "day":
        full_dates = list(daterange(start_date, end_date))
    elif group_type == "month":
        full_dates = [datetime(start_date.year, m, 1) for m in
                      range(start_date.month, end_date.month + 1)]
    elif group_type == "hour":
        full_dates = []
        current_time = start_date
        while current_time <= end_date:
            full_dates.append(current_time)
            current_time += timedelta(hours=1)

    full_dataset = [0] * len(full_dates)

    for i, dt in enumerate(full_dates):
        if dt.strftime('%Y-%m-%dT%H:%M:%S') in labels:
            index = labels.index(dt.strftime('%Y-%m-%dT%H:%M:%S'))
            full_dataset[i] = dataset[index]

    return full_dates, full_dataset
