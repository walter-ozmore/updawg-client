# Use Ubuntu as the base image
FROM ubuntu:latest

# Install Git and other necessary packages
RUN apt-get update && \
    apt-get install -y git python3 python3-pip && \
    apt-get clean

# Install required Python packages using pip
RUN pip3 install --no-cache-dir requests PyYAML

# Run UpDawg Installer
COPY ./install/docker-install.sh /root/install.sh
RUN chmod +x /root/install.sh
RUN /bin/bash /root/install.sh

# Copy over test files
COPY ./config.yaml /etc/updawg/config.yaml
COPY ./start.py /etc/updawg/start.py

# Set the working directory to where your application will run
WORKDIR /etc/updawg

# Command to start your application
CMD ["python3", "start.py"]
