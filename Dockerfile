# The image you are going to inherit your Dockerfile from
FROM python:3.10.12
# Necessary, so Docker doesn't buffer the output and that you can see the output 
# of your application (e.g., Django logs) in real-time.
ENV PYTHONUNBUFFERED 1
# Make a directory in your Docker image, which you can use to store your source code
RUN mkdir /pms
# Set the /HMS directory as the working directory
WORKDIR /pms
# Copies from your local machine's current directory to the HMS folder 
# in the Docker image
COPY . .
# Copy the requirements.txt file adjacent to the Dockerfile 
# to your Docker image
COPY ./requirements.txt /requirements.txt
# Install the requirements.txt file in Docker image
RUN pip install -r /requirements.txt
# Create a non-system user with a home directory
RUN adduser --disabled-password --gecos "" user
USER user