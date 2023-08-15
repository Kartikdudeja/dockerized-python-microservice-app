## Dockerized Python Micro-Service Application

A Dockerized Micro-service Application, built with Python, Nodejs and different software architecture and technologies like **Microservices Architecture**, **Event Driven Architecture**, **Load Balancing**, **Caching**. For communication between independent services, we use asynchronous messaging using rabbitmq, and for synchronous communication for real-time communications with using REST.

Micro-service application designed to be containerized, facilitating effortless deployment, scalability, and streamlined maintenance.

### Technology Stack

##### *Backend:*

**Micro-Service 1:**<br/>
Language: Python<br/>
Framework: FastAPI<br/>

**Micro-Service 2:**<br/>
Language: Nodejs<br/>
Framework: Express<br/>

##### *Database:*
Relational Database: Postgres<br/>
NoSQL Database: MongoDB<br/>
Cache Database: Redis


##### *Deployment:*
Operating System: Linux<br/>
Web-Proxy: Nginx<br/>
Technology: Docker and Docker-Compose<br/>
CI/CD Pipeline: Jenkins

##### *Message Broker:*
Rabbit MQ

### Features:
- Micro-service Architecture for better scalability, faster development cycle, higher degree of fault tolerance.
- Entire application is dockerized
- Vertical Scaling using docker scale
- CI/CD Pipeline using Jenkins
- Load Balancing with Nginx
- Message Broker for decoupling different services.
- Restful APIs to perform CRUD Operations
- MongoDB as Document Database
- Caching using Redis

### Project's HLD
![screenshot](https://github.com/Kartikdudeja/microservice-application/blob/main/ProjectX-HLD(with%20grid).png)

## Getting Started

Follow these steps to set up and run the Dockerized micro-service application on your local machine.

### Prerequisites

Make sure you have the following software installed on your system:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)

### Installation and Setup

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/Kartikdudeja/dockerized-python-microservice-app.git
   ```

2. Navigate to the project directory:

   ```bash
   cd dockerized-python-microservice-app
   ```

### Build and Run the Docker Containers

1. Build the Docker images for your micro-service application:

   ```bash
   docker-compose build
   ```

2. Start the Docker containers:

   ```bash
   docker-compose up -d
   ```

   This will start the micro-service containers defined in the `docker-compose.yml` file.

3. Access the micro-service in your web browser or using tools like `curl` or Postman.

#### Swagger Documentation:
After Starting the Application, visit the following link to access the API Documentation
``` bash
http://127.0.0.1:5000/docs
```

### Scaling

To scale your micro-service application, you can adjust the number of containers using Docker Compose:

```bash
docker-compose up -d --scale service_name=num_instances
```

Replace `service_name` with the name of the micro-service defined in `docker-compose.yml` and `num_instances` with the desired number of instances.

### Stopping the Containers

To stop and remove the running containers, use the following command:

```bash
docker-compose down
```

## Acknowledgments

- Docker documentation: [https://docs.docker.com](https://docs.docker.com)
- Docker Compose documentation: [https://docs.docker.com/compose](https://docs.docker.com/compose)
- Python documentation: [https://docs.python.org](https://docs.python.org)

---

Happy micro-service development!
