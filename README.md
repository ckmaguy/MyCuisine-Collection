```markdown
# MyCuisine Collection

**MyCuisine Collection** is a Flask & MySQL web application for managing personal recipes. It's designed for culinary enthusiasts and web developers interested in learning more about web application development, database management, and automated testing.

**Link to the deployed image:** [Docker Hub - MyCuisine Collection](https://hub.docker.com/r/kadidiac/my-cuisine-collection)

## Features

- **User Authentication**: Register and log in to your account.
- **Recipe CRUD Operations**: Create, read, update, and delete recipes in a user-friendly interface.
- **Responsive Design**: Ensures compatibility with various devices and screen sizes.
- **Docker Deployment**: Simplifies deployment and ensures consistency across different environments.
- **Automated Testing with Selenium**: Guarantees application stability and performance.

## Technical Stack

- **Backend Framework**: Flask (Python)
- **Database**: MySQL
- **Containerization**: Docker
- **Testing**: Selenium for browser automation

## File and Directory Structure

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
9. **requirements.txt**: Lists dependencies.
10. **Testing Files**:
    - **start_test.py**
    - **test_mycuisine_db.sql**
    - **testing_config.py**
    - **tests** directory.

## Getting Started

### Installation

Clone the repository:

```bash
git clone https://github.com/ckmaguy/MyCuisine-Collection.git
```

Install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Usage

To run the application:

```bash
python run.py
```

### Testing

To run the unit tests:

```bash
python -m unittest discover -s tests -v
```

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

## Continuous Integration and Deployment

This project uses GitHub Actions for Continuous Integration (CI) and Continuous Deployment (CD). The CI workflow runs tests on every push and pull request to the main branch, ensuring that changes do not break the application. The CD workflow builds and pushes the Docker image to Docker Hub on pushes to the main branch.

