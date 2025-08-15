#!/usr/bin/env python3
"""
Test script for the AI News Generator API
Run this after starting the API server
"""

import requests
import time
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_api():
    """Test the API endpoints"""
    
    print("🚀 Testing AI News Generator API")
    print("=" * 50)
    
    # Test root endpoint
    print("\n1. Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Root endpoint: {response.json()}")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
        return
    
    # Test list available topics
    print("\n2. Testing list available topics...")
    try:
        response = requests.get(f"{BASE_URL}/list-available-topics")
        print(f"✅ Available topics: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ List topics failed: {e}")
    
    # Test news generation
    print("\n3. Testing news generation...")
    topic_data = {
        "topic": "artificial intelligence trends 2025",
        "current_year": "2025"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/generate-news", json=topic_data)
        if response.status_code == 200:
            result = response.json()
            task_id = result["task_id"]
            print(f"✅ News generation started: {result}")
            
            # Poll for task completion
            print(f"\n4. Polling for task completion (Task ID: {task_id})...")
            max_attempts = 30  # Wait up to 5 minutes
            attempt = 0
            
            while attempt < max_attempts:
                time.sleep(10)  # Wait 10 seconds between checks
                attempt += 1
                
                try:
                    status_response = requests.get(f"{BASE_URL}/task-status/{task_id}")
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        print(f"   Attempt {attempt}: Status = {status_data['status']}")
                        
                        if status_data['status'] == 'completed':
                            print(f"✅ Task completed! PDF path: {status_data.get('pdf_path')}")
                            
                            # Test PDF download
                            print(f"\n5. Testing PDF download...")
                            download_response = requests.get(f"{BASE_URL}/download-pdf/{task_id}")
                            if download_response.status_code == 200:
                                print(f"✅ PDF download successful! Size: {len(download_response.content)} bytes")
                                
                                # Save the PDF locally
                                with open(f"downloaded_news_{task_id}.pdf", "wb") as f:
                                    f.write(download_response.content)
                                print(f"✅ PDF saved as: downloaded_news_{task_id}.pdf")
                            else:
                                print(f"❌ PDF download failed: {download_response.status_code}")
                            
                            break
                        elif status_data['status'] == 'failed':
                            print(f"❌ Task failed: {status_data.get('error', 'Unknown error')}")
                            break
                    else:
                        print(f"   Attempt {attempt}: Failed to get status")
                        
                except Exception as e:
                    print(f"   Attempt {attempt}: Error checking status: {e}")
            
            if attempt >= max_attempts:
                print("⏰ Timeout waiting for task completion")
                
        else:
            print(f"❌ News generation failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ News generation request failed: {e}")

if __name__ == "__main__":
    test_api()
