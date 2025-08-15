# AI News Generator API

This FastAPI application provides endpoints for generating news articles based on topics and downloading the generated PDF files.

## Features

- **Generate News**: Submit a topic and get a task ID for news generation
- **Task Status**: Check the status of ongoing news generation tasks
- **Download PDF**: Download the generated PDF file once the task is completed
- **List Topics**: View all available topics that have been processed
- **Background Processing**: News generation runs in the background to avoid blocking

## Installation

1. Make sure you have all dependencies installed in your virtual environment:
```bash
pip install -r requirements.txt
```

## Running the API

### Option 1: Direct Python execution
```bash
cd src/ai_project1
python api.py
```

### Option 2: Using uvicorn directly
```bash
cd src/ai_project1
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Root Endpoint
- **GET** `/`
- Returns a simple message confirming the API is running

### 2. Generate News
- **POST** `/generate-news`
- **Request Body:**
```json
{
    "topic": "artificial intelligence trends 2025",
    "current_year": "2025"
}
```
- **Response:**
```json
{
    "message": "News generation started",
    "task_id": "task_20250114_123456",
    "status": "processing"
}
```

### 3. Check Task Status
- **GET** `/task-status/{task_id}`
- Returns the current status of a news generation task
- **Status values:** `processing`, `running`, `completed`, `failed`

### 4. Download PDF
- **GET** `/download-pdf/{task_id}`
- Downloads the generated PDF file (only available when task is completed)
- Returns the PDF file as a downloadable response

### 5. List Available Topics
- **GET** `/list-available-topics`
- Returns a list of all processed topics with their PDF files

## Usage Flow

1. **Submit Topic**: Send a POST request to `/generate-news` with your topic
2. **Get Task ID**: Receive a task ID in the response
3. **Monitor Progress**: Poll `/task-status/{task_id}` to check completion
4. **Download PDF**: Once completed, download the PDF from `/download-pdf/{task_id}`

## Example Frontend Integration

### JavaScript/HTML Example
```html
<!DOCTYPE html>
<html>
<head>
    <title>AI News Generator</title>
</head>
<body>
    <h1>AI News Generator</h1>
    
    <div>
        <input type="text" id="topic" placeholder="Enter topic...">
        <button onclick="generateNews()">Generate News</button>
    </div>
    
    <div id="status"></div>
    <div id="download"></div>

    <script>
        async function generateNews() {
            const topic = document.getElementById('topic').value;
            const statusDiv = document.getElementById('status');
            const downloadDiv = document.getElementById('download');
            
            try {
                // Start news generation
                const response = await fetch('/generate-news', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({topic: topic})
                });
                
                const result = await response.json();
                const taskId = result.task_id;
                
                statusDiv.innerHTML = `Task started: ${taskId}`;
                
                // Poll for completion
                const checkStatus = async () => {
                    const statusResponse = await fetch(`/task-status/${taskId}`);
                    const statusData = await statusResponse.json();
                    
                    if (statusData.status === 'completed') {
                        statusDiv.innerHTML = 'Task completed!';
                        downloadDiv.innerHTML = `<a href="/download-pdf/${taskId}">Download PDF</a>`;
                    } else if (statusData.status === 'failed') {
                        statusDiv.innerHTML = `Task failed: ${statusData.error}`;
                    } else {
                        statusDiv.innerHTML = `Status: ${statusData.status}`;
                        setTimeout(checkStatus, 5000); // Check again in 5 seconds
                    }
                };
                
                checkStatus();
                
            } catch (error) {
                statusDiv.innerHTML = `Error: ${error.message}`;
            }
        }
    </script>
</body>
</html>
```

## Testing

Run the test script to verify all endpoints work correctly:

```bash
python test_api.py
```

## Notes

- News generation can take several minutes depending on the complexity of the topic
- The API uses background tasks to avoid blocking requests
- PDF files are stored in the `news/` directory
- Task status is stored in memory (will be lost on server restart)

## Error Handling

The API includes comprehensive error handling:
- Invalid task IDs return 404 errors
- Attempting to download incomplete tasks returns 400 errors
- Server errors return 500 errors with descriptive messages

## Development

To modify the API:
1. Edit `src/ai_project1/api.py`
2. The API automatically reloads when using uvicorn with `--reload` flag
3. Check the console for any error messages during development
