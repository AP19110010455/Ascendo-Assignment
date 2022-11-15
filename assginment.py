from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from uuid import UUID
from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __init__(self, students_to_return):
        self.students_to_return = students_to_return


app = FastAPI()


class Students(BaseModel):
    id: int
    Student_Name: str = Field(min_length=1,max_length=100)
    created_at: str = Field(min_length=1, max_length=100)
    created_by:str = Field(min_length=1, max_length=100)
    updated_at: str = Field(min_length=1, max_length=100)
    updated_by:str = Field(min_length=1, max_length=100)

    class Config:
        schema_extra = {
            "example": {
                "id": 2,
                "Student_Name": "Aj",
                "created_at": "5/06/05",
                "created_by": "A very nice description of a book",
                "updated_at": "7/06/05",
                'updated_by':"Hello"
            }
        }




Student_Details = []


@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request,
                                            exception: NegativeNumberException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Hey, why do you want {exception.students_to_return} "
                            f"books? You need to read more!"}
    )






@app.get("/")
async def read_all_students(students_to_return: Optional[int] = None):

    if students_to_return and students_to_return < 0:
        raise NegativeNumberException(students_to_return=students_to_return)

    if len(Student_Details) < 1:
        create_students_no_api()

    if students_to_return and len(Student_Details) >= students_to_return > 0:
        i = 1
        new_student = []
        while i <= students_to_return:
            new_student.append(Student_Details[i - 1])
            i += 1
        return new_student
    return Student_Details


@app.get("/student/{students_id}")
async def read_student(student_id: int):
    for x in Student_Details:
        if x.id == student_id:
            return x
    raise raise_item_cannot_be_found_exception()


# @app.get("/book/rating/{book_id}", response_model=BookNoRating)
# async def read_book_no_rating(student_id: UUID):
#     for x in Student_Details:
#         if x.id == student_id:
#             return x
#     raise raise_item_cannot_be_found_exception()


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_student(student: Students):
    Student_Details.append(student)
    return student


@app.put("/{students_id}")
async def update_student(student_id: int, student: Students):
    counter = 0

    for x in Student_Details:
        counter += 1
        if x.id == student_id:
            Student_Details[counter - 1] = student
            return Student_Details[counter - 1]
    raise raise_item_cannot_be_found_exception()


@app.delete("/{students_id}")
async def delete_student(student_id: int):
    counter = 0

    for x in Student_Details:
        counter += 1
        if x.id == student_id:
            del Student_Details[counter - 1]
            return f'Student_ID:{student_id} deleted'
    raise raise_item_cannot_be_found_exception()


def create_students_no_api():
    student_1 = Students(id=1,
                  Student_Name="Aj",
                  created_at="5/06/05",
                  created_by="Ak",
                  updated_at="6/06/05",
                  updated_by="Sk")
    student_2 = Students(id=2,
                  Student_Name="Aj",
                  created_at="5/06/05",
                  created_by="Ak",
                  updated_at="6/06/05",
                  updated_by="Sk")
    student_3 = Students(id=3,
                  Student_Name="Aj",
                  created_at="5/06/05",
                  created_by="Ak",
                  updated_at="7/06/05",
                  updated_by="Sk")
    student_4 = Students(id=4,
                  Student_Name="Aj",
                  created_at="5/06/05",
                  created_by="Ak",
                  updated_at="8/06/05",
                  updated_by="Sk")
    Student_Details.append(student_1)
    Student_Details.append(student_2)
    Student_Details.append(student_3)
    Student_Details.append(student_4)


def raise_item_cannot_be_found_exception():
    return HTTPException(status_code=404,
                         detail="Student not found",
                         headers={"X-Header_Error":
                                  "Nothing to be seen at the UUID"})
