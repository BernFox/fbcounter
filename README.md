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
then use 'docker kill [id]'.

This must be done or else this will just stack up connections to RabbitMQ, and once the 
max connections have been made, new connections will be denied. 

-Removed the env directory, you'll need this to test locally. Or you can uncomment some lines in the code. 






Running the fbrsscounter.py script 
==================================
This script gets facebook data for all entries in a given rss feed, then outputs the data as a csv. 
Run the script like this:

./fbrsscounter.py [rss feed url] [output file name]

Example
-------

./fbrsscounter.py http://feeds.abcnews.com/abcnews/topstories abc_test


Notes
-----

When you specify the output file name, leave out ".csv", the script does it for you.