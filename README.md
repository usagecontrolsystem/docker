Docker
In our project we have 2 distinct webservices, one is the UsageControl, the other the PEP. 

Thus, for each of the two service we have provided a distinct Dockerfiles with the following content: https://github.com/usagecontrolsystem/docker/blob/master/docker_ucs/Dockerfile

We start from a clean ubuntu machine, we install java and other required software. After all these pre-steps, we copy the folders containing the values for pips and the required jars plus the application.properties, and we open the port in order to access the webservices from remote endpoint and that's it. 

In order to launch both services at the same time, we exploited docker-compose capabilities. Hence we wrote a docker-compose.yaml file as follows: 

version: '3'
services:
 ucs:
   build: docker_ucs/
   ports:
     - "9998:9998"
   networks:
     backend:
       ipv4_address: 10.0.0.3
 pep:
   build: docker_pep/
   ports:
     - "9999:9999"
   networks:
     backend:
       ipv4_address: 10.0.0.5
networks:
 backend:
   ipam:
    config:
      - subnet: 10.0.0.0/16

where we specify the folder in which we have stored the Dockerfile and the desired port mapping. Plus we have also to set up the network in order to allow the PEP and the UCS to communicate between each other. 

Folllowing this approach it would be possible to run multiple instances of the various components, if they are mapped to a different port. 

To launch the docker-compose, it is sufficient to run the command docker-compose up -d where the -d is used for detach mode in order not to login into the container itself. 

Jenkins
In order to integrate the docker compose inside jenkins, we created a freestyle project in jenkins where in the Pipeline section we write the following https://github.com/usagecontrolsystem/docker/blob/master/jenkins-pipeline: 

Where in the checkout phase we retrieve the code from the github project, in the compile phase we compile the code using Maven and then copy the generated jars inside the folders where we have the proper Dockerfile. 

In the build phase we call docker_compose in order to build the 2 Dockers. 

In the test phase we launch the integration tests written in python so to verify taht the code is still working properly. 

Local site
To perform the same steps in the local machine, these are the steps to be done: 

1) Assume we have a folder named ~/ucs
2) clone/pull the modifications from both repositories, https://github.com/usagecontrolsystem/docker and https://github.com/usagecontrolsystem/usagecontrolsystem so to have in our ucs folder 2 subfolders: docker and usagecontrolsystem
3) Go inside the usagecontrolsystem folder and launch Maven compilation and jar creation:
\ta. [cd usagecontrolsystem]
\tb. [mvn install -DskipTests]
4) Go inside the docker folder and copy the generated jars from UCSRest and PEPRest inside docker_ucs and docker_pep repsectively: 
\ta. [cd ../docker] 
\tb. [cp ../usagecontrolsystem/UsageControlFramework/target/UCSRest-x.x.x-y.jar docker_ucs/ucs.jar] 
\tc. [cp ../usagecontrolsystem/PEPRest/target/PEPRest-x.x.x-y.jar docker_pep/pep.jar] 
5) Create and launch both docker containers using docker compose
a. [docker-compose up]
6) You will see now 2 docker containers running that have binded ports 9998 and 9999 as written above. If you have other webservices running on those port feel free to change the port numbers in Dockerfile in docker_ucs and docker_pep directories respectively.
7) If you want you can now launch the tests written inside the dockerTest folder: 
[cd dockerTests]
[python3 IntegrationTest.py]
[python3 IntegrationTestWithRevoke.py]
8) Finally, in order to start from a clean environment at every execution, you can use the docker rmi to remove the just created images.
