import boto3
import pandas as pd
import holidays
import pyarrow as pa
import pyarrow.parquet as pq
import io

BUCKET = 'chinook-dw-987'
PREFIX = 'warehouse/dim_date/'

def generate_dim_date(start='2000-01-01', end='2030-12-31'):
    co_holidays = holidays.Colombia(years=range(2000, 2031))
    us_holidays = holidays.US(years=range(2000, 2031))
    all_holidays = {**co_holidays, **us_holidays}
    
    dates = pd.date_range(start=start, end=end, freq='D')
    df = pd.DataFrame({'FullDate': dates})
    
    df['DateKey']   = df['FullDate'].dt.strftime('%Y%m%d').astype(int)
    df['Year']      = df['FullDate'].dt.year
    df['Quarter']   = df['FullDate'].dt.quarter
    df['Month']     = df['FullDate'].dt.month
    df['MonthName'] = df['FullDate'].dt.strftime('%B')
    df['Day']       = df['FullDate'].dt.day
    df['DayOfWeek'] = df['FullDate'].dt.dayofweek + 1
    df['DayName']   = df['FullDate'].dt.strftime('%A')
    df['IsHoliday'] = df['FullDate'].dt.date.apply(
        lambda d: 1 if d in all_holidays else 0
    )
    df['FullDate']  = df['FullDate'].dt.strftime('%Y-%m-%d')
    return df[['DateKey','FullDate','Year','Quarter','Month',
               'MonthName','Day','DayOfWeek','DayName','IsHoliday']]

def upload_to_s3(df, bucket, prefix):
    table = pa.Table.from_pandas(df)
    buf = io.BytesIO()
    pq.write_table(table, buf)
    buf.seek(0)
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket, Key=f'{prefix}dim_date.parquet',
                  Body=buf.getvalue())
    print(f'Subido a s3://{bucket}/{prefix}dim_date.parquet')

if __name__ == '__main__':
    print('Generando DimDate...')
    df = generate_dim_date()
    print(f'Filas generadas: {len(df)}')
    upload_to_s3(df, BUCKET, PREFIX)
    print('DimDate completado.')
