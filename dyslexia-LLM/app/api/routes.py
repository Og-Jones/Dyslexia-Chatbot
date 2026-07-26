from fastapi import APIRouter
from pydantic import BaseModel
from app.generation.generate import generate_answer

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str


class SourceResponse(BaseModel):
    source: str
    title: str
    section: str
    url: str


class AnswerResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]
    
@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest,):

    answer, metadatas = generate_answer(query=request.question)

    sources = []

    displayed_sources = set()

    for metadata in metadatas:

        source_key = (
            metadata["source"],
            metadata["title"],
            metadata["section"],
            metadata["url"],
        )

        if source_key in displayed_sources:
            continue

        displayed_sources.add(source_key)

        sources.append(
            SourceResponse(
                source=metadata["source"],
                title=metadata["title"],
                section=metadata["section"],
                url=metadata["url"],
            )
        )

    return AnswerResponse(
        answer=answer,
        sources=sources,
    )