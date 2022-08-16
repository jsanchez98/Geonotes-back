# Set base image (host OS)
FROM python:3.8-alpine

# By default, listen on port 5000
EXPOSE 5000

# Set the working directory in the container
WORKDIR /

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY app.db .flaskenv .gitignore config.py Dockerfile microblog.py ./

ADD App App

ADD migrations migrations

# Command to run on container start
CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0"]