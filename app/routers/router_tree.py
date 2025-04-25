from fastapi import APIRouter, HTTPException
from ..models.csv_data import CSVData
import io, csv
from ..core.tree.tree import build_tree, to_json, classify

tags = ["Tree"]
router_tree = APIRouter(
    prefix="/tree"
)

cached_trees = {}
cached_headers = {}


@router_tree.post("/build", tags=tags)
async def build_router(data: CSVData):
    try:
        f = io.StringIO(data.csv_text)
        reader = list(csv.reader(f))
        if len(reader) < 2:
            raise ValueError("Недостаточно данных")

        header = reader[0]
        data = reader[1:]
        tree = build_tree(data, header[:-1])

        cached_trees[data.session_id] = tree
        cached_headers[data.session_id] = header

        tree_json = to_json(tree)
        return {"tree": tree_json}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при построении дерева: {e}")


@router_tree.post("/classify", tags=tags)
async def classify_router(data: CSVData):
    f = io.StringIO(data.csv_text)
    reader = list(csv.reader(f))
    if len(reader) < 1:
        raise HTTPException(status_code=400, detail="Введите данные для принятия решения!")

    session_id = data.session_id

    if session_id not in cached_trees:
        raise HTTPException(status_code=400, detail="Дерево не найдено!")

    tree = cached_trees[session_id]
    headers = cached_headers[session_id]

    results = [
        classify(tree, headers, row)
        for row in reader
    ]

    return {"results": results}
