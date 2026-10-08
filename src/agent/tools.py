from dotenv import load_dotenv
from langchain_core.tools import tool
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from langchain_postgres.vectorstores import PGVector
from langchain_huggingface import HuggingFaceEmbeddings
from ..database import async_engine
import os

load_dotenv()

LANGCHAIN_DB_URL = os.getenv("LANGCHAIN_DB_URL")
langchain_async_engine = create_async_engine(LANGCHAIN_DB_URL)

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={"device": "cpu"}, 
    encode_kwargs={"normalize_embeddings": True}
)
vector_store = PGVector(
    connection=langchain_async_engine,
    embeddings=embeddings,  
    collection_name="platform_vectors",
    use_jsonb=True,
)

@tool
async def search_vector_store(query: str, post_id: int|None = None) -> str:
    """
    Use for semantic search, natural language QA, or topic search across posts and comments.
    Filters by post_id or user_id before running similarity search.
    """
    print(f"Searching vector store for post_id={post_id} with query: {query}")  # Debugging line
    filters = {}
    if post_id is not None:
        filters["post_id"] = post_id
    # elif user_id is not None:
    #     filters["user_id"] = user_id

    results = await vector_store.asimilarity_search(
        query=query, 
        k=5, 
        filter=filters if filters else None
    )
    if not results:
        return "No semantically relevant posts or comments found."
    return "\n\n".join([doc.page_content for doc in results])


@tool
async def fetch_full_post_thread(query:str, post_id: int) -> str:
    """
    Use ONLY when the user asks to SUMMARIZE or digest a specific post and ALL of its comments.
    Queries post and comment contents asynchronously using your active AsyncSession.
    """
    print(f"Fetching full post thread for post_id={post_id} with query: {query}")  # Debugging line
    query = text("""
        SELECT 'POST: ' || p.title || ' - ' || p.content AS content, p.created_at
        FROM posts p WHERE p.id = :post_id
        UNION ALL
        SELECT 'COMMENT: ' || c.content AS content, c.created_at
        FROM comments c WHERE c.post_id = :post_id
        ORDER BY created_at ASC;
    """)
    async with AsyncSession(async_engine) as session:  
        rows = (await session.execute(query, {"post_id": post_id})).fetchall()
        
        if not rows:
            return f"No post or comment thread found for post_id={post_id}."
        
        return "\n\n".join([row[0] for row in rows])


@tool
async def database_stats_query(query: str, user_id: int, post_id: int|None = None
) -> str:
    """
    Use when the user asks for STATS, COUNTS, NUMBERS, or METADATA (e.g., 'How many posts did I make?').
    Executes aggregation SQL queries on your active AsyncSession.
    """
    print(f"Executing database stats query for user_id={user_id}, post_id={post_id} with query: {query}")  # Debugging line
    query_lower=query.lower()  
    async with AsyncSession(async_engine) as session:  
        if "my post count" in query_lower or "how many posts" in query_lower:
            result = await session.execute(text("SELECT COUNT(*) FROM posts WHERE author_id = :uid"), {"uid": user_id})
            return f"You have created a total of {result.scalar()} posts."
        
        elif post_id and "comment count" in query_lower:
            result = await session.execute(text("SELECT COUNT(*) FROM comments WHERE post_id = :pid"), {"pid": post_id})
            return f"There are {result.scalar()} comments on post #{post_id}."
        
        else:
            result = await session.execute(
                text("SELECT (SELECT COUNT(*) FROM posts WHERE author_id = :uid) + (SELECT COUNT(*) FROM comments WHERE user_id = :uid)"),
                {"uid": user_id}
                )
            return f"Total user activity items count: {result.scalar()}."