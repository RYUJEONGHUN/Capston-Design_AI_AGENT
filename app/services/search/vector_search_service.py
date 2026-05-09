from app.core.factory import embeddings
from app.data.mongo import db
from app.services.search.search_pipeline import (
    build_search_pipeline,
    build_vector_search_config,
)


async def run_vector_search(
    query: str,
    target_category: str | None = None,
    region: str | None = None,
    require_naegift: bool = False,
    limit: int = 5,
    score_threshold: float = 0.45,
) -> list[dict]:
    query_vector = await embeddings.aembed_query(query)

    search_config = build_vector_search_config(
        query_vector=query_vector,
        target_category=target_category,
        require_naegift=require_naegift,
        num_candidates=100,
        limit=15,
    )

    pipeline = build_search_pipeline(search_config, region=region)

    cursor = db.incheon_contents.aggregate(pipeline)
    results = await cursor.to_list(length=limit)

    filtered_results = [
        r for r in results if r.get("score", 0) >= score_threshold
    ]

    return filtered_results