from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import gzip
import brotli
import base64
from typing import Any, Dict

app = FastAPI()

def compress_with_gzip(data: bytes) -> bytes:
    """Compress data using Gzip."""
    return gzip.compress(data)

def compress_with_brotli(data: bytes) -> bytes:
    """Compress data using Brotli."""
    return brotli.compress(data)

def decompress_with_gzip(data: bytes) -> bytes:
    """Decompress Gzip data."""
    return gzip.decompress(data)

def decompress_with_brotli(data: bytes) -> bytes:
    """Decompress Brotli data."""
    return brotli.decompress(data)

class CompressRequest(BaseModel):
    data: Dict[str, Any]  # Accept any complex JSON structure

class DecompressRequest(BaseModel):
    data: str  # Expecting base64-encoded string

@app.post("/compress/gzip/")
async def compress_gzip(request: CompressRequest):
    """Compress data using Gzip."""
    try:
        json_data = str(request.data).encode('utf-8')  # Convert dict to bytes
        compressed_data = compress_with_gzip(json_data)
        # Return the compressed data as a base64-encoded string
        return {"compressed_data": base64.b64encode(compressed_data).decode('utf-8')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compress/brotli/")
async def compress_brotli(request: CompressRequest):
    """Compress data using Brotli."""
    try:
        json_data = str(request.data).encode('utf-8')  # Convert dict to bytes
        compressed_data = compress_with_brotli(json_data)
        # Return the compressed data as a base64-encoded string
        return {"compressed_data": base64.b64encode(compressed_data).decode('utf-8')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/decompress/gzip/")
async def decompress_gzip(request: DecompressRequest):
    """Decompress Gzip data from base64 string."""
    try:
        compressed_data = base64.b64decode(request.data)
        decompressed_data = decompress_with_gzip(compressed_data)
        return {"decompressed_data": decompressed_data.decode('utf-8')}  # Return as JSON
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/decompress/brotli/")
async def decompress_brotli(request: DecompressRequest):
    """Decompress Brotli data from base64 string."""
    try:
        compressed_data = base64.b64decode(request.data)
        decompressed_data = decompress_with_brotli(compressed_data)
        return {"decompressed_data": decompressed_data.decode('utf-8')}  # Return as JSON
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))