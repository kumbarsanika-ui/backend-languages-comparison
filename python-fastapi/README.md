# Python + FastAPI

This is the first implementation of the shared Employee Management API. It uses a small in-memory collection so you can follow the request and response before adding a database.

## Files

- `app/main.py` defines the employee data shapes, creates the FastAPI application, stores example records in memory, and implements all six routes.
- `tests/test_main.py` sends requests directly to a fresh app and checks successful operations, invalid input, and missing employees.
- `requirements.txt` lists the web framework, local development server, email validation support, and test tools.
- `.gitignore` keeps the local virtual environment and generated Python/test caches out of version control.

## Requirements and Setup

Use Python 3.10 or newer. From the VS Code PowerShell terminal, start in the repository root and run:

```powershell
cd python-fastapi
py --version
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

If PowerShell blocks virtual-environment activation, you can install and run tools through the environment directly instead:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
.\.venv\Scripts\python.exe -m pytest
```

## Run and Test

Start the development server from `python-fastapi/`:

```powershell
py -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for FastAPI's interactive API page. Stop the server with `Ctrl+C`. Run the automated tests from the same folder in another terminal:

```powershell
py -m pytest
```

Restarting the server creates a new in-memory collection. The sample employee returns, and any records you created or changed are gone. A database is needed to preserve them.

## Routes and Example Requests

| Method | Path | Result |
| --- | --- | --- |
| `GET` | `/health` | `200` health status |
| `GET` | `/employees` | `200` list of employees |
| `GET` | `/employees/{employee_id}` | `200` employee, or `404` if absent |
| `POST` | `/employees` | `201` created employee |
| `PUT` | `/employees/{employee_id}` | `200` updated employee, or `404` if absent |
| `DELETE` | `/employees/{employee_id}` | `204` with no response body, or `404` if absent |

FastAPI uses braces for a path parameter, such as `{employee_id}`. That notation belongs to the framework's router, not to Python itself.

List employees in PowerShell:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/employees
```

Create one:

```powershell
$body = @{ name = 'Grace Hopper'; email = 'grace@example.com' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/employees -ContentType 'application/json' -Body $body
```

The response has this shape (the assigned ID is `2` in a fresh server process):

```json
{
  "id": 2,
  "name": "Grace Hopper",
  "email": "grace@example.com"
}
```

To test in Postman, create a request to `http://127.0.0.1:8000/employees`. Choose `POST`, select **Body → raw → JSON**, enter `{"name":"Grace Hopper","email":"grace@example.com"}`, and send. Use the route table for the other methods; for `PUT`, send the same JSON fields to `/employees/2`.

## How the POST Request Works

1. Uvicorn receives the HTTP request and passes it to the FastAPI application.
2. FastAPI matches `POST /employees` to the decorated `create_employee` function.
3. FastAPI parses the JSON body into `EmployeeInput`. Pydantic checks that `name` has 1-100 characters and that `email` is a valid email address. Invalid data gets `422` without entering the function.
4. The function reads the next ID, builds an `Employee`, and stores it in `app.state.employees`.
5. FastAPI serializes the returned model as JSON and sends `201 Created`.

`EmployeeInput` describes client-provided fields; the server-owned `id` is added by `Employee`. `HTTPException` turns missing records into `404` responses. Returning a `Response` with status `204` makes DELETE an intentionally empty response.

## Post-Setup Notes

- `ModuleNotFoundError`: make sure the terminal is in `python-fastapi/` and the virtual environment is active, then install `requirements.txt` again.
- `Address already in use`: stop the other server with `Ctrl+C`, or start this one on another port with `py -m uvicorn app.main:app --reload --port 8001`.
- PowerShell does not recognize `py`: install Python, enable the PATH option, and open a new terminal. Use `python` in place of `py` if that is the launcher available on your system.
- A `422` response means the request body did not pass validation. Check the JSON format, required fields, name length, and email value.

## MySQL Later

The routes currently read and write a Python dictionary; that is why restarting loses changes. In a later stage, the storage operations will be replaced with a MySQL connection and parameterized SQL (or a Python database library). The connection string and password will come from environment variables, not source code. The API contract and HTTP status behavior can remain the same.