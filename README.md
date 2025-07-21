
# Math Microservice (FastAPI Extended Version)

## Overview

This project builds upon an [initial CLI-based microservice](https://github.com/techwithirina/math_service.git) that performed mathematical operations (power, Fibonacci, factorial) via a command-line interface using `click`, with results logged into a local SQLite database. The original implementation emphasized simplicity, modularity, and extensibility, using tools like `pydantic` for input validation and `flake8` for code quality.

The project has now been extended into a production-oriented FastAPI-based microservice that incorporates modern backend design features including asynchronous request processing, bearer token authorization, and in-memory caching with expiration control.

## FastAPI Integration

The service was migrated from a CLI tool to a web-accessible REST API using FastAPI. FastAPI was chosen for its high performance, ease of use, automatic validation through Pydantic, and built-in support for OpenAPI documentation.

All CLI commands were converted into POST endpoints:

- `/power`: Computes a number raised to a power.
- `/fib`: Computes the n-th Fibonacci number.
- `/fact`: Computes the factorial of a number.

Each endpoint accepts validated JSON input and returns JSON responses. The input is parsed using Pydantic models, and computation logic is reused from the original service implementation.

## Multithreaded Background Processing

To prevent blocking operations such as logging from delaying API responses, a background worker system was implemented using Python’s `threading` and `queue` modules.

When a user sends a request to an endpoint:

1. The computation result is immediately returned to the user.
2. A logging task is placed in a thread-safe queue.
3. A background worker thread continuously reads from this queue and writes logs to the SQLite database.

This design keeps request handling fast and cleanly separates business logic from side-effects such as I/O operations.

## Authorization with Bearer Tokens

The microservice is secured using Bearer token authentication. Each incoming request is required to include an Authorization header with a valid token.

Tokens are defined in a `.env` file and loaded at runtime using the `python-dotenv` library. FastAPI’s `HTTPBearer` and `Depends` features are used to inject and validate the token for every endpoint.

This approach was selected for its simplicity and alignment with standard practices for securing RESTful APIs, while still being lightweight and suitable for local or internal use.

## In-Memory Caching with Expiry

To optimize repeated requests, especially for computationally expensive operations like Fibonacci and factorial, an in-memory caching layer was added.

Key characteristics of the caching layer:

- Thread-safe using `threading.Lock`.
- Configurable expiration using a TTL (time-to-live) defined in `.env`.
- Each cached entry stores both result and timestamp.
- Before returning a cached result, its validity is checked based on TTL.

This approach reduces unnecessary computation and improves performance for frequent queries.

## Summary

This FastAPI-based extension transforms the original CLI math tool into a functional, secure, and performant microservice. It demonstrates key backend patterns including:

- RESTful API design with FastAPI.
- Background processing using multithreading.
- Token-based authorization.
- Thread-safe in-memory caching with expiration.