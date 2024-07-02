# FastAPI Jira Microservice

This project implements a FastAPI-based microservice for managing work items in Jira, supporting a hierarchical structure of Epics, User Stories, Tasks, and Test Cases. It provides a robust API for efficient project management and integrates with Jira's REST API.

## Concept

The project aims to develop an AI-powered system that can assist users in managing software development projects by interacting with Jira. Users can provide high-level project ideas or features, and the system will automatically generate detailed project elements like epics, user stories, tasks, acceptance criteria, and test cases. This information will be presented to the user for validation before being pushed to Jira.

### Key Components

1. **AI-Powered Agent in Jira**:
   - **Interaction**: The AI agent communicates with users through a chat interface, interpreting natural language inputs to generate project details. The AI agent interacts with users, interprets their project ideas, and translates them into actionable project elements.
   - **Generation**: It breaks down high-level ideas into detailed project elements. It generates a structured breakdown of project tasks based on user inputs.
   - **Validation**: Before pushing data to Jira, the agent presents the generated elements to the user for review and approval. The agent provides a user-friendly interface on chatgpt for validation before pushing data to Jira.

2. **FastAPI Jira Microservice**:
   - This service handles the actual communication with Jira.
   - It manages the creation, retrieval, update, and deletion of project elements such as epics, user stories, tasks, acceptance criteria, and test cases.
   - It ensures all data is stored and traceable within a PostgreSQL database.

### Project Structure

The project is organized into a single FastAPI Jira Microservice, the AI Agent is fully managed by OpenAI.

#### FastAPI Jira Microservice

- **Endpoints**: This service provides endpoints for creating, retrieving, updating, and deleting project elements. Each endpoint corresponds to different types of project elements:
  - **Epics**: High-level functionalities or modules of the project.
  - **User Stories**: Detailed requirements derived from epics.
  - **Tasks**: Specific actions needed to complete user stories.
  - **Acceptance Criteria**: Conditions that must be met for user stories to be considered complete.
  - **Test Cases**: Tests to verify that user stories meet the acceptance criteria.

- **Database**: Uses PostgreSQL to store additional metadata and ensure traceability of all project elements.
- **Containerization**: Docker is used to ensure consistent deployment across various environments.
- **CI/CD Pipeline**: GitHub Actions automates testing and deployment to ensure smooth updates and maintenance.

## Setup and Configuration

### Prerequisites

- Python 3.9
- PostgreSQL
- Docker
- GitHub account with access to the repository

### Development Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/samimhidia1/fastapi-jira-microservice.git
   cd fastapi-jira-microservice
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Set up the PostgreSQL database:
   ```bash
   sudo -u postgres psql
   CREATE USER devin WITH PASSWORD 'password';
   CREATE DATABASE dbname;
   GRANT ALL PRIVILEGES ON DATABASE dbname TO devin;
   \q
   ```

5. Set up the PostgreSQL database schema manually.

6. Run the FastAPI application:
   ```bash
   uvicorn app.main:app --reload
   ```

### Docker Setup

1. Build the Docker image:
   ```bash
   docker build -t fastapi-jira-microservice .
   ```

2. Run the Docker container:
   ```bash
   docker run -d -p 8000:8000 fastapi-jira-microservice
   ```

### CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment. The workflow file is located at `.github/workflows/ci-cd-pipeline.yml`.

Ensure that the secrets `DOCKER_USERNAME` and `DOCKER_PASSWORD` are set up in the GitHub repository's settings.

## API Endpoints

This document provides an overview of the available API endpoints in the FastAPI Jira Microservice.

### Epics
- `POST /api/v1/epics/`: Create an Epic
- `POST /api/v1/epics/batch`: Create multiple Epics
- `GET /api/v1/epics/`: List all Epics
- `GET /api/v1/epics/{epic_id}`: Get an Epic by ID
- `PUT /api/v1/epics/{epic_id}`: Update an Epic by ID
- `DELETE /api/v1/epics/{epic_id}`: Delete an Epic by ID
- `GET /api/v1/epics/{epic_id}/stories`: List all Stories in an Epic

### Stories
- `POST /api/v1/stories/`: Create a Story
- `GET /api/v1/stories/`: List all Stories
- `GET /api/v1/stories/{story_id}`: Get a Story by ID
- `PUT /api/v1/stories/{story_id}`: Update a Story by ID
- `DELETE /api/v1/stories/{story_id}`: Delete a Story by ID

### Tasks
- `POST /api/v1/tasks/`: Create a Task
- `GET /api/v1/tasks/`: List all Tasks
- `GET /api/v1/tasks/{task_id}`: Get a Task by ID
- `PUT /api/v1/tasks/{task_id}`: Update a Task by ID
- `DELETE /api/v1/tasks/{task_id}`: Delete a Task by ID

### Test Cases
- `POST /api/v1/test_cases/`: Create a Test Case
- `GET /api/v1/test_cases/`: List all Test Cases
- `GET /api/v1/test_cases/{test_case_id}`: Get a Test Case by ID
- `PUT /api/v1/test_cases/{test_case_id}`: Update a Test Case by ID
- `DELETE /api/v1/test_cases/{test_case_id}`: Delete a Test Case by ID

- `GET /health`: Health check endpoint

## Data Models

This document describes the data models used in the FastAPI Jira Microservice.

### Issue Base Model

```python
class IssueBase(BaseModel):
    summary: str
    description: str
    project_key: str
    custom_fields: Optional[Dict] = {}
```

### Issue Create Model

```python
class IssueCreate(IssueBase):
    issuetype: str
    epic_id: Optional[str] = None
    parent_id: Optional[str] = None
```

## Deployment

The application is containerized using Docker for consistent deployment across environments.

### Dockerfile

```Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./app /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

## Advanced Features

The FastAPI Jira Microservice includes several advanced features to enhance functionality and user experience:

1. **Pagination and Filtering**: All list endpoints support pagination and filtering for efficient handling of large datasets.
2. **Search Functionality**: Users can search issues by various fields such as summary, description, or status.
3. **Batch Operations**: The API supports batch creation and updates for epics, tasks, and test cases.
4. **Custom Fields**: The system allows for flexible handling of custom fields in requests and responses.
5. **User Permissions and Roles**: Enhanced security and access control through user permissions and roles.
6. **Activity Logs**: Comprehensive tracking and logging of activities for auditing purposes.
7. **Webhooks**: Support for real-time updates and notifications through webhooks.

## Directory Structure

The project directory structure is organized as follows:

```
fastapi_jira_microservice/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── schemas.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── epics.py
│   │   ├── stories.py
│   │   ├── tasks.py
│   │   ├── test_cases.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_epics.py
├── .github/
│   ├── workflows/
│   │   ├── ci-cd-pipeline.yml
├── .env
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt
```

## Running the Project

To run the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/samimhidia1/fastapi-jira-microservice.git
   cd fastapi-jira-microservice
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Set up the PostgreSQL database:
   ```bash
   sudo -u postgres psql
   CREATE USER devin WITH PASSWORD 'password';
   CREATE DATABASE dbname;
   GRANT ALL PRIVILEGES ON DATABASE dbname TO devin;
   \q
   ```

5. Set up the PostgreSQL database schema manually.

6. Run the FastAPI application:
   ```bash
   uvicorn app.main:app --reload
   ```

## Deployment on Scaleway Serverless Container

To deploy the application on Scaleway serverless container via the container registry, follow these steps:

1. Build the Docker image:
    ```bash
    docker build -t fastapi-jira-microservice .
    ```

2. Tag the Docker image for the Scaleway container registry:
    ```bash
    docker tag fastapi-jira-microservice rg.fr-par.scw.cloud/YOUR_NAMESPACE/fastapi-jira-microservice:latest
    ```

3. Log in to the Scaleway container registry:
    ```bash
    docker login rg.fr-par.scw.cloud
    ```

4. Push the Docker image to the Scaleway container registry:
    ```bash
    docker push rg.fr-par.scw.cloud/YOUR_NAMESPACE/fastapi-jira-microservice:latest
    ```

5. Deploy the image to Scaleway serverless container:
    - Go to the Scaleway Console.
    - Navigate to the "Serverless Containers" section.
    - Create a new container and configure it to use the pushed Docker image.
    - Set the necessary environment variables and configuration options.
    - Deploy the container.

6. Access the deployed application via the provided URL.

Note: SQLAlchemy and Alembic have been removed from the project. You will need to set up the PostgreSQL database schema manually.

## Running Tests

To run the tests for the FastAPI Jira Microservice, follow these steps:

1. Ensure the PostgreSQL database is running and accessible.
2. Set the necessary environment variables for the database connection.
3. Run the tests using pytest:
    ```bash
    pytest
    ```

## Troubleshooting

### Common Issues

1. **Database Connection Issues**:
    - Ensure the PostgreSQL database is running and accessible.
    - Verify the database connection details in the environment variables.

2. **Docker Container Issues**:
    - Check the Docker container logs for any errors.
    - Ensure the Docker containers are running and properly configured.

3. **API Endpoint Errors**:
    - Verify the API endpoint URLs and request payloads.
    - Check the application logs for any errors or exceptions.

4. **Test Failures**:
    - Ensure the test data is valid and matches the expected format.
    - Check the test logs for any errors or failures.
```

Note: SQLAlchemy and Alembic have been removed from the project. You will need to set up the PostgreSQL database schema manually.

4. Set up the PostgreSQL database connection:
   - Ensure the PostgreSQL database is running and accessible.
   - Update the `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD` environment variables in the Dockerfile or `.env` file with the correct values.
   - If the database is running on the host machine, use the host's IP address instead of `host.docker.internal`.
