### Project Brief
A Micro-service Application, built with Python, Nodejs and different software architecture and technologies like **Microservices Architecture**, **Event Driven Architecture**, **Load Balancing**, **Caching**. For communication between independent services, we use asynchronous messaging using rabbitmq, and for synchronous communication for real-time communications with using REST.

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
Web-Proxy: Nginx
Technology: Docker and Docker-Compose

##### *Message Broker:*
Rabbit MQ

### Features:
- Micro-service Architecture for better scalability, faster development cycle, higher degree of fault tolerance.
- Entire application is dockerized
- Vertical Scaling using docker scale
- Load Balancing with Nginx
- Message Broker for decoupling different services.
- Restful APIs to perform CRUD Operations
- MongoDB as Document Database
- Caching using Redis

### Project's HLD
![screenshot](https://github.com/Kartikdudeja/microservice-application/blob/main/ProjectX-HLD(with%20grid).png)

### Quick Start the Project
``` bash
docker-compose up --build -d
```

### Swagger Documentation:
After Starting the Application, visit the following link to access the API Documentation
``` bash
http://127.0.0.1:5000/docs
```
