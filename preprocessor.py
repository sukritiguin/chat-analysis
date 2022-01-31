import re
import pandas as pd
def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    # Create a data frame with two columsn i) user_message ii) message_date
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # message_date to date time format
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M - ')
    # rename message_date to date
    df.rename(columns={'message_date': 'date'}, inplace=True)
    # df.head()
    # Total number of messages is
    # df.shape
    users = []
    messages = []
    for each_message in df['user_message']:
        pattern = '([\w\W]+?):\s'
        entry = re.split(pattern, each_message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Group_Notification')
            messages.append(entry[0])
    df['users'] = users
    df['messages'] = messages
    # drop user_message column
    df.drop(columns=['user_message'], inplace=True)
    # calculate day, month and year from date column
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    #Another Prepocessor
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str("00"))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period

    return df