from unittest import result
from urllib import response
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from server.models.reponse import Response
import pandas as pd
from server.gpt import *

from server.models.GPT import (
    GPTSchema
)


router = APIRouter()


@router.post("/", response_description="Predict area")
async def predict_GPT(request: GPTSchema):
    data = jsonable_encoder(request)
    
    print(data)

    schema = data['db_schema']
    question = data['question']
    settings = data['settings']

    code = generate_code(schema, question, settings)
    
    
    response = {
        "sql" : code,
    }
    return Response.ResponseModel(response, "detected successfully")
