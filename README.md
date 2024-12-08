# SNR

## Project Overview
This project implements a message queue system using Flask, allowing for the production and consumption of messages through various endpoints. It includes three different blueprints for handling various tasks: Task One, Task Two, and Task Three.

- **Task One**: Demonstrates a producer-consumer pattern using multi-threading:
  - Producer thread generates random integers every 0.1 seconds
  - Consumer thread processes integers every 0.15 seconds 
  - Uses a thread-safe queue with max size of 10
  - Implements proper thread synchronization with locks
  - Runs for 10 seconds before graceful termination

- **Task Two**: Implements a RabbitMQ message broker system with three different messaging patterns:
  - **Basic Queue Pattern**:
    - Creates a simple queue named "test_queue"
    - Sender publishes "Hello, World!" message to the queue
    - Receiver listens and prints messages from the queue
    - Demonstrates basic point-to-point messaging
  - **Work Queue Pattern**: 
    - Distributes time-consuming tasks among multiple workers
    - Implements persistent message delivery
    - Ensures fair dispatch of tasks
    - Useful for resource-intensive operations
  - **Publish/Subscribe Pattern**:
    - Uses exchanges to broadcast messages to multiple queues
    - Publishers send messages to an exchange
    - Multiple subscribers can receive the same message
    - Implements fanout exchange type for broadcasting

- **Task Three**: Implements a simple greeting RESTful API endpoint that returns personalized JSON greeting messages.

## Endpoint Structure
- **Task One**
  - **/v1/multi_threading**: This endpoint demonstrates a producer-consumer pattern using multi-threading. A producer thread generates random integers every 0.1 seconds and places them in a thread-safe queue (max size 10). A consumer thread reads and processes these integers every 0.15 seconds. The system runs for 10 seconds before gracefully terminating.

- **Task Two**
  - **/v1/basic_queue**: Demonstrates the simplest form of messaging with RabbitMQ
    - **Functionality**: Creates a direct point-to-point queue where one sender sends a "Hello, World!" message and one receiver consumes it
    - **Use Case**: Simple message passing between two components

  - **/v1/work_queue**: Implements a task distribution system
    - **Functionality**: Distributes multiple tasks (Task 1-5) among available workers
    - **Features**: Message persistence, fair dispatch
    - **Use Case**: Distributing resource-intensive tasks among multiple workers

  - **/v1/pub_sub**: Implements publish/subscribe messaging pattern
    - **Functionality**: Broadcasts messages to multiple subscribers through an exchange
    - **Features**: Fanout exchange type, multiple subscribers
    - **Use Case**: Broadcasting events to multiple interested parties

- **Task Three**
  - **/v1/greet**: A RESTful API endpoint that accepts GET requests with an optional query parameter 'name'.
    - **Functionality**: Returns a JSON response with a greeting message.
    - If a name is provided: Returns {"message": "Hello, {name}!"}
    - If no name is provided: Returns {"message": "Hello, World!"}

## Example Usage
- **Task One**: Access the `/v1/multi_threading` endpoint to observe the producer-consumer pattern in action. Watch as random integers are generated and processed in a thread-safe manner over a 10-second period.
- **Task Two**: 
  - Basic Queue: Access `/v1/basic_queue` to see simple message passing
  - Work Queue: Use `/v1/work_queue` to observe task distribution among workers
  - Pub/Sub: Try `/v1/pub_sub` to see message broadcasting in action
- **Task Three**: Access the `/v1/greet` endpoint to receive a JSON greeting message:
  - Without parameter: GET `/v1/greet` returns {"message": "Hello, World!"}
  - With name parameter: GET `/v1/greet?name=John` returns {"message": "Hello, John!"}

## Running the Application
This application uses Docker Compose to manage multiple containers:
- An application server container built from our Dockerfile that runs the Flask application
- A RabbitMQ container that provides the message queue functionality required for Task Two

To run both containers, navigate to the project directory and execute:
```
docker-compose up --build
```

## Docker Compose Setup

The `docker-compose.yml` file defines two services:
- `app`: The Flask application service
  - Built from the Dockerfile in the current directory
  - Maps port 5000 to host port 5000
  - Depends on RabbitMQ service
  - Environment variables configured for RabbitMQ connection

- `rabbitmq`: The RabbitMQ message broker service
  - Uses official RabbitMQ 3-management image
  - Maps ports 5672 (AMQP) and 15672 (Management UI)
  - Persists data using named volume

## Demo

The first gif demonstrates the process of starting the application using Docker Compose, which launches both the Flask application and RabbitMQ containers.

![alt text](intro.gif)

The second gif demonstrates Task One's producer-consumer pattern implementation using multi-threading. It shows how random integers are safely produced and consumed using a shared queue with thread synchronization. You can check the terminal to see the generated numbers in real-time, and the final produced and consumed items will be displayed on the webpage as JSON response.

![alt text](one.gif)

The third gif demonstrates Task Two's basic queue implementation using RabbitMQ. It shows a simple message queue where a single message "Hello, World!" is sent to a queue and then consumed by a receiver. The terminal output displays both the sending and receiving of the message, demonstrating the message queue pattern in action.

![alt text](two.gif)

The fourth gif demonstrates Task Two's work queue implementation using RabbitMQ. Unlike the basic queue which sends a single message, the work queue distributes multiple tasks (Task 1 through Task 5) among available workers. This implementation ensures fair dispatch of work, with the round-robin distribution ensuring no worker is overwhelmed. The messages are also made persistent to prevent loss in case of RabbitMQ server crashes. The terminal output shows both the sending of tasks to the queue and their reception by workers, with each worker processing one task at a time.

![alt text](three.gif)

The fifth gif demonstrates Task Two's publish/subscribe (pub/sub) pattern implementation using RabbitMQ. In this pattern, messages are broadcast to multiple subscribers rather than being processed by a single consumer. The publisher sends messages to an exchange, which then distributes them to all bound queues. Each subscriber creates an exclusive queue that is bound to the exchange, allowing them to receive all published messages. This demonstrates how a single message can be delivered to multiple recipients simultaneously, which is useful for scenarios like broadcasting updates or notifications to multiple parts of a system.

![alt text](four.gif)

The sixth gif demonstrates Task Three's greeting endpoint implementation. This simple REST API endpoint accepts GET requests and provides personalized greetings. When accessed without any parameters (GET `/v1/greet`), it returns a default greeting "Hello, World!". When provided with a name parameter (GET `/v1/greet?name=snr`), it returns a personalized greeting "Hello, snr!". The response is formatted as JSON, making it easy to integrate with other applications. The terminal output shows the logging of each request, while the webpage displays the JSON response containing the greeting message.

![alt text](fifth.gif)
