import pandas as pd
import re


def preprocess(data):
    # pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s?[APMapm]{2})?\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({
        'user_message': messages,
        'message_date': dates
    })

    # convert message_date datatype
    # df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')
    # remove weird unicode space
    df['message_date'] = df['message_date'].str.replace('\u202f', ' ', regex=True)

    # remove trailing " -"
    df['message_date'] = df['message_date'].str.replace(' -', '', regex=False)

    # now convert
    df['message_date'] = pd.to_datetime(df['message_date'], dayfirst=True, errors='coerce')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    message = []

    for msg in df['user_message']:
        split = msg.split(': ', 1)
        if len(split) == 2:
            users.append(split[0])
            message.append(split[1])
        else:
            users.append('group_notification')
            message.append(split[0])

    df['user'] = users
    df['message'] = message
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()

    return df