# ec2-gpu-inference-workflow

## 构建弹性伸缩的深度学习推理集群

### 背景

深度学习模型的推理常常会运行在带GPU的机器上。但由于GPU资源较为昂贵，因此在一些离线任务处理场景下面，我们会希望GPU集群可以随着任务的数量来进行弹性伸缩。简单来说，如果任务多的话，我们开启更多的GPU机器来处理，如果任务少的话，就减少一些机器。任务都处理完的话，我们甚至会希望能够将机器全部关闭，从而最大限度的节省成本。

### 整体架构 

在AWS上，我们可以考虑利用EC2的自动伸缩组(Auto Scaling Group)来构建这样一个可弹性伸缩的深度学习推理集群。

如下是整体的架构图：



架构设计的考虑点包括：

- 使用EC2 G4实例来运行模型的推理。G4实例使用了NVIDIA的T4 GPU，比较合适用在推理场景。同时，我们可以使用Spot实例，即EC2的闲置资源来节省成本
- 推理任务由前端应用发送至消息队列(SQS)，G4实例轮询消息列队并进行推理任务
- 通过自动伸缩组(Auto Scaling Group)来自动启动EC2实例并根据任务


### 参考资料

https://aws.amazon.com/blogs/compute/running-cost-effective-queue-workers-with-amazon-sqs-and-amazon-ec2-spot-instances/

asg target tracking:
https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_TargetTrackingConfiguration.html

https://docs.aws.amazon.com/cli/latest/reference/autoscaling/put-scaling-policy.html

https://docs.amazonaws.cn/en_us/autoscaling/ec2/userguide/as-using-sqs-queue.html#create-sqs-policies-cli

cloudwatch metric:
https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/publishingMetrics.html#usingDimensions

https://docs.aws.amazon.com/cli/latest/reference/cloudwatch/put-metric-data.html

step function wait for token:
https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token



https://github.com/OlafenwaMoses/ImageAI/blob/master/imageai/Prediction/README.md


