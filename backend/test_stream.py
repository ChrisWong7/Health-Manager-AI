import httpx
import asyncio
import json
import sys

# Force UTF-8 encoding for stdout on Windows
sys.stdout.reconfigure(encoding='utf-8')

async def test_stream():
    url = "http://localhost:8000/api/v1/stream_query"
    payload = {"query": "高血压需要终身服药吗？"}
    
    print(f"Connecting to {url}...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            async with client.stream("POST", url, json=payload) as response:
                if response.status_code != 200:
                    print(f"Error: {response.status_code}")
                    return

                print("Stream connected. Waiting for events...")
                async for line in response.aiter_lines():
                    if line.startswith("event:"):
                        event_type = line.split(": ", 1)[1]
                        print(f"\n[Event: {event_type}]")
                    elif line.startswith("data:"):
                        data = line.split(": ", 1)[1]
                        if data.startswith("{") or data.startswith("["):
                             # Likely JSON (sources)
                             print(f"Data (JSON): {data[:50]}...")
                        else:
                             # Text chunk
                             print(f"Chunk: {data}", end="|")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_stream())
