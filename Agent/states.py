
from asyncio import Task
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
class File(BaseModel):
    path : str = Field(description="The path of the file it will be kept in")
    purpose : str = Field(description="The purpose of the file, e.g 'main application logic', 'data processing logic'")
class Plan(BaseModel):
    name : str = Field(description="This field is the name of the app you are going to make in according to the user's prompt") 
    description : str = Field(description="A single line description of the app you are making")    
    techstack : str = Field(description="The tech stack that will be used to build this app . Eg. : Python, Javascript, HTML, CSS")
    files : list[File] = Field(description="list of all the files required for the project to be made, each with a 'path' and 'purpose' ")
    features : list[str] = Field(description="list of all the features that will be in this app. Eg : Data visualisation , Authetication, Reset button")

class ImplementationTask(BaseModel):
    file_path : str = Field(description="the path of the file that needs to be modified")
    task_description :str = Field(description="This is the detailed description of the task that needs to be done ")
    
class TaskPlan(BaseModel):
    implementation_steps : list[ImplementationTask] = Field("List of steps that needs to be tasken to implement a task")
    model_config = ConfigDict(extra="allow")
    
class CoderState(BaseModel):
    task_plan : TaskPlan = Field(description="The plan for the task to be implemented")
    current_step_index :int = Field(0,description="The index of the current step in the implementation step")
    current_file_content: Optional[str] = Field(None,description="Content of the file the is currently being edited or created")    