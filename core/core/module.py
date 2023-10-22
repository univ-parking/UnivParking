def s3_connection():
    import boto3
    from core.settings import (
        AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY,
        AWS_S3_REGION_NAME,
        AWS_STORAGE_BUCKET_NAME
        )
    try:
        # s3 클라이언트 생성
        s3 = boto3.client(
            service_name='s3',
            region_name=AWS_S3_REGION_NAME,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!")
        return s3, AWS_STORAGE_BUCKET_NAME