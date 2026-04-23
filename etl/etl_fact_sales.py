import boto3
import pandas as pd
import pymysql
import pyarrow as pa
import pyarrow.parquet as pq
import io
from dotenv import load_dotenv
import os

load_dotenv('/home/ec2-user/environment/backend/.env')

BUCKET = 'chinook-dw-987'
PREFIX = 'warehouse/fact_sales/'

conn = pymysql.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

sql = """
SELECT 
    i.CustomerId as CustomerKey,
    il.TrackId as TrackKey,
    CAST(DATE_FORMAT(i.InvoiceDate, '%Y%m%d') AS UNSIGNED) as InvoiceDateKey,
    NULL as EmployeeKey,
    il.Quantity as Quantity,
    il.UnitPrice as UnitPrice,
    il.Quantity * il.UnitPrice as TotalAmount,
    YEAR(i.InvoiceDate) as year,
    MONTH(i.InvoiceDate) as month,
    DAY(i.InvoiceDate) as day
FROM Invoice i
JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId
"""

df = pd.read_sql(sql, conn)
conn.close()

print(f'Filas: {len(df)}')

# Subir particionado por year/month/day
s3 = boto3.client('s3')

for (year, month, day), group in df.groupby(['year', 'month', 'day']):
    partition = group.drop(columns=['year', 'month', 'day'])
    table = pa.Table.from_pandas(partition)
    buf = io.BytesIO()
    pq.write_table(table, buf)
    buf.seek(0)
    key = f'{PREFIX}year={year}/month={month}/day={day}/data.parquet'
    s3.put_object(Bucket=BUCKET, Key=key, Body=buf.getvalue())

print(f'FactSales subido con particionamiento a s3://{BUCKET}/{PREFIX}')
