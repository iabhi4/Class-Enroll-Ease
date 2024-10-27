### Prerequisites

- A linux distribution
- Python (version 3.10.12 or compatible)
- Foreman for managing Procfile-based applications
- KrakenD for API Gateway
- Redis Server for caching and data storage
- AWS CLI with configured dummy credentials for DynamoDB Local, for local DynamoDB management
- Java Runtime Environment (JRE) for running DynamoDB Local
- aiosmtpd for mail server

### Setup
Before running the application, ensure that you have Redis and DynamoDB Local correctly installed and configured. Make sure you have Java Runtime Environment (JRE) installed on your machine as DynamoDB Local requires Java. 

Follow these steps to set up your environment and run the application:

- Clone the Repository:

Use the following command to clone the project repository:
```
git clone https://github.com/iabhi4/Class-Enroll-Ease.git
```

- Initialize the Project:

Navigate to the project directory.
Run make to set up the Python virtual environment and install required Python packages from requirements.txt:
```
make
```

- Start Redis Server:

Ensure Redis Server is running on your system:
```
redis-server
```


### Quick Start Guide - Running API

- Use the following scripts to start the project, create and populate the databases:

```
sh run.sh
sh resetDatabases.sh
```

Now you can access the API through the listed URLs and ports listed below.

### URLs and Ports

Foreman will host the processes  in the following URLs and ports:

- `users-primary`: [http://localhost:5000](http://localhost:5000)
- `enroll.1`: [http://localhost:5300](http://localhost:5000)
- `enroll.2`: [http://localhost:5301](http://localhost:5001)
- `enroll.3`: [http://localhost:5302](http://localhost:5002)
- `krakend`: [http://localhost:5400](http://localhost:5400)
- `dynamodb_local`: [http://localhost:5500](http://localhost:5500)
- `notification_service`: [http://localhost:5600](http://localhost:5600)

### Testing endpoints

Downloading Postman is optional, however it was used to test our endpoints, as stated in the project documentation.

Example credentials:

```
{
    "username": "micah",
    "password": "12345"
}
```

This credentials include the roles instructor, registrar, and student making it
simple to test all endpoints with just one bearer.

Use login endpoint to retrieve bearer and pass this bearer in body for all endpoints.
