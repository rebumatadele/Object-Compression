from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
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
    data: bytes  # Expecting raw bytes for decompression

@app.post("/compress/gzip/raw/")
async def compress_gzip_raw(request: CompressRequest):
    """Compress data using Gzip and return raw bytes."""
    try:
        json_data = str(request.data).encode('utf-8')  # Convert dict to bytes
        compressed_data = compress_with_gzip(json_data)
        return Response(content=compressed_data, media_type="application/octet-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compress/gzip/base64/")
async def compress_gzip_base64(request: CompressRequest):
    """Compress data using Gzip and return base64-encoded string."""
    try:
        json_data = str(request.data).encode('utf-8')  # Convert dict to bytes
        compressed_data = compress_with_gzip(json_data)
        return {"compressed_data": base64.b64encode(compressed_data).decode('utf-8')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compress/brotli/raw/")
async def compress_brotli_raw(request: CompressRequest):
    """Compress data using Brotli and return raw bytes."""
    try:
        json_data = str(request.data).encode('utf-8')  # Convert dict to bytes
        compressed_data = compress_with_brotli(json_data)
        return Response(content=compressed_data, media_type="application/octet-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compress/brotli/base64/")
async def compress_brotli_base64(request: CompressRequest):
    """Compress data using Brotli and return base64-encoded string."""
    try:
        json_data = str(request.data).encode('utf-8')  # Convert dict to bytes
        compressed_data = compress_with_brotli(json_data)
        return {"compressed_data": base64.b64encode(compressed_data).decode('utf-8')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/decompress/gzip/")
async def decompress_gzip(request: DecompressRequest):
    """Decompress Gzip data from raw bytes."""
    try:
        compressed_data = base64.b64decode(request.data)
        decompressed_data = decompress_with_gzip(compressed_data)
        return {"decompressed_data": decompressed_data.decode('utf-8')}  # Return as JSON
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/decompress/brotli/")
async def decompress_brotli(request: DecompressRequest):
    """Decompress Brotli data from raw bytes."""
    try:
        compressed_data = base64.b64decode(request.data)
        decompressed_data = decompress_with_brotli(compressed_data)
        return {"decompressed_data": decompressed_data.decode('utf-8')}  # Return as JSON
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))