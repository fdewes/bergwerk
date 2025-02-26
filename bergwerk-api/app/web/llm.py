from service import llm as service
from fastapi import APIRouter

router = APIRouter(prefix="/llm")

@router.post("/llm")
@router.post("/llm/")
def query_llm(data: str) -> str:
    r = service.query_llm(data)
    return r

@router.get("/llm")
@router.get("/llm/")
def query_llm():
    r = service.query_llm("Please generate a Lorem ipsum paragraph")
    return r


@router.get("/llm_training_data")
@router.get("/llm_training_data/")
def llm_training_data():
    service.llm_training_data()
