import boto3

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'chinook-dw-987'

prefijos = [
    'raw/', 'warehouse/dim_customer/', 'warehouse/dim_track/',
    'warehouse/dim_date/', 'warehouse/fact_sales/',
    'scripts/', 'athena-results/', 'glue-temp/'
]

for prefix in prefijos:
    s3.put_object(Bucket=BUCKET, Key=prefix)
    print(f'Creado: {prefix}')
