import boto3
import subprocess
import sys
import os

BUCKET = 'chinook-dw-987'

s3 = boto3.client('s3')

# Solo subir y ejecutar DimDate (no necesita RDS)
script = 'etl/etl_dim_date.py'
name = 'etl_dim_date.py'
s3.upload_file(script, BUCKET, f'scripts/{name}')
print(f'Subido: {name}')
result = subprocess.run(['python3.11', script], capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print(result.stderr)
    sys.exit(1)
print(f'{name} ejecutado OK')

# Subir los otros scripts a S3 (se ejecutan desde Back_P1)
for script in ['etl/etl_dim_track.py', 'etl/etl_fact_sales.py']:
    name = script.split('/')[-1]
    s3.upload_file(script, BUCKET, f'scripts/{name}')
    print(f'Subido a S3: {name}')

print('ETL pipeline completado.')
