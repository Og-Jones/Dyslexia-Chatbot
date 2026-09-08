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
    sections: list[str]
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

    sources_by_url: dict[str, dict] = {}

    for metadata in metadatas:
        
        # Sources must be from unique URLs
        url = metadata["url"]
        normalised_url = url.rstrip("/") # remove trailing slah for comparrison
        
        section = metadata.get("section")
        
        if normalised_url not in sources_by_url:
            sources_by_url[normalised_url] = {
                "source": metadata["source"],
                "title": metadata["title"],
                "sections": [],
                "url": url,
            }
        
        sections = sources_by_url[normalised_url]["sections"]

        if section and section not in sections:
            sections.append(section)
            
    sources = [
        SourceResponse(**source)
        for source in sources_by_url.values()
    ]

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