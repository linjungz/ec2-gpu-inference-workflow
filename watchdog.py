import boto3
import time
from datetime import datetime


queue_url = "https://sqs.cn-northwest-1.amazonaws.com.cn/402202783068/Glint-Demo-GPUJobQueue"
sqs = boto3.client('sqs')
asg = boto3.client('autoscaling')
cw = boto3.client('cloudwatch')

def main():
    while True:
        #Get Number of Messages in SQS
        response = sqs.get_queue_attributes(
            QueueUrl = queue_url,
            AttributeNames = ['ApproximateNumberOfMessages']
        )

        msgsCnt = int(response['Attributes']['ApproximateNumberOfMessages'])
        #print(response)
        print(msgsCnt)


        #Get Number of InService Instances in ASG
        response = asg.describe_auto_scaling_groups(
            AutoScalingGroupNames = ['Glint-Demo-GPU-Workers-ASG']
        )

        instancesCnt = int(response['AutoScalingGroups'][0]['DesiredCapacity'])
        print(instancesCnt)

        if instancesCnt > 0 :
            print("Queue per instance: ", msgsCnt / instancesCnt)

            #Publish Metric
            print(datetime.now())
            response = cw.put_metric_data(
                Namespace='Glint-Demo',
                MetricData=[
                    {
                        'MetricName': 'Backlog-per-worker',
                        'Value' : msgsCnt / instancesCnt,
                        'Timestamp' : time.time()
                    }
                ]
            )
        else:
            print("No instance")
            #Publish Metric
            print(datetime.now())
            response = cw.put_metric_data(
                Namespace='Glint-Demo',
                MetricData=[
                    {
                        'MetricName': 'Backlog-per-worker',
                        'Value' : 0,
                        'Timestamp' : time.time()
                    }
                ]
            )
            
            if msgsCnt > 0 :
                # Pending job in queue and no instance in ASG. Need to start one instance to process it
                response = asg.set_desired_capacity(
                    AutoScalingGroupName = 'Glint-Demo-GPU-Workers-ASG',
                    DesiredCapacity = 1
                )
                print("Found pending job and need to start one instance to process it")

        

        time.sleep(60)


if __name__ == '__main__':
    main()