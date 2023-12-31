import boto3
import dotenv
import os 
import logging

logging.basicConfig(filename='app.log', filemode='a+', format='%(name)s - %(levelname)-8s - %(message)s')
logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)

dotenv.load_dotenv()


#Create S3 Client instance
try:
    bucket_name = os.environ.get('BUCKET_NAME')
    s3 = boto3.client('s3', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )
    logger.info("S3 client created")
except Exception as e:
    logger.error(e)


# List all files in the bucket
def list_files_in_bucket():
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)

        if 'Contents' in response:
            #If 'Content' in responsse, return an array of dict, where each file would be numbered incrementally, where each dict contains name of the file, last motified date and size of the file
            files = []
            for obj in response['Contents']:
                #If the size is less than 1 mb, represent it in KB, else in MB else if smaller than 1kb, in bytes
                if obj['Size'] < 1000:
                    size = str(obj['Size']) + ' bytes'
                elif obj['Size'] < 1000000:
                    size = str(round(obj['Size']/1000, 2)) + ' KB'
                else:
                    size = str(round(obj['Size']/1000000, 2)) + ' MB'

                files.append({
                    'id': len(files) + 1, #Incremental id
                    'name': obj['Key'],
                    'last_modified': str(obj['LastModified']).split(' ')[0],
                    'size': size
                })
            logger.info("Files returned successfully")
            return files
        else:
            logger.warning("No objects found in the bucket.")
            return []
    except Exception as e:
        logger.error("Error: " + str(e))
        return []
    

def download_file_from_s3(filename):
    s3.download_file(bucket_name, filename, 'cache/' + filename)
    logger.info("File downloaded from S3")
    return 


def upload_file_to_s3(file_obj, file_name):
    s3.upload_fileobj(file_obj, bucket_name, file_name)
    logger.info("File uploaded to S3")
    return 


