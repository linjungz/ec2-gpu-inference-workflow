import boto3
import time
import logging
from botocore.exceptions import ClientError

#Test
#Set up logging
logger = logging.getLogger('worker')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('worker.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

queue_url = "https://sqs.cn-northwest-1.amazonaws.com.cn/402202783068/Glint-Demo-GPUJobQueue"
sqs = boto3.client('sqs')

def main():
    while True:
        #Get message
        print("output")
        logger.debug("Ready to receive message")
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=120,
            WaitTimeSeconds=10
        ) 
        
        logger.debug(response)
        if 'Messages' in response:
            #TODO: add asg scale-in protection
            #Received message
            for msg in response['Messages']:
                #Start processing the messages
                logger.info('Received message {} {}'.format(msg['MessageId'], msg['Body']))
                #wait for a while for processing
                logger.debug("Processing message")
                time.sleep(60)

                #delete message from queue
                receipt_handle = msg['ReceiptHandle']
                sqs.delete_message(
                    QueueUrl = queue_url,
                    ReceiptHandle=receipt_handle
                )
                logger.info("Message {} deleted from queue".format(msg['MessageId']))
        else:
            logger.info('No message. Put worker to sleep for a while...')
            time.sleep(5)

if __name__ == '__main__':
    logger.info("Now running")
    main()
