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
ENV DB_HOST=51.159.75.72
ENV DB_PORT=3636
ENV DB_NAME=jira
ENV DB_USER=jira
ENV DB_PASSWORD=jira&Samou123

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
