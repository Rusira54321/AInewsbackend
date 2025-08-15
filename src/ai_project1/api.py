from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from datetime import datetime
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
# Load environment variables first
# Try to find .env file in different locations
env_paths = [
    os.path.join(os.path.dirname(__file__), "..", "..", ".env"),  # project root
    os.path.join(os.path.dirname(__file__), "..", ".env"),        # src folder
    ".env"                                                        # current directory
]

for env_path in env_paths:
    if os.path.exists(env_path):
        print(f"Loading .env from: {env_path}")
        load_dotenv(env_path)
        break
else:
    print("Warning: No .env file found")

# Check if API keys are loaded
openai_key = os.getenv("OPENAI_API_KEY")
serper_key = os.getenv("SERPER_API_KEY")

print(f"OpenAI API Key loaded: {'Yes' if openai_key else 'No'}")
print(f"Serper API Key loaded: {'Yes' if serper_key else 'No'}")

# Try to import the crew, handle import errors gracefully
try:
    # Try different import paths
    try:
        from crew import AiProject1
        CREW_AVAILABLE = True
    except ImportError:
        try:
            from src.ai_project1.crew import AiProject1
            CREW_AVAILABLE = True
        except ImportError:
            from ai_project1.src.ai_project1.crew import AiProject1
            CREW_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import crew: {e}")
    CREW_AVAILABLE = False

app = FastAPI(title="AI News Generator API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ai-news-generator-frontend-69x4vhkzr-rusira-dinujayas-projects.vercel.app"],  # Or your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class TopicRequest(BaseModel):
    topic: str
    current_year: str = "2025"

@app.get("/")
async def root():
    return {
        "message": "AI News Generator API", 
        "crew_available": CREW_AVAILABLE,
        "openai_key_loaded": bool(openai_key),
        "serper_key_loaded": bool(serper_key)
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "crew_available": CREW_AVAILABLE,
        "openai_key_loaded": bool(openai_key),
        "serper_key_loaded": bool(serper_key)
    }

@app.post("/generate-news")
async def generate_news(request: TopicRequest):
    if not CREW_AVAILABLE:
        raise HTTPException(status_code=500, detail="Crew not available - check imports")
    
    if not openai_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not found in environment variables")
    
    try:
        # Generate filename
        filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_news_article"
        
        # Prepare inputs for the crew
        inputs = {
            'topic': request.topic,
            'current_year': request.current_year,
            'filename': filename
        }
        
        # Run the crew
        crew = AiProject1().crew()
        result = crew.kickoff(inputs=inputs)
        
        # Check if the PDF was created with our filename
        news_dir = os.path.join(os.path.dirname(__file__), "..", "..", "news")
        pdf_path = os.path.join(news_dir, f"{filename}.pdf")
        
        if os.path.exists(pdf_path):
            return {
                "message": "News generated successfully",
                "pdf_filename": f"{filename}.pdf",
                "result": str(result)
            }
        else:
            return {"message": "No PDF generated", "result": str(result)}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download-pdf/{filename}")
async def download_pdf(filename: str):
    news_dir = os.path.join(os.path.dirname(__file__), "..", "..", "news")
    pdf_path = os.path.join(news_dir, filename)
    
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF not found")
    
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=filename
    )

@app.get("/list-pdfs")
async def list_pdfs():
    news_dir = os.path.join(os.path.dirname(__file__), "..", "..", "news")
    pdf_files = [f for f in os.listdir(news_dir) if f.endswith('.pdf')]
    
    return {"pdf_files": pdf_files}

if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI server...")
    print("Swagger UI will be available at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
