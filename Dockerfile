FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME World

# Run main.py when the container launches with hot-reloading
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]