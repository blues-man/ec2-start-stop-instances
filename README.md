# ec2-start-stop-instances

A small Python script using boto to auto start-stop instances on Amazon AWS EC2

## Setup

First, you need Python [Boto](https://github.com/boto/boto)

Boto is already installed in most Amazon EC2 AMIs, if you are running it elsewhere, just:

### Debian/Ubuntu

```bash
sudo apt-get install python-boto
```
### Mac OS X

```bash
sudo easy_install pip
sudo pip install boto
```

### Windows

Good luck!

## Usage:

* -O, --aws-access-key : your AWS Access Key
* -W, --aws-secret-key :your AWS Secret Key
* -r, --region: the AWS region of you instances 
* -i, --instances_id : a list of id of you instances, separated by comma
* -a, --action : start or stop
* -e, --email-alert : enable email alert, if omitted is disabled
* -h, --help : prints out an help

Example:

Start
```bash
./aws_start_stop.py -O yourAccessKey -W yourSecretKey -r eu-west-1 -i i-caf3b4be,i-deadb33f -a start
```

Stop
```bash
./aws_start_stop.py -O yourAccessKey -W yourSecretKey -r eu-west-1 -i i-c4febab3 -a stop
```

Stop and Email alert
```bash
./aws_start_stop.py -O yourAccessKey -W yourSecretKey -r eu-west-1 -i i-c4febab3 -a stop -e
```
## Use case

### Crontab 

You may want to start/stop instance at the needing, for example day/night business days with a crontab:

```bash
0 7 * * 1-5  /opt/aws_start_stop.py -O yourAccessKey -W yourSecretKey -r eu-west-1 -i i-caf3b4be,i-deadb33f -a start -e >/dev/null 2>&1
0 18 * * 1-5 /opt/aws_start_stop.py  -O yourAccessKey -W yourSecretKey -r eu-west-1 -i i-caf3b4be,i-deadb33f -a stop -e >/dev/null 2>&1
```

### AWS IAM Role

You may want to restrict the capability of starting or stopping instances to some users and some instances, this could be done by creating an AWS IAM Role for a user with a custom policy mapping the proper ARN instance as:

```yaml
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:StartInstances",
                "ec2:StopInstances"
            ],
            "Resource": [
                "arn:aws:ec2:REGION_ID:ACCOUNT_ID:instance/INSTANCE_ID1"
                "arn:aws:ec2:REGION_ID:ACCOUNT_ID:instance/INSTANCE_ID2",
            ]
        }
    ]
}
```



## Mail Notification

A mail is sent to you in order to notify about the operation status, anyway is optional by the -e flag

Fill ```mail_sender``` and ```mail_receivers``` if you want to be notified by email about operation status
SMTP server if supposed to run in localhost, please adjust with your settings if you run it elsewhere

