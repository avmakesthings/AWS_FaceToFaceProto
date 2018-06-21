import time
import subprocess
import threading
import os
import boto3

streamName = "test" # Is this right?

# TODO: Share clients
client = boto3.client(
    'kinesis',
)

class Producer (threading.Thread):

    def run (self):
        kinesisProducerCmd = "AWS_ACCESS_KEY_ID={} AWS_SECRET_ACCESS_KEY={} ./kinesis_video_gstreamer_sample_app {}"
        kinesisProducerCmdFmt = kinesisProducerCmd.format(
            os.environ['TEMP_AWS_ACCESS_KEY_ID'], 
            os.environ['TEMP_AWS_SECRET_ACCESS_KEY'], 
            streamName
        )
        relativePath = "../amazon-kinesis-video-streams-producer-sdk-cpp/kinesis-video-native-build"
        finalCmd = "cd {}; {}".format(relativePath, kinesisProducerCmdFmt)
        # ls_output=subprocess.Popen([finalCmd], stdout=subprocess.PIPE)
        os.system(finalCmd)
        while True:
            time.sleep(1)
    

# Blocks forever, runs kinesis_producer
def start_producer():
    t = Producer()
    t.daemon = True
    t.start()