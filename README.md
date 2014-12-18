FB Counter
============

Setup
-----------------------
Run the following to build the fbcounter container:

```
docker build -t quay.io/somespider/fbcounter .
docker run --env-file env/local.env -v /home/core/spider/fbcounter -t quay.io/somespider/fbcounter
```


Notes
-----

For some reason the processes doesn't die when ctrl-c or ctrl-z are used. 
You have to manually kill the docker process by using 'docker ps' to find the process id, 
then use 'docker kill -id-'.

This must be done or else this will just stack up connections to RabbitMQ, and once the 
max connections have been made, new connections will be denied. 