#import
from fastapi import FastAPI, Path, Query
from typing import Optional
from pydantic import BaseModel


# describe the name
app = FastAPI()

#the data
todolists = {
    1:{'task' : 'feed the cats',
       'status' : 'pending',
       'deadline' :'today'},
    
    2:{'task' : 'water the flowers',
       'status' : 'completed',
       'deadline' :'today'},
    
    3:{'task' : 'clean the window',
       'status' : 'pending',
       'deadline' :'tomorrow'},
    
    4:{'task' : 'buy the groceries',
       'status' : 'completed',
       'deadline' :'tomorrow'},
    
    5:{'task' : 'do the homework',
       'status' : 'late',
       'deadline' :'1pm'},
}

class todoList(BaseModel):
    task: str
    status: str
    deadline: str
    
class UpdatetodoList(BaseModel):
    task: Optional[str] = None
    status: Optional[str] = None
    deadline: Optional[str] = None

# get todo-list by ID
@app.get("/get-todolist_by_ID/{id}")
def get_todolist(id: int = Path(description="Number of task you want to check by id:")): 
    return todolists[id]


# get todo-list by status
@app.get("/get-todolist_by_status")
def get_todolist(status: str = Query(description="Please only put 'pending', 'late', or 'completed' !")): 
    matching_todolists = []
    for todolist_id in todolists:
        if todolists[todolist_id]['status'] == status:
            matching_todolists.append(todolists[todolist_id])
    
    if matching_todolists:
        return matching_todolists
    else:
        return {"Error": "No task(s) were found."}


# get todo-list by deadline
@app.get("/get-todolist_by_deadline")
def get_todolist(deadline: str = Query(description="Please put the exact deadline of the tasks ex/ 'today', 'tomorrow', 'monday', '1pm' !")): 
    matching_todolists = []
    for todolist_id in todolists:
        if todolists[todolist_id]['deadline'] == deadline:
            matching_todolists.append(todolists[todolist_id])
    
    if matching_todolists:
        return matching_todolists
    else:
        return {"Error": "No task(s) were found."}


# post method
@app.post("/create-todolist/{todolist_id}")
def add_todolist(todolist_id: int, todolist: todoList):
    if todolist_id in todolists:
        return {"Error": "Task ID exist."}
    todolists[todolist_id] = todolist
    return todolists[todolist_id]


# put method
@app.put("/update-todolist/{todolist_id}")
def update_todolist(todolist_id: int, todolist: UpdatetodoList):
    if todolist_id not in todolists:
        return {"Error": "Task ID not found."}

    todo = todolists[todolist_id]

    if todolist.task is not None:
        todo['task'] = todolist.task
        
    if todolist.status is not None:
        todo['status'] = todolist.status
        
    if todolist.deadline is not None:
        todo['deadline'] = todolist.deadline
        
    return todo


# delete method
@app.delete("/delete-todolist/{todolist_id}")
def delete_todolist(todolist_id: int):
    del todolists[todolist_id]
    return {"msg" : "Task deleted."}