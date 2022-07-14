from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from src.repositories.student import (
    retrieve_student,
    add_student,
    retrieve_students,
    update_student,
    delete_student
)

from src.schemas.student import (
    StudentSchema,
    UpdateStudentModel,
    ResponseModel,
    ErrorResponseModel
)

router = APIRouter()


@router.post("/")
async def add_student_data(student: StudentSchema = Body(...)):
    student = jsonable_encoder(student)
    new_student = await add_student(student)
    return ResponseModel(new_student, "Student added successfully.")


@router.get("/")
async def get_students():
    students = await retrieve_students()
    if students:
        return ResponseModel(students, "Students data retrieved successfully")
    return ResponseModel(students, "Empty list returned")


@router.get("/{id}")
async def get_student_data(id: str):
    student = await retrieve_student(id)
    if student:
        return ResponseModel(student, "Student data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")


@router.put("/{id}")
async def update_student_data(id: str, req: UpdateStudentModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_student = await update_student(id, req)
    
    if updated_student:
        return ResponseModel(
            f'Student with ID: {id} name update is successful',
            'Student name updated successfully'
        )
        
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )
    
    
@router.delete("/{id}")
async def delete_student_data(id: str):
    deleted_student = await delete_student(id)
    
    if deleted_student:
        return ResponseModel(
            f'Student with ID: {id} removed', 
            'Student deleted successfully'
        )
    
    return ErrorResponseModel(
        'An error occurred',
        404,
        f'Student with id {id} doesn`t exist'
    )