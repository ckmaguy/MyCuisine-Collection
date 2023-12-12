# MyCuisine-Collection
MyCuisine Collection: A Flask &amp; MySQL web app for managing personal recipes. Features user accounts, recipe CRUD operations, responsive design, Docker deployment, and Selenium testing. Perfect for culinary enthusiasts and web development learners.


### Project Overview

**Project Name:** MyCuisine Collection

**Description:** A Flask & MySQL web application for managing personal recipes. It's designed for culinary enthusiasts and web developers interested in learning more about web application development, database management, and automated testing.

### Features

- **User Authentication**: Register, login
- **Recipe CRUD Operations**: Create, read, update, and delete recipes in a user-friendly interface.
- **Responsive Design**: Ensures compatibility with various devices and screen sizes.
- **Docker Deployment**: Simplifies deployment and ensures consistency across different environments.
- **Automated Testing with Selenium**: Guarantees application stability and performance.

### Technical Stack

- **Backend Framework**: Flask (Python)
- **Database**: MySQL
- **Containerization**: Docker
- **Testing**: Selenium for browser automation

### File and Directory Structure

1. **.git & .gitignore**: Version control configurations.
2. **__pycache__**: Python compiled files.
3. **app**: Core application code, including templates, static files, and Python scripts.
4. **config.py**: Application configuration settings.
5. **Docker Files**:
   - **docker-compose.yml**: Defines how Docker containers should be built and run.
   - **dockerfile**: Instructions for building the Docker image.
6. **migrations**: Database migration scripts.
7. **Web Drivers**:
   - **chrome.exe**
   - **msedgedriver.exe**: For running tests in different browsers.
8. **Virtual Environment**: **mycuisine-env** (if applicable).
9. **README.md**: Documentation file.
10. **requirements.txt**: Lists dependencies.
11. **run.py**: Entry point to run the Flask app.
12. **Testing Files**:
    - **start_test.py**
    - **test_mycuisine_db.sql**
    - **testing_config.py**
    - **tests** directory.

### Getting Started

## Installation
Clone the repository:
```bash
git clone https://github.com/ckmaguy/MyCuisine-Collection.git
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To run the application:
```bash
python run.py
```

## Testing
To run the unit tests:
```bash
python -m unittest discover -s tests -v
```

## Docker
To build and run the Docker container:
```bash
docker build -t my-cuisine-collection .
docker run -p 5000:5000 my-cuisine-collection
```

## Continuous Integration and Deployment
This project uses GitHub Actions for Continuous Integration (CI) and Continuous Deployment (CD). The CI workflow runs tests on every push and pull request to the main branch, ensuring that changes do not break the application. The CD workflow builds and pushes the Docker image to Docker Hub on pushes to the main branch.

It appears that you have provided a GitHub Actions workflow file for both Continuous Integration (CI) and Continuous Deployment (CD) for the "MyCuisine Collection" project. Let's break down the contents of these workflow files and update the README accordingly.

### Continuous Integration (CI)

The CI workflow is triggered on pushes and pull requests to the repository. Its purpose is to build and test the project.

```yaml
#CI

name: Continuous Integration

on: [push, pull_request]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python 3.8
      uses: actions/setup-python@v2
      with:
        python-version: '3.8' 

    - name: Install dependencies
      run: |
        pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run unit tests
      run: |
        python -m unittest discover -s tests -v
```

#### CI Workflow Steps:

1. **Checkout Repository**: Fetches the latest code from the repository.
2. **Set up Python 3.8**: Configures the Python version for the environment.
3. **Install Dependencies**: Ensures that Python dependencies listed in `requirements.txt` are installed.
4. **Run Unit Tests**: Executes unit tests located in the `tests` directory.

### Continuous Deployment (CD)

The CD workflow is triggered on pushes to the `main` and `kadidia` branches. Its purpose is to build a Docker image and push it to Docker Hub.


#### CD Workflow Steps:

1. **Checkout Repository**: Fetches the latest code from the repository.
2. **Log in to Docker Hub**: Authenticates with Docker Hub using credentials stored in GitHub secrets.
3. **Build and push Docker image**: Builds a Docker image from the project and pushes it to Docker Hub.


To run the CI workflow locally, you can use the following commands:

```bash
git clone <repository_url>
cd <repository_directory>
pip install --upgrade pip
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

#### Continuous Deployment

**Continuous Deployment (CD)** automates the process of deploying the application to a production environment whenever code changes are pushed to specific branches. In this case, deployments are triggered when changes are pushed to the `main` and `kadidia` branches.

##### CD Workflow Steps:

1. **Checkout Repository**: This step fetches the latest code from the repository.
2. **Log in to Docker Hub**: Authenticates with Docker Hub using credentials stored in GitHub secrets.
3. **Build and push Docker image**: Builds a Docker image from the project and pushes it to Docker Hub.

To deploy the application using Docker, you can follow the CD workflow by pushing changes to the `main` or `kadidia` branches.

Please customize and expand these sections in the README based on your specific project details and requirements. If you have any additional information or specific instructions you'd like to include in the README, please let me know, and I can provide further assistance.

## Docker Setup
This project can be run using Docker Compose. The `docker-compose.yml` file is configured to set up the application and its required services. The application is exposed on port 5001, and the MySQL database is exposed on port 3307.

To start the application using Docker Compose, run the following command:
```sh
docker-compose up -d
```

The application can then be accessed at `http://localhost:5000`.

To stop and remove the containers created by Docker Compose, run:
```sh
docker-compose down
```

Please ensure to customize the environment variables in the `docker-compose.yml` file according to your needs before starting the application.
