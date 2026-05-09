import pandas as pd
from pymongo import MongoClient
from pathlib import Path

MONGO_URI = "mongodb+srv://junghunryu4_db_user:fbwjdgns369@incheonmate-cluster.xuaucw1.mongodb.net/?appName=IncheonMate-cluster"
DB_NAME = "IncheonMate"
COLLECTION_NAME = "incheon_contents"

BASE_DIR = Path(__file__).resolve().parents[2]
EXCEL_PATH = BASE_DIR / "IncheonMate.xlsx"

SHEET_CATEGORY_MAP = {
    "식당": "restaurants",
    "관광지": "places",
    "카페": "cafes",
    "숙박": "stays",
}

COLUMN_RENAME_MAP = {
    "Image": "ImageURL",
    "image": "ImageURL",
    "#NAME?": "Mbti",   # 관광지 시트 헤더 깨짐 대응
}

INVALID_STRING_VALUES = {
    "",
    "-",
    "미제공",
    "nan",
    "none",
    "null",
    "#NAME?",
}


def to_none(value):
    if pd.isna(value):
        return None

    if isinstance(value, str):
        value = value.strip()
        if value.lower() in INVALID_STRING_VALUES:
            return None

    return value


def to_string(value):
    value = to_none(value)
    if value is None:
        return None
    return str(value).strip()


def to_float(value):
    value = to_none(value)
    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def to_bool(value):
    value = to_none(value)
    if value is None:
        return False

    if isinstance(value, bool):
        return value

    if isinstance(value, (int, float)):
        return bool(value)

    if isinstance(value, str):
        v = value.strip().lower()
        if v in {"true", "1", "y", "yes", "o"}:
            return True
        if v in {"false", "0", "n", "no", "x"}:
            return False

    return False


def parse_tags(value):
    value = to_none(value)
    if value is None:
        return []

    if isinstance(value, list):
        raw_parts = value
    else:
        raw_parts = str(value).replace(",", " ").split()

    tags = []
    seen = set()

    for part in raw_parts:
        part = str(part).strip()
        if not part:
            continue
        if part.startswith("#"):
            part = part[1:]
        part = part.strip()

        if not part:
            continue
        if part.lower() in INVALID_STRING_VALUES:
            continue

        if part not in seen:
            seen.add(part)
            tags.append(part)

    return tags


def parse_single_or_list(value):
    value = to_none(value)
    if value is None:
        return []

    if isinstance(value, str):
        raw_parts = value.replace(",", " ").replace("/", " ").split()
    else:
        raw_parts = [value]

    items = []
    seen = set()

    for part in raw_parts:
        part = to_string(part)
        if not part:
            continue
        if part not in seen:
            seen.add(part)
            items.append(part)

    return items


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    renamed = {}
    for col in df.columns:
        col_str = str(col).strip()
        renamed[col] = COLUMN_RENAME_MAP.get(col_str, col_str)
    return df.rename(columns=renamed)


def get_subcategory(row: dict):
    # 새 파일은 SubCategory 우선
    value = to_string(row.get("SubCategory"))
    if value:
        return value

    # 혹시 예전 형식 잔존 시 대응
    value = to_string(row.get("음식 구분"))
    if value:
        return value

    return None


def normalize_row(sheet_name: str, row: dict) -> dict:
    doc = {
        "PlaceName": to_string(row.get("PlaceName")),
        "Address": to_string(row.get("Address")),
        "PlaceCategory": to_string(row.get("PlaceCategory")),
        "category": SHEET_CATEGORY_MAP[sheet_name],
        "subCategory": get_subcategory(row),
        "Region": to_string(row.get("Region")),
        "X": to_float(row.get("X")),
        "Y": to_float(row.get("Y")),
        "KakaoId": to_string(row.get("KakaoId")),
        "naegiftId": to_string(row.get("naegiftId")),
        "Rating": to_float(row.get("Rating")),
        "Mbti": to_string(row.get("Mbti")),
        "Sasang": to_string(row.get("Sasang")),
        "mbtiTags": parse_single_or_list(row.get("Mbti")),
        "sasangTags": parse_single_or_list(row.get("Sasang")),
        "Tags": parse_tags(row.get("Tags")),
        "Comment": to_string(row.get("Comment")),
        "ImageURL": to_string(row.get("ImageURL")),
        "isFamily": to_bool(row.get("isFamily")),
        "isSole": to_bool(row.get("isSole")),
        "isCouple": to_bool(row.get("isCouple")),
        "isFriend": to_bool(row.get("isFriend")),
        "sourceSheet": sheet_name,
    }

    return doc


def is_valid_document(doc: dict) -> bool:
    if not doc["PlaceName"]:
        return False

    # 좌표는 유지하는 게 search/course에 유리
    if doc["X"] is None or doc["Y"] is None:
        return False

    return True


def load_excel_to_documents(excel_path: Path) -> list[dict]:
    excel_file = pd.ExcelFile(excel_path)
    all_docs = []

    for sheet_name in excel_file.sheet_names:
        if sheet_name not in SHEET_CATEGORY_MAP:
            print(f"[SKIP] 매핑되지 않은 시트: {sheet_name}")
            continue

        df = pd.read_excel(excel_path, sheet_name=sheet_name)
        df = normalize_columns(df)

        records = df.to_dict(orient="records")
        sheet_docs = []

        for row in records:
            doc = normalize_row(sheet_name, row)

            if is_valid_document(doc):
                sheet_docs.append(doc)

        print(f"[OK] {sheet_name}: {len(sheet_docs)}개 문서 준비 완료")
        all_docs.extend(sheet_docs)

    return all_docs


def main():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    documents = load_excel_to_documents(EXCEL_PATH)

    if not documents:
        print("업로드할 문서가 없습니다.")
        return

    result = collection.insert_many(documents)
    print(f"[DONE] 업로드 완료: {len(result.inserted_ids)}개 문서")


if __name__ == "__main__":
    main()