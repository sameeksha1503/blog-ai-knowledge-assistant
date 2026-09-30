from langchain_groq import ChatGroq

tools = [sql_analytics, vector_search, post_details_by_id]

# Initialize free Groq LLM with tool calling support
model = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

system_prompt = (
    "You are an Agentic Assistant for a Post & Comment app. Select tools dynamically:\n"
    "1. `sql_analytics`: Aggregate rankings (most positive/negative posts).\n"
    "2. `vector_search`: Open semantic searches on knowledge base.\n"
    "3. `post_details_by_id`: Retrieve full post body and comments for a given ID."
)

# create_agent outputs a compiled graph directly
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt
)