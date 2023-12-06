import os;
import psycopg2;

# cluster connection details
host = os.environ.get("REDSHIFT_HOST");
port = os.environ.get("REDSHIFT_PORT");
user = os.environ.get("REDSHIFT_USER");
password = os.environ.get("REDSHIFT_PASSWORD");
database = os.environ.get("REDSHIFT_DATABASE");

# cluster IAM role to access S3 file
iam_role = os.environ.get("REDSHIFT_IAM_ROLE");

def lambda_handler(event, context):
    table = event.get("table");
    if table is None:
        raise ValueError("Table is required");

    s3_file_url = event.get("s3_file_url");
    if s3_file_url is None:
        raise ValueError("S3 file URL is required");

    command = f"COPY \"{table}\" FROM '{s3_file_url}' IAM_ROLE '{iam_role}' FORMAT PARQUET;"

    with psycopg2.connect(host=host, port=port, user=user, password=password, database=database) as connection:
        with connection.cursor() as cursor:
            cursor.execute(command);
