import os
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from main import InferencePipeline
import shutil

app = FastAPI()

pipe = InferencePipeline()

@app.get("/")
async def root():
    return {"message": "OK"}

@app.post("/store-pdf/")
async def store_pdf(file: UploadFile):
    try:
        pdf_dir = "./data/raw/"
        os.makedirs(pdf_dir, exist_ok=True) 
        pdf_path = f"./data/raw/{file.filename}"
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        pipe.store_pdf_db([pdf_path])
        return {"message": "PDF stored successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/query/")
async def query_db(query: str = Form(...)):
    result = pipe.result(query)
    return JSONResponse(content={"response": result})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)