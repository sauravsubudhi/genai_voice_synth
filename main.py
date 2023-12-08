import os
from func import final
import uvicorn
from fastapi import FastAPI,Query,HTTPException
from fastapi import FastAPI, HTTPException
import json

app = FastAPI()
@app.post("/final_endpoint")
async def final_1(request_data: dict):
    try:
        time_range_list = eval(request_data.get("time_range_list", ""))
        transcript = eval(request_data.get("transcript", ""))
        fu = final(time_range_list, transcript)
        return {"final_enhanced_list": fu}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
