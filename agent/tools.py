@tool
async def sql_analytics(query_type: str, limit: int = 5) -> str:
    """Executes aggregate SQL analytical queries for post sentiment and counts."""
    async with pool.acquire() as conn:
        if query_type == "most_positive_posts":
            sql = """
                SELECT p.id, p.title, COUNT(c.id) AS positive_comment_count, 
                       ROUND(AVG(c.sentiment_score), 2) AS avg_score
                FROM posts p JOIN comments c ON p.id = c.post_id
                WHERE c.sentiment = 'positive'
                GROUP BY p.id, p.title ORDER BY positive_comment_count DESC LIMIT $1;
            """
        elif query_type == "most_negative_posts":
            sql = """
                SELECT p.id, p.title, COUNT(c.id) AS negative_comment_count,
                       ROUND(AVG(c.sentiment_score), 2) AS avg_score
                FROM posts p JOIN comments c ON p.id = c.post_id
                WHERE c.sentiment = 'negative'
                GROUP BY p.id, p.title ORDER BY negative_comment_count DESC LIMIT $1;
            """
        else:
            return json.dumps({"error": f"Invalid query_type: {query_type}"})

        rows = await conn.fetch(sql, limit)
        return json.dumps([dict(r) for r in rows], default=str)


@tool
async def vector_search(query_text: str, limit: int = 4) -> str:
    """Performs semantic vector search across knowledge base when searching general topics."""
    embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")
    query_vector = await embeddings_model.aembed_query(query_text)

    async with pool.acquire() as conn:
        sql = """
            SELECT source_type, source_id, post_id, content,
                   1 - (embedding <=> $1::vector) AS similarity
            FROM knowledge_base ORDER BY embedding <=> $1::vector LIMIT $2;
        """
        rows = await conn.fetch(sql, str(query_vector), limit)
        return json.dumps([dict(r) for r in rows], default=str)


@tool
async def post_details_by_id(post_id: str) -> str:
    """Fetches full body text and all attached comments for a single known Post UUID."""
    async with pool.acquire() as conn:
        sql = """
            SELECT p.id AS post_id, p.title, p.body AS post_body,
                   COALESCE(
                       json_agg(
                           json_build_object('comment_id', c.id, 'body', c.body, 'sentiment', c.sentiment)
                       ) FILTER (WHERE c.id IS NOT NULL), '[]'
                   ) AS comments
            FROM posts p LEFT JOIN comments c ON p.id = c.post_id
            WHERE p.id = $1::uuid GROUP BY p.id;
        """
        row = await conn.fetchrow(sql, post_id)
        if not row:
            return json.dumps({"error": f"Post ID {post_id} not found."})
        
        data = dict(row)
        data['comments'] = json.loads(data['comments']) if isinstance(data['comments'], str) else data['comments']
        return json.dumps(data, default=str)