import os
from pathlib import Path
import pandas as pd

def load_tables():


    ##### LOAD THE RAW DATA #####
    df = pd.DataFrame()
    parent = Path(__file__).parent.parent
    DATA_DIR = os.path.join(parent, 'data')
    WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    for f in os.listdir(DATA_DIR):
        if f.endswith('.csv') and '20210201' not in f:
            in_file = os.path.join(DATA_DIR, f)
            df = df.append(pd.read_csv(in_file, parse_dates=['Date Time (UTC)']))

    df = df.reset_index().drop('index', axis=1)
    df = df[df['DEX'] == 'Uniswap v2']
    weekday_map = dict(enumerate(WEEKDAYS, start=1))
    df['Weekday'] = df['Date Time (UTC)'].apply(lambda row: weekday_map[row.isoweekday()])
    df['Hour'] = df['Date Time (UTC)'].dt.hour
    df['Weekday + Hour'] = df['Weekday'] + '-' + df['Hour'].astype(str)
    
    ##### AGGREATE BY WEEKDAY #####
    weekday_df = pd.DataFrame()
    weekday_df = weekday_df.append(df[df['Token (In)'] == ' HOPR'].groupby('Weekday').sum()[['Amount (In)']])
    weekday_df = weekday_df.join(df[df['Token (Out)'] == ' HOPR'].groupby('Weekday').sum()[['Amount (Out)']])
    weekday_df['Volume (HOPR)'] = weekday_df['Amount (In)'] + weekday_df['Amount (Out)']
    weekday_df = weekday_df.loc[WEEKDAYS]
    weekday_df['Weekday'] = weekday_df.index
    transaction_count = [len(df[df['Weekday'] == day]) for day in WEEKDAYS]
    weekday_df['Transaction Count'] = transaction_count
    
    ##### AGGREATE BY HOUR #####
    hour_df = pd.DataFrame()
    hour_df = hour_df.append(df[df['Token (In)'] == ' HOPR'].groupby('Hour').sum()[['Amount (In)']])
    hour_df = hour_df.join(df[df['Token (Out)'] == ' HOPR'].groupby('Hour').sum()[['Amount (Out)']])
    hour_df['Volume (HOPR)'] = hour_df['Amount (In)'] + hour_df['Amount (Out)']
    hour_df['Hour'] = hour_df.index
    transaction_count = [len(df[df['Hour'] == hour]) for hour in hour_df.index]
    hour_df['Transaction Count'] = transaction_count
    
    ##### AGGREATE BY WEEKDAY AND HOUR #####
    day_hour_df = pd.DataFrame()
    day_hour_df = day_hour_df.append(df[df['Token (In)'] == ' HOPR'].groupby('Weekday + Hour').sum()[['Amount (In)']])
    day_hour_df = day_hour_df.join(df[df['Token (Out)'] == ' HOPR'].groupby('Weekday + Hour').sum()[['Amount (Out)']])
    day_hour_df['Volume (HOPR)'] = day_hour_df['Amount (In)'] + day_hour_df['Amount (Out)']
    idx = []
    for weekday in WEEKDAYS:
        for hour in sorted(df['Hour'].unique()):
            idx.append(weekday + '-' + str(hour))
    day_hour_df['Weekday + Hour'] = idx
    transaction_count = [len(df[df['Weekday + Hour'] == entry]) for entry in day_hour_df['Weekday + Hour']]
    day_hour_df['Transaction Count'] = transaction_count
    weekdays = [s.split('-')[0] for s in day_hour_df['Weekday + Hour']]
    hours = [s.split('-')[1] for s in day_hour_df['Weekday + Hour']]
    day_hour_df['Weekday'] = weekdays
    day_hour_df['Hour'] = hours
    
    return df, weekday_df, hour_df, day_hour_df


if __name__ == '__main__':
    df, weekday_df, hour_df, day_hour_df = load_tables()
