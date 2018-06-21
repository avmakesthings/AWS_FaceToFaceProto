import boto3
import pprint
import time
import threading

client = boto3.client(
    'kinesis',
)

verbose = False #TODO: Make an environment variable? Use Logger?
streamName = "test"

kinesisVideoStreamArn = "arn:aws:kinesisvideo:us-west-2:828973683334:stream/test/1529284848830"
kinesisDataStreamArn = "arn:aws:kinesis:us-west-2:828973683334:stream/AmazonRekognition_FaceToFace"

#TODO Wrap c++ producer stuff as well...

def log(o):
    if verbose:
        pp = pprint.PrettyPrinter(indent=4)
        return pp.pprint(o)

def list_streams():
    response = client.list_streams(
        Limit=123
    )
    log(response)
    return response

def describe_stream():
    response = client.describe_stream(
        StreamName=streamName,
    )
    log(response)
    return response

class ReadShard (threading.Thread):

    def setShard(self, stream_out, shard_id):
        self.stream_out = stream_out
        self.shard_id = shard_id
        return self

    def run (self):
        resp = client.get_shard_iterator(
            StreamName=streamName,
            ShardId=self.shard_id,
            ShardIteratorType='LATEST'
        )
        next_shard_iterator = resp["ShardIterator"]

        while True:
            resp = client.get_records(
                ShardIterator=next_shard_iterator,
                Limit=123
            )
            records = resp["Records"]
            for i in range (len(records)):
                self.stream_out.append(records[i])

            next_shard_iterator = resp["NextShardIterator"]
            if len(records) == 0:
                time.sleep(1)

# Blocks forever, reading from a stream
def read_stream():
    resp = describe_stream()
    shards = resp["StreamDescription"]["Shards"]
    
    stream_out = []

    for i in range (len(shards)):
        t = ReadShard()
        t.daemon = True
        t.setShard(stream_out, shards[i]["ShardId"]).start()

    pp = pprint.PrettyPrinter(indent=4)
    while True:
        for i in range(len(stream_out)):
            pp.pprint(stream_out[i])

        del stream_out[:]
        time.sleep(1) 
