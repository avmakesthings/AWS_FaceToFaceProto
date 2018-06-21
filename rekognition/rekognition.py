import boto3
import pprint

client = boto3.client(
    'rekognition',
)

verbose = False #TODO: Make an environment variable? Use Logger?
streamProcessorName = "FaceToFaceStreamProcessor"
collectionID = "FaceToFaceCollection"

kinesisVideoStreamArn = "arn:aws:kinesisvideo:us-west-2:828973683334:stream/test/1529284848830"
kinesisDataStreamArn = "arn:aws:kinesis:us-west-2:828973683334:stream/AmazonRekognition_FaceToFace"
roleArn = "arn:aws:iam::828973683334:role/AmazonRekognitionMyServiceRole"


def log(o):
    if verbose:
        pp = pprint.PrettyPrinter(indent=4)
        return pp.pprint(o)

def create_collection():
    response = client.create_collection(
        CollectionId=collectionID
    )
    log(response)
    return response

def list_collections():
    response = client.list_collections(
        MaxResults=123
    )
    log(response)
    return response

def create_stream_processor():
    response = client.create_stream_processor(
        Input={
            'KinesisVideoStream': {
                'Arn': kinesisVideoStreamArn
            }
        },
        Output={
            'KinesisDataStream': {
                'Arn': kinesisDataStreamArn
            }
        },
        Name=streamProcessorName,
        Settings={
            'FaceSearch': {
                'CollectionId': collectionID,
                'FaceMatchThreshold': 0
            }
        },
        RoleArn=roleArn
    )
    log(response)
    return response

def delete_stream_processor():
    response = client.delete_stream_processor(
        Name=streamProcessorName
    )
    log(response)
    return response

def start_stream_processor():
    response = client.start_stream_processor(
        Name=streamProcessorName
    )
    log(response)
    return response

def describe_stream_processor():
    response = client.describe_stream_processor(
        Name=streamProcessorName
    )
    log(response)
    return response

def stop_stream_processor():
    response = client.stop_stream_processor(
        Name=streamProcessorName
    )
    log(response)
    return response
