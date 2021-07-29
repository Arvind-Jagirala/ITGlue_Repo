This repo contains the source code of the webapp written using python flask which uploads the files to S3 and responds with the public url. It also has the Cloudformation template for spinning resources on AWS along with ansible playbook and jenkins pipeline script for ci/cd. The given task can be achieved in different ways. I have built this application by using two approaches using the tech stack - Jenkins, Ansible, Docker, Git, AWS CloudFormation.

**Prerequisites for both the approaches:**
1. AWS CLI Installed and Configured on the server from where you execute CLoudFormation template.
2. Aws configured with access key and passphrase key of the user with Administrator access.
3. Create key pairs or use an existing one in the same region as resource stack( like ca-central-1) which will be passed into CloudFormation template creation. 
4. Postman setup to test the file upload functionality to S3 bucket.

**Approach-1 : **
**High-level steps involved:**
1. Run the CloudFormation template provided to provision resources. It has the startup scripts defined within the template as userdata which deploys and starts the application.
2. Test the functionality using Postman body ‘GET’ and ‘POST’ methods. It  uploads the files to S3 and responds back with an URL link to access the file.
**Detailed steps to perform:**
1. Run the CloudFormation template(cfscript.yml) provided in Git repo from the AWS CLI using the below command by replacing with your key-value.
   	
      >aws cloudformation create-stack --stack-name ec2-stack --template-body file://cfscript.yml --parameters ParameterKey=Key,ParameterValue=Test_Ec2_Private
      ![stack-creation](https://user-images.githubusercontent.com/33229776/127478053-0e087f79-8709-454d-8a7d-c9c081d3dc50.jpeg)

2. After the Ec2 is spinned up by CloudFormation template, connect to it and check the logs (tail -500f /var/log/messages) to validate that the cloud-init script is completed. This will take about 10 minutes to install the docker, build the image, deploy  and start the application. Use below commands to check the image created and running container.
   To check docker images:
   
      >docker images

   To check docker containers:
   
      >docker ps
      
3. Once the docker container is up and running you should be able to upload the files to S3. Do this exercise through the postman body by calling the “GET” and “POST” methods to test the ‘files upload’ to S3 bucket as per the requirement by passing the public ip as below. 
     For “GET” - Application endpoint ip i.e; http://35.182.155.44
     For “POST” - Application endpoint ip i.e; http://35.182.155.44/upload 
“GET” method screenshot
![GET](https://user-images.githubusercontent.com/33229776/127474286-ab10ef23-a5d0-4e24-aeee-68a824966c69.jpeg)

“POST” method screenshot
![POST](https://user-images.githubusercontent.com/33229776/127474335-273423a4-ca4a-47cc-9202-125d954fd7ac.jpeg)

Upload success screenshot
![upload_success](https://user-images.githubusercontent.com/33229776/127474366-384fbd66-729e-4a4a-8ae3-0fbf111f8b3c.jpeg)

Access link screenshot
![access_link](https://user-images.githubusercontent.com/33229776/127474382-aeb89fee-d35e-4d15-986a-6027363745bc.jpeg)


**Approach-2 :**
**High-level steps involved:**
1. Provision Infrastructure on AWS using CloudFormation template.
2. Run Jenkins pipeline job to install Docker and deploy applications using Ansible.
3. Test the functionality using Postman body ‘GET’ and ‘POST’ methods to upload the files to S3 and respond back with an URL link to access the file.
****Pre-requisites: ****
In addition to the above mentioned prerequisites, we need a Jenkins server with Ansible installed in it that runs a pipeline job to deploy the application in the Application server created by cloudformation..
**Detailed steps to perform:**
1. Provision of resources is done by CloudFormation. Run the CloudFormation template(cloudformationtemplate.yml) provided in Git repo from the AWS CLI using the below command by replacing with your key-value.
   	
      >aws cloudformation create-stack --stack-name ec2-stack --template-body file://cloudformationtemplate.yml --parameters ParameterKey=Key,ParameterValue=Test_Ec2_Private

**Note:** Before running the above command, replace the public key mentioned under userdata in cloudformationtemplate.yml with your ansible server’s public key.
2. Once the Ec2 is spinned up by CloudFormation template, connect to it and check the logs (tail -500f /var/log/messages) to validate that the cloud-init script is completed. 
3. Application deployment is done by Jenkins. Open Jenkins url and create a pipeline job with github url as https://github.com/Arvind-Jagirala/ITGlue_Repo.git which has all the source code, required files and a pipeline script named “Jenkinsfile”.
4. After configuring the job, run it by clicking “Build with Parameters” and provide the public ip of the instance created by cloudformation and run the build.           
![jenkins_pipeline](https://user-images.githubusercontent.com/33229776/127475753-69d00775-4cf0-42c7-b9ab-40f00deb553d.jpeg)

![job_finished](https://user-images.githubusercontent.com/33229776/127475793-47a5e573-2201-4ac7-a302-4f2ca7bc3963.jpeg)


5. The above screenshot says “Finished:Aborted” because the job was aborted after it ran the final step. This is the workaround to avoid the job from running endlessly and needs to be fixed with something like running the application in detached/background mode to keep the session alive and application running.
6. The application takes 5-7 mins to be accessible. Once the docker container is up and running you should be able to upload the files to S3 using postman as mentioned in Approach 1. 
       For “GET” - Application endpoint ip i.e; http://3.99.31.81
       For “POST” - Application endpoint ip i.e; http://3.99.31.81/upload 


**Deleting the Stack:**
For Approach 1, use below command to delete the resource stack

>aws cloudformation delete-stack --stack-name ec2-stack --template-body file://cfscript.yml --parameters ParameterKey=Key,ParameterValue=Test_Ec2_Private

For Approach 2, use below command to delete the resource stack

>aws cloudformation delete-stack --stack-name ec2-stack --template-body file://cloudformationtemplate.yml --parameters ParameterKey=Key,ParameterValue=Test_Ec2_Private


