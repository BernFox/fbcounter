# FB Counter
============

## Building the container
-------------------------

Run the following to build the fbcounter container:
docker build -t quay.io/somespider/fbcounter .


## Running the container
------------------------

To run the container:
docker run --env-file env/local.env -v /home/core/spider/fbcounter -t quay.io/somespider/fbcounter

