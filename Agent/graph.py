from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from prompts import *
from states import *
from langgraph.graph import StateGraph
from langsmith import traceable
load_dotenv()
llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.9)

@traceable  
def planner_agent(state:dict)->dict:
    users_prompt = state["user_prompt"]    
    resp = llm.with_structured_output(Plan).invoke(user_prompt)
    if resp is None :
        raise ValueError("Planner did not return a valid response")
    return{
        "plan":resp
    }
@traceable   
def architech_agent(state:dict)->dict:
    plan:Plan = state["plan"]
    resp = llm.with_structured_output(TaskPlan).invoke(architech_prompt(plan))   #architech_prompt will add system prompt for architech agent + plan prompt
    if resp is None: 
        raise ValueError("Architech didn't return a valid response") 
    resp.plan = plan # this adds plan variable to the TaskPlan object i.e resp and model_config helped us do that
    return {
        "task_steps":resp
    }

@traceable
def coder_agent(state:dict)->dict:
    task_step:TaskPlan = state["task_steps"]
    


    
user_prompt = "Create a simple calculator web application"
planner_prompt = planner_prompt(user_prompt=user_prompt)
graph = StateGraph(dict)

graph.add_node("planner",planner_agent)
graph.add_node("architech",architech_agent)
graph.add_node("coder",coder_agent)

graph.add_edge("planner","architech")
graph.set_entry_point("planner")

agent=graph.compile()

resp = agent.invoke({"user_prompt":user_prompt})
print(resp)
