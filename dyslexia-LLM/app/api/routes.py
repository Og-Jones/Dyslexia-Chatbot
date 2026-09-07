from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, Field

from app.generation.generate import generate_answer
from app.generation.speech import generate_speech


router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

class SpeechRequest(BaseModel):
    text: str = Field(min_length=1, max_length=4096)

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
    
@router.post("/speech")
def create_speech(request: SpeechRequest):
    try:
        audio = generate_speech(request.text)

        return Response(
            content=audio,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": 'inline; filename="response.mp3"',
                "Cache-Control": "no-store",
            },
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Unable to generate speech.",
        ) from error