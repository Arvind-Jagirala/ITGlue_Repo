README file:
NOTE : This task can be achieved in different ways. I have built this application by using two approaches using the tech stack - Jenkins, Ansible, Docker, Git, AWS CloudFormation.
Prerequisites for both the approaches:
AWS CLI Installed and Configured on the server from where you execute CLoudFormation template.
Aws configured with access key and passphrase key of the user with Administrator access.
Create key pairs or use an existing one in the same region as resource stack( like ca-central-1) which will be passed into CloudFormation template creation. 
Postman setup to test the file upload functionality to S3 bucket.

Approach-1 : 

High-level steps involved:
Run the CloudFormation template provided to provision resources. It has the startup scripts defined within the template as userdata which deploys and starts the application.
Test the functionality using Postman body ‘GET’ and ‘POST’ methods. It  uploads the files to S3 and responds back with an URL link to access the file.
Detailed steps to perform:
Run the CloudFormation template(cfscript.yml) provided in Git repo from the AWS CLI using the below command by replacing the highlighted key-value with yours.
   	# aws cloudformation create-stack --stack-name ec2-stack --template-body file://cfscript.yml --parameters ParameterKey=Key,ParameterValue=Test_Ec2_Private
After the Ec2 is spinned up by CloudFormation template, connect to it and check the logs (tail -500f /var/log/messages) to validate that the cloud-init script is completed. This will take about 10 minutes to install the docker, build the image, deploy  and start the application. Use below commands to check the image created and running container.
# docker images
# docker ps
Once the docker container is up and running you should be able to upload the files to S3. Do this exercise through the postman body by calling the “GET” and “POST” methods to test the ‘files upload’ to S3 bucket as per the requirement by passing the public ip as below. 
For “GET” - Application endpoint ip i.e; http://35.182.155.44
For “POST” - Application endpoint ip i.e; http://35.182.155.44/upload 
“GET” method screenshot

“POST” method screenshot

Upload success screenshot

Access link screenshot


Approach-2 :

High-level steps involved:
Provision Infrastructure on AWS using CloudFormation template.
Run Jenkins pipeline job to install Docker and deploy applications using Ansible.
Test the functionality using Postman body ‘GET’ and ‘POST’ methods to upload the files to S3 and respond back with an URL link to access the file.
Pre-requisites: 
In addition to the above mentioned prerequisites, we need a Jenkins server with Ansible installed in it that runs a pipeline job to deploy the application in the Application server created by cloudformation..
Detailed steps to perform:
Provision of resources is done by CloudFormation. Run the CloudFormation template(cloudformationtemplate.yml) provided in Git repo from the AWS CLI using the below command by replacing the highlighted key-value with yours.
   	# aws cloudformation create-stack --stack-name ec2-stack --template-body file://cloudformationtemplate.yml --parameters ParameterKey=Key,ParameterValue=Test_Ec2_Private

Note: Before running the above command, replace the public key mentioned under userdata in cloudformationtemplate.yml with your ansible server’s public key.
Once the Ec2 is spinned up by CloudFormation template, connect to it and check the logs (tail -500f /var/log/messages) to validate that the cloud-init script is completed. 
Application deployment is done by Jenkins. Open Jenkins url and create a pipeline job with github url as https://github.com/Arvind-Jagirala/ITGlue_Repo.git which has all the source code, required files and a pipeline script named “Jenkinsfile”.
After configuring the job, run it by clicking “Build with Parameters” and provide the public ip of the instance created by cloudformation and run the build.           



The above screenshot says “Finished:Aborted” because the job was aborted after it ran the final step. This is the workaround to avoid the job from running endlessly and needs to be fixed with something like running the application in detached/background mode to keep the session alive and application running.
The application takes 5-7 mins to be accessible. Once the docker container is up and running you should be able to upload the files to S3 using postman as mentioned in Approach 1. 
            For “GET” - Application endpoint ip i.e; http://3.99.31.81
For “POST” - Application endpoint ip i.e; http://3.99.31.81/upload 
