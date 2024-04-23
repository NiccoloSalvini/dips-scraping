# dips-scraping

## Description

This project is aimed at scraping data from the DIPS website.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/dips-scraping.git
    ```

2. Navigate to the project directory:

    ```bash
    cd dips-scraping
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the main script:

    ```bash
    python main.py
    ```

2. The scraped data will be saved in the `data` directory.

## Contributing

Contributions are welcome! Please follow the guidelines in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is licensed under the [MIT License](LICENSE).
## Docker Compose

To spin up a test database using Docker Compose, follow these steps:

1. Make sure you have Docker and Docker Compose installed on your machine.

2. Create a `docker-compose.yml` file in the root directory of your project with the following content:

    ```yaml
    version: '3'
    services:
      db:
         image: postgres
         environment:
            POSTGRES_USER: your_username
            POSTGRES_PASSWORD: your_password
            POSTGRES_DB: your_database
         ports:
            - 5432:5432
    ```

3. Open a terminal and navigate to the root directory of your project.

4. Run the following command to start the test database:

    ```bash
    docker-compose up -d
    ```

    This will start a PostgreSQL database container with the specified credentials and expose port 5432.

5. You can now connect to the test database using the following connection details:

    - Host: localhost
    - Port: 5432
    - Username: your_username
    - Password: your_password
    - Database: your_database

## Directory Structure

Here is an example directory structure for your project:
