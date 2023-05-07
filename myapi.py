#import
from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel


# describe the name
app = FastAPI()


# the data
students ={
    1:{'name':'Bagus',
       'age': 20,
       'classes' : 'L4AC'},
    
    2:{'name':'S',
       'age': 12,
       'classes' : 'L4AC'}
}


class Student(BaseModel):
    name: str
    age: int
    classes: str
    
class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    classes: Optional[str] = None


#-#


# testing the api
@app.get("/")
def index():
    return {"Test" : "Testing"}


# /get-student/.......
# path parameter for description
@app.get("/get-student/{id}")
def get_student(id: int = Path(description="ID of student to get")): 
    return students[id]


# query parameter 
# ex/ google.com/menu?search="..."&age=...    <- this is 2 parameters
@app.get("/get-student_by_name")
def get_student(*,student_id:int, name: str = None, text: str):    #(name: Optional[str] = None):
    # *, is for the required after the optional, but if required first then no need
    for student_id in students:
        if students[student_id]['name'] == name:
            return students[student_id]
    return {"Error": "Student name not found."}


# post method
@app.post("/create-student/{student_id}")
def add_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student ID exist."}
    students[student_id] = student
    return students[student_id]


# put method
@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student ID not found."}
    
    if student[student_id].name != None:
        student[student_id].name = student.name
        
    if student[student_id].age != None:
        student[student_id].age = student.age
        
    if student[student_id].classes != None:
        student[student_id].classes = student.classes
        
    return student[student_id]


# delete method
@app.delete("/delete-student/{student_id}")
def delete_student(student_id:int):
    del students[student_id]
    return {"msg" : "student deleted."}
