  import os

class Config:
    # Database configuration
    DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb://localhost:27017/")
    # Bot modes configuration
    MODES = [
        "PDF Merge",           # Mode 1
        "PDF Watermark",       # Mode 2
        "PDF Split",           # Mode 3
        "Remove Watermark",    # Mode 4
        "Text Extraction"      # Mode 5
    ]
    
    # Additional configuration options
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB limit
    ALLOWED_EXTENSIONS = ['.pdf']
    
    # Watermark settings
    WATERMARK_OPACITY = 0.3
    WATERMARK_POSITION = "center"
    
    # Queue settings
    MAX_QUEUE_SIZE = 100
    PROCESSING_TIMEOUT = 300  # 5 minutes