import rekognition
import kinesis
import sys
import pprint

def info():
    
    pp = pprint.PrettyPrinter(indent=4)

    resp = rekognition.describe_stream_processor()
    print("\n\nrekognition.describe_stream_processor:\n")
    pp.pprint(resp)

    resp = kinesis.describe_stream()
    print("\n\nkinesis.describe_stream:\n")
    pp.pprint(resp)
     

def start():
    # rekognition.start_stream_processor()
    # TODO: Is there a way to start/stop kinesis streams?
    kinesis.read_stream()

def stop():
    rekognition.stop_stream_processor()

def custom():
    # FIXME: Don't know how to prevent this from blocking...
    kinesis.start_producer()

def main():
    if(len(sys.argv)<2):
        print("Please specify 'info', 'start' (which will run indefinitely) or 'stop' (to cleanup) or 'custom'")
        return
    
    cmd = sys.argv[1]
    response = eval('{}()'.format(cmd))

if __name__ == "__main__":
    main()
