def build_vector_search_config(
    query_vector: list[float],
    target_category: str | None = None,
    require_naegift: bool = False,
    num_candidates: int = 100,
    limit: int = 15,
) -> dict:
    search_config = {
        "index": "vector_index",
        "path": "embedding",
        "queryVector": query_vector,
        "numCandidates": num_candidates,
        "limit": limit,
    }

    filters = []

    if target_category:
        filters.append({"category": target_category})

    if require_naegift:
        filters.append({"naegiftId": {"$ne": None}})

    if filters:
        if len(filters) == 1:
            search_config["filter"] = filters[0]
        else:
            search_config["filter"] = {"$and": filters}

    return search_config


def build_search_pipeline(search_config: dict, region: str | None = None) -> list[dict]:
    pipeline = [
        {"$vectorSearch": search_config},
        {
            "$project": {
                "PlaceName": 1,
                "Address": 1,
                "category": 1,
                "subCategory": 1,
                "Region": 1,
                "Mbti": 1,
                "Sasang": 1,
                "mbtiTags": 1,
                "sasangTags": 1,
                "Comment": 1,
                "X": 1,
                "Y": 1,
                "ImageURL": 1,
                "Rating": 1,
                "Tags": 1,
                "naegiftId": 1,
                "isFamily": 1,
                "isSole": 1,
                "isCouple": 1,
                "isFriend": 1,
                "KakaoId" : 1,
                "score": {"$meta": "vectorSearchScore"},
            }
        },
    ]

    if region:
        pipeline.append(
            {
                "$match": {
                    "$or": [
                        {"Address": {"$regex": region, "$options": "i"}},
                        {"Region": {"$regex": region, "$options": "i"}},
                        {"PlaceName": {"$regex": region, "$options": "i"}},
                    ]
                }
            }
        )

    return pipeline