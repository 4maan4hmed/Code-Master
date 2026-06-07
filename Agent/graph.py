from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from tools import get_current_directory, list_files, read_file, run_cmd, write_file
from prompts import *
from states import *
from langgraph.graph import END, StateGraph
from langsmith import traceable
load_dotenv()
from config import planner_llm, architect_llm, coder_llm

@traceable  
def planner_agent(state:dict)->dict:
    user_prompt = state["user_prompt"]    
    resp = planner_llm.with_structured_output(Plan).invoke(user_prompt)
    if resp is None :
        raise ValueError("Planner did not return a valid response")
    return{
        "plan":resp
    }
@traceable   
def architech_agent(state:dict)->dict:
    plan:Plan = state["plan"]
    resp = architect_llm.with_structured_output(TaskPlan).invoke(architech_prompt(plan))   #architech_prompt will add system prompt for architech agent + plan prompt
    if resp is None: 
        raise ValueError("Architech didn't return a valid response") 
    resp.plan = plan # this adds plan variable to the TaskPlan object i.e resp and model_config helped us do that
    return {
        "task_steps":resp
    }

@traceable
def coder_agent(state:dict)->dict:
    
    coder_state = state.get("coder_state")
    
    if coder_state is None:
        coder_state = CoderState(task_plan=state["task_steps"],current_step_index=0)
    steps= coder_state.task_plan.implementation_steps #list of all the task that need to be implimented
    current_task_index = coder_state.current_step_index
    if(current_task_index>=len(steps)):
        return {"coder_state":coder_state,"status":"DONE"} 
    current_task = steps[current_task_index]
    path = current_task.file_path
    description = current_task.task_description
    existing_content = read_file.run(path)
    user_prompt =(f"task:{description}\n"
                  f"path:{path}\n"
                  f"Existing Content:{existing_content}\n"
                  "Use write_file tool(path,content) to write the content to the path"
                  )
    system_prompt = coder_system_prompt()
    coder_tools = [write_file,read_file,list_files,get_current_directory,run_cmd]
    coder_agent_with_tools = create_agent(coder_llm,coder_tools)
    coder_agent_with_tools.invoke({
        "messages":[
            {
                "role":"system", "content":system_prompt
            },
            {
                "role":"user","content":user_prompt
            }
        ]
    })
    coder_state.current_step_index+=1
    return {
        "coder_state":coder_state
    }
    


    
user_prompt = "Create a simple calculator web application"
planner_prompt = planner_prompt(user_prompt=user_prompt)
graph = StateGraph(dict)

graph.add_node("planner",planner_agent)
graph.add_node("architech",architech_agent)
graph.add_node("coder",coder_agent)

graph.add_edge("planner","architech")
graph.add_edge("architech","coder")
graph.add_conditional_edges("coder",
                            lambda s: "END" if s.get("status") == "DONE" else "coder",
                            {
                                "coder":"coder",
                                "END":END
                            }
                            )
graph.set_entry_point("planner")

agent=graph.compile()

resp = agent.invoke({"user_prompt":user_prompt})
