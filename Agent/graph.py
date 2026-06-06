from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

load_dotenv()


user_prompt = "Create a simple calculator web application"
prompt = f"You are a planner agent. Convert the user_prompt into a complete software engineer plan that is not too advance and fairly simple in nature. User Prompt : {user_prompt}"
class File(BaseModel):
    path : str = Field(description="The path of the file it will be kept in")
    purpose : str = Field(description="The purpose of the file, e.g 'main application logic', 'data processing logic'")
class Plan(BaseModel):
    name : str = Field(description="This field is the name of the app you are going to make in according to the user's prompt") 
    description : str = Field(description="A single line description of the app you are making")    
    techstack : str = Field(description="The tech stack that will be used to build this app . Eg. : Python, Javascript, HTML, CSS")
    files : list[File] = Field(description="list of all the files required for the project to be made, each with a 'path' and 'purpose' ")
    features : list[str] = Field(description="list of all the features that will be in this app. Eg : Data visualisation , Authetication, Reset button")


llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.9)
req = llm.with_structured_output(Plan).invoke("make a calculator app")
print(req)