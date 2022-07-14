from bson.objectid import ObjectId
from src.config.database import student_collection


# função auxiliar para fazer consultar no banco de dados
def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "email": student["email"],
        "course_of_study": student["course_of_study"],
        "year": student["year"],
        "GPA": student["gpa"],
    }


# Recuperar todos os alunos presentes no banco de dados
async def retrieve_students():
    students = []
    async for student in student_collection.find():
        students.append(student_helper(student))
    return students


# Adicionar um novo aluno ao banco de dados
async def add_student(student_data: dict) -> dict:
    student = await student_collection.insert_one(student_data)
    new_student = await student_collection.find_one({"_id": student.inserted_id})
    return student_helper(new_student)


# Recuperar um aluno com um ID correspondente
async def retrieve_student(id: str) -> dict:
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        return student_helper(student)


# Atualizar um aluno com um ID correspondente
async def update_student(id: str, data: dict):
    # Retorna false se um corpo de solicitação vazio for enviado.
    if len(data) < 1:
        return False
    
    student = await student_collection.find_one({"_id": ObjectId(id)})
    
    if student:
        updated_student = await student_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        
        if updated_student:
            return True
        
        return False


# Excluir um aluno do banco de dados
async def delete_student(id: str):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True