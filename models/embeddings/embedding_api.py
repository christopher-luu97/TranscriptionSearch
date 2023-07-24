import sentence_transformers
from fastapi import FastAPI, Body
import uvicorn
from pydantic import BaseModel

class TranscriptionDocument(BaseModel):
    transcription_document: str

embed = None

app = FastAPI(title="Embedding API", 
              description="API for flax-sentence-embeddings/all_datasets_v4_MiniLM-L6",
              version="1.0")
@app.on_event('startup')
async def load_model():
    global embed
    embed = sentence_transformers.SentenceTransformer('./embedding_model')

@app.post('/embed', tags=["embedding"])
async def get_prediction(transcription_document: TranscriptionDocument):
    data = transcription_document.transcription_document
    print("Received data:", data)  # Debugging line to see the received data
    prediction = embed.encode(data)  # Vectorize
    prediction = prediction.tolist()  # Convert to a JSON-serializable format (array)
    return {"vectors": prediction}

@app.get("/")
def root():
    # simple root value just to see if things work when we go to the root
    return {"Hello": "World"}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=5000)