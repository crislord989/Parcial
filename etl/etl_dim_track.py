import boto3
import pandas as pd
import pymysql
import pyarrow as pa
import pyarrow.parquet as pq
import io
import os

BUCKET = 'chinook-dw-987'
PREFIX = 'warehouse/dim_track/'

conn = pymysql.connect(
    host=os.getenv('DB_HOST', '').strip(),
    user=os.getenv('DB_USER', '').strip(),
    password=os.getenv('DB_PASSWORD', '').strip(),
    database=os.getenv('DB_NAME', '').strip()
)

sql = """
SELECT 
    t.TrackId as TrackKey,
    t.Name as Name,
    al.Title as Album,
    ar.Name as Artist,
    g.Name as Genre,
    mt.Name as MediaType,
    t.Composer as Composer,
    t.Milliseconds as Milliseconds
FROM Track t
JOIN Album al ON t.AlbumId = al.AlbumId
JOIN Artist ar ON al.ArtistId = ar.ArtistId
JOIN Genre g ON t.GenreId = g.GenreId
JOIN MediaType mt ON t.MediaTypeId = mt.MediaTypeId
"""

df = pd.read_sql(sql, conn)
conn.close()

print(f'Filas: {len(df)}')

table = pa.Table.from_pandas(df)
buf = io.BytesIO()
pq.write_table(table, buf)
buf.seek(0)

s3 = boto3.client('s3')
s3.put_object(Bucket=BUCKET, Key=f'{PREFIX}dim_track.parquet', Body=buf.getvalue())
print(f'Subido a s3://{BUCKET}/{PREFIX}dim_track.parquet')
