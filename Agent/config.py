from langchain_groq import ChatGroq

PLANNER_MODEL = "openai/gpt-oss-20b"
ARCHITECT_MODEL = "openai/gpt-oss-20b"
CODER_MODEL = "openai/gpt-oss-120b"

planner_llm = ChatGroq(
    model=PLANNER_MODEL,
    temperature=0.2
)

architect_llm = ChatGroq(
    model=ARCHITECT_MODEL,
    temperature=0.2
)

coder_llm = ChatGroq(
    model=CODER_MODEL,
    temperature=0.2
)