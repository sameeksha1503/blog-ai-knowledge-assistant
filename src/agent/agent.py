# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from .tools import database_stats_query, search_vector_store, fetch_full_post_thread
from dotenv import load_dotenv
from langchain.agents import create_agent

tools = [database_stats_query, search_vector_store, fetch_full_post_thread]

load_dotenv()  # Load environment variables from .env file
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
)
# model = ChatGoogleGenerativeAI(
#     model="gemini-3.8-flash",
#     temperature=0
# )



SYSTEM_PROMPT = """You are an AI Assistant for a social posting platform. 
Answer the user's query accurately using the appropriate tool.

Available Context Variables:
- User ID: {user_id}
- Post ID: {post_id}

Tool Selection Guidelines:
1. If Post ID is NOT 'None' AND user asks to SUMMARIZE the thread -> Call `fetch_full_post_thread`.
2. If the query asks for NUMBERS, COUNTS, or STATS -> Call `database_stats_query`.
3. For general topic questions or semantic QA -> Call `search_vector_store`.

Note: Database sessions are supplied automatically at runtime. Focus purely on selecting the correct arguments (post_id, or query).

"""

# create_agent outputs a compiled graph directly
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)