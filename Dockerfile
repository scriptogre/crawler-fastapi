FROM python:3.9-buster

# Create /code directory
RUN mkdir /code

# Set the working directory to /code for simplicity
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make the entrypoint script executable
RUN chmod +x ./entrypoint.sh

CMD ["./entrypoint.sh"]