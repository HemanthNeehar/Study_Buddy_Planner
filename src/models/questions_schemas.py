from pydantic import BaseModel, Field, validator
from typing import List, Any

class MCQQuestion(BaseModel):
    question: str=Field(description="The question text")
    options: List[str] = Field(description="List of 4 options")
    correct_answer: str = Field(description="The correct answer from the options")

    @validator('question', pre=True)
    def clean_question(cls, v):
        if isinstance(v,dict):
            return v.get('description', str(v))
        return str(v)
    
class FillBlankQuestion(BaseModel):
    question: str = Field(description = "The question text with '____' for the blank")
    answer:str = Field(description = "The correct word or phrase for the blank")

    @validator('question', pre=True)
    def clean_question(cls, v):
        if isinstance(v,dict):
            return '' if v.get('description', str(v)) is None else v.get('description', str(v))
        return '' if v is None else str(v)