FROM quay.io/somespider/python

# Install python dependencies
ADD 	requirements.txt requirements.txt
RUN 	pip install -r requirements.txt


# Run app
CMD ["/bin/bash", "start.sh"]