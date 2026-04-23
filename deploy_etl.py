import boto3
import subprocess
import sys

BUCKET = 'chinook-dw-987'

scripts = [
    'etl/etl_dim_date.py',
    'etl/etl_dim_track.py',
    'etl/etl_fact_sales.py',
]

s3 = boto3.client('s3')

for script in scripts:
    name = script.split('/')[-1]
    s3.upload_file(script, BUCKET, f'scripts/{name}')
    print(f'Subido: {name}')
    result = subprocess.run(['python3.11', script], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        sys.exit(1)
    print(f'{name} ejecutado OK')

print('ETL completo.')
