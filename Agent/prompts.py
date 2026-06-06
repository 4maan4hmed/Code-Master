
def planner_prompt(user_prompt :str):
    planner_prompt = f"""
    You are a planner agent. Convert the user_prompt into a complete software engineer plan that is not too advance and fairly simple in nature.
    
    User Prompt :
    {user_prompt}
    """
    return planner_prompt

def architech_prompt(plan: str):
    architech_prompt = f"""
You are the ARCHITECT agent. Given this project plan, break it down into explicit engineering tasks.

RULES:
- For each FILE in the plan, create one or more IMPLEMENTATION TASKS.
- In each task description:
    * Specify exactly what to implement.
    * Name the variables, functions, classes, and components to be defined.
    * Mention how this task depends on or will be used by previous tasks.
    * Include integration details: imports, expected function signatures, data flow.
- Order tasks so that dependencies are implemented first.
- Each step must be SELF-CONTAINED but also carry FORWARD the relevant context from earlier tasks.

Project Plan:
{plan}
    """
    return architech_prompt
    