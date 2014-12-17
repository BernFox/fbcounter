FROM quay.io/somespider/python

# Install python dependencies
ADD 	requirements.txt /app/requirements.txt
RUN 	pip install -r /app/requirements.txt

ADD 	. /app/src/

WORKDIR /app/src

#test
#RUN echo 'TEST'

# Run app
CMD ["python", "fb_query.py"]