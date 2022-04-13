from typing import Optional

from pydantic import BaseModel, Field




class GPTSchema(BaseModel):
    """GPT Q&A Model"""

    db_schema: list = Field(..., description="Database Schema")
    question: str = Field(..., title="Question", description="Question from User")
    settings: dict = Field(..., title="Settings", description="Settings for the Question")
    class Config:
        schema_extra = {
            "example" : {
                "db_schema" : ["id_field : text_FIELD" , "name_field : text_TYPE", "score_field : text_TYPE" ],
                "question" : "tell me all name havng age more than 6",
                "settings": {
                    "temperature" : 0.75,
                    "num_beams" : 10,
                    "top_p" : 0.6,
                    "top_k" : 50,
                }
            }
        }
