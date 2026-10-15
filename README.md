# Backend Languages Comparison and Internals

A beginner-friendly, hands-on tour of how seven popular languages build backend services. The project will implement the same Employee Management REST API in Python, JavaScript, Java, PHP, C#, Go, and Ruby, then compare what happens from the moment an HTTP request arrives until JSON is returned.

The examples begin with in-memory data so the request flow is easy to see. In-memory data is temporary: it is lost when the process stops or restarts. Later lessons will show how each implementation can use MySQL for persistent storage.

## Learning Plan

We will build this in small stages. Each implementation will include its setup, annotated code, sample requests, and tests before moving on.

1. Establish the project overview, prerequisites, and folder plan (this page).
2. Build Python + FastAPI, exercise its routes, and explain the request lifecycle.
3. Build Node.js + Express and compare its request handling and concurrency model with Python.
4. Add Java + Spring Boot, then PHP, C# + ASP.NET Core, Go + `net/http`, and Ruby + Sinatra one at a time.
5. Complete the shared language, runtime, memory, concurrency, REST, security, and MySQL comparison guides.

The first implementation is Python + FastAPI. The later implementations are not included yet, so each can be learned and tested in sequence.

## What We Will Compare

Backend development is the server-side work behind an application: receiving requests, applying rules, accessing data, and sending responses. The languages share these jobs, but differ in syntax, runtime, libraries, and common deployment patterns. A framework also affects how routes, validation, and JSON responses are written, so a route's spelling is not always a language feature.

| Language and planned stack | Runtime and typical request model | Useful strengths | Trade-offs and common fits |
| --- | --- | --- | --- |
| Python + FastAPI | Python runtime; synchronous or asynchronous request handlers | Readable syntax, quick development, type-aware validation and API documentation | Runtime and library choices affect throughput; common in APIs, automation, and data-oriented services |
| JavaScript + Node.js + Express | Node.js runtime; event loop with asynchronous I/O | One language can be used across browser and server; large package ecosystem | CPU-heavy work can block an event loop unless moved elsewhere; common in web APIs and real-time services |
| Java + Spring Boot | JVM; managed threads and asynchronous options | Mature ecosystem, strong tooling, and broad enterprise support | More configuration and concepts to learn; common in large services and enterprise systems |
| PHP | PHP runtime, commonly hosted through a web server; request execution depends on the deployment model | Direct fit with web hosting and a mature web ecosystem | Hosting and application architecture shape process reuse and concurrency; common in websites and web APIs |
| C# + ASP.NET Core | .NET runtime; asynchronous I/O and thread-pool scheduling | Strong tooling, typed APIs, and broad web/cloud support | Framework and runtime concepts add an initial learning curve; common in business and cloud services |
| Go + `net/http` | Compiled native program; goroutines support concurrent work | Small deployment artifacts, simple standard HTTP package, and built-in concurrency primitives | Fewer high-level framework conventions by default; common in network services and infrastructure tools |
| Ruby + Sinatra | Ruby runtime; request concurrency depends on the server and deployment | Concise syntax and a small framework surface | Runtime and server choices matter for scaling; common in small services and rapid web development |

This is a starting map, not a speed ranking. Real performance and operational fit depend on workload, architecture, libraries, hardware, and deployment configuration. The later lessons will separate differences caused by the language from those caused by its runtime or framework.

## Request Workflow

The same basic path appears in all seven implementations:

```mermaid
flowchart LR
	A[Client / Browser] --> B[HTTP Request]
	B --> C[Web Server / Runtime]
	C --> D[Router]
	D --> E[Input Validation]
	E --> F[Business Logic]
	F --> G[Database, when required]
	G --> H[JSON Response]
	H --> I[Client / Browser]
```

For the first examples, the data step uses an in-memory collection instead of a database. The MySQL lessons will replace that storage step while leaving the client-facing API largely the same.

## Planned Project Structure

Folders are added as their stage begins. This is the intended end state; only this README is present at the start.

```text
backend-languages-comparison/
├── README.md
├── docs/
│   ├── backend-fundamentals.md
│   ├── language-comparison.md
│   ├── request-lifecycle.md
│   ├── runtime-and-memory.md
│   └── performance-and-concurrency.md
├── python-fastapi/
│   ├── app/
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
├── javascript-node-express/
├── java-spring-boot/
├── php/
├── csharp-aspnet-core/
├── go/
└── ruby-sinatra/
```

Each language folder will use that ecosystem's normal dependency and configuration files, source layout, startup command, and test conventions. Implementations will provide `GET /employees`, `GET /employees/{id}`, `POST /employees`, `PUT /employees/{id}`, `DELETE /employees/{id}`, and `GET /health`. Framework route syntax can differ: for example, Express examples will use `/employees/:id`, while FastAPI uses `/employees/{id}`. Both represent a path parameter; the framework defines the spelling.

## Prerequisites

### Needed for the first stage

- VS Code with its integrated PowerShell terminal.
- Python 3.10 or newer and `pip`.
- An internet connection for installing FastAPI and the development server.

Check the Python installation in the VS Code terminal:

```powershell
py --version
py -m pip --version
```

If `py` is not recognized, install a current Python release and enable the option to add Python to `PATH`, then open a new terminal. The first implementation will give the exact commands to create an isolated virtual environment and install its dependencies.

### Needed in later stages

Install these when we reach their implementation; they are not required to begin with Python:

| Stage | Required tools | Version check |
| --- | --- | --- |
| Node.js + Express | Node.js and npm | `node --version`; `npm --version` |
| Java + Spring Boot | JDK 17 or newer; Maven wrapper will be included with the example | `java --version` |
| PHP | PHP 8.1 or newer; Composer | `php --version`; `composer --version` |
| C# + ASP.NET Core | .NET SDK 8 or newer | `dotnet --info` |
| Go | Go 1.21 or newer | `go version` |
| Ruby + Sinatra | Ruby and Bundler | `ruby --version`; `bundle --version` |
| MySQL lessons | MySQL Server, or a compatible managed/local instance | `mysql --version` |

Postman is optional. The examples will also include command-line requests that can be run from PowerShell, so a separate API client is not required.

## Shared API Contract

All seven versions will use the same JSON shape and HTTP behavior. An employee will have an integer `id`, a string `name`, and a string `email`. Creating an employee accepts `name` and `email`; the server assigns the ID. Invalid input will receive a client-error status, a missing employee will receive `404 Not Found`, successful creation will receive `201 Created`, and successful reads, updates, or deletes will use appropriate `2xx` statuses.

Each implementation will include automated tests for successful operations and common errors, example request/response pairs, startup and shutdown instructions, Postman steps, and troubleshooting notes. The MySQL guide will explain connection settings and safe handling of credentials rather than committing passwords to the repository.

## Next

The next lesson will create `python-fastapi/`, explain each file before adding it, and implement the API with in-memory data. It will walk through receiving a request, parsing and validating JSON, applying the employee operation, handling errors, and returning a JSON response.