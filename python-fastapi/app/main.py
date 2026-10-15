from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, EmailStr, Field


class EmployeeInput(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr


class Employee(EmployeeInput):
    id: int


def create_app() -> FastAPI:
    app = FastAPI(title="Employee Management API")
    app.state.employees = {
        1: Employee(id=1, name="Ada Lovelace", email="ada@example.com")
    }
    app.state.next_employee_id = 2

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/employees", response_model=list[Employee])
    def list_employees() -> list[Employee]:
        return list(app.state.employees.values())

    @app.get("/employees/{employee_id}", response_model=Employee)
    def get_employee(employee_id: int) -> Employee:
        employee = app.state.employees.get(employee_id)
        if employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee

    @app.post(
        "/employees",
        response_model=Employee,
        status_code=status.HTTP_201_CREATED,
    )
    def create_employee(employee_input: EmployeeInput) -> Employee:
        employee_id = app.state.next_employee_id
        app.state.next_employee_id += 1
        employee = Employee(id=employee_id, **employee_input.model_dump())
        app.state.employees[employee_id] = employee
        return employee

    @app.put("/employees/{employee_id}", response_model=Employee)
    def update_employee(employee_id: int, employee_input: EmployeeInput) -> Employee:
        if employee_id not in app.state.employees:
            raise HTTPException(status_code=404, detail="Employee not found")
        employee = Employee(id=employee_id, **employee_input.model_dump())
        app.state.employees[employee_id] = employee
        return employee

    @app.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_employee(employee_id: int) -> Response:
        if employee_id not in app.state.employees:
            raise HTTPException(status_code=404, detail="Employee not found")
        del app.state.employees[employee_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return app


app = create_app()