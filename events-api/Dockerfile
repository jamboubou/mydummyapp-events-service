# start by pulling the python image
FROM python:3.9-alpine

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy app files
COPY ./app.py /app/app.py
COPY ./config.py /app/config.py
COPY ./main.py /app/main.py

# configure the container to run in an executed manner

CMD ["ddtrace-run", "python", "main.py"]