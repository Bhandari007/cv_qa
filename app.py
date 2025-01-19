from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from main import InferencePipeline
import shutil

app = FastAPI()

pipe = InferencePipeline()

@app.post("/store-pdf/")
async def store_pdf(file: UploadFile):
    pdf_path = f"./data/raw/{file.filename}"
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    pipe.store_pdf_db([pdf_path])
    return {"message": "PDF stored successfully"}

@app.post("/query/")
async def query_db(query: str = Form(...)):
    result = pipe.result(query)
    return JSONResponse(content={"response": result})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)