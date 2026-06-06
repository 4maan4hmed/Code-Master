
def planner_prompt(user_prompt :str):
    planner_prompt = f"""
    You are a planner agent. Convert the user_prompt into a complete software engineer plan that is not too advance and fairly simple in nature.
    
    User Prompt :
    {user_prompt}
    """
    return planner_prompt