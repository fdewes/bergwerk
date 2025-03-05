import io
from fastapi import APIRouter, HTTPException, Response, UploadFile
from data import wiki as data_wiki
from error import Unauthorized
from datetime import datetime
import json
from icecream import ic

router = APIRouter(prefix="/admin")


@router.get("")
@router.get("/")
def admin_endpoint() -> str:
    return ":o"


@router.get("/build_intent_classifier/{token}")
@router.get("/build_intent_classifier/{token}/")
def build_intent_classifier(token: str) -> None:
    if not data_wiki.check_admin_token(token):
        raise HTTPException(status_code=403, detail="Incorrect token.")
    try:
        data_wiki.build_intent_classifier(token=token)
    except Unauthorized as exc:
        raise HTTPException(status_code=403, detail=exc.msg)


@router.get("/export/{token}")
@router.get("/export/{token}/")
def export_json(token: str):
    if not data_wiki.check_admin_token(token):
        raise HTTPException(status_code=403, detail="Incorrect token.")

    all_pages = data_wiki.get_all_pages_of_category("Content")
    export = {title: data_wiki.get_entire_page(title) for title in all_pages}
    json_data = json.dumps(export)

    date = datetime.now().strftime("%Y%m%d")
    headers = {
        'Content-Disposition': f'attachment; filename="export_{date}.json"'
    }

    return Response(content=json_data, media_type="application/json", headers=headers)


@router.post("/import/{token}")
@router.post("/import/{token}/")
async def import_json(file: UploadFile, token: str):
    if not data_wiki.check_admin_token(token):
        raise HTTPException(status_code=403, detail="Incorrect token.")

    file_content = await file.read()

    try:
        deserialized_data = json.loads(file_content)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON file: {e}")

    for title, text in deserialized_data.items():
        if title.lower() in ("configuration", "token"):
            print(f"Skipping {title}.")
            continue
        print(f"Creating page {title}.")
        data_wiki.create_or_update_page(title, text)
