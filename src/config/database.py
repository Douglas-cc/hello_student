from motor.motor_asyncio import AsyncIOMotorClient


MONGO_DETAILS = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_DETAILS)

db = client.students

student_collection = db.get_collection("students_collection")
