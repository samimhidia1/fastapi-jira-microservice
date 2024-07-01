FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Set the working directory
WORKDIR /app

# Copy the application code
COPY ./app /app

# Copy the tests directory
COPY ./tests /app/tests

# Copy the requirements file
COPY ./requirements.txt /app/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

# Expose the port that the application will run on
EXPOSE 8000

# Set the PYTHONPATH environment variable to include the current working directory
ENV PYTHONPATH=/app

# Set environment variables for database connection
ENV DB_HOST=your_db_host
ENV DB_PORT=your_db_port
ENV DB_NAME=your_db_name
ENV DB_USER=your_db_user
ENV DB_PASSWORD=your_db_password

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
