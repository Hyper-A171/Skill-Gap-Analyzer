import re

def clean_text(text):
    """
    Normalizes text while strictly preserving symbols for skills like C++, C#, and .NET.
    """
    if not text:
        return ""
    
    # Convert to lowercase for consistent processing
    text = text.lower()
    
    # Replace newlines and tabs with spaces
    text = re.sub(r'[\n\t\r]', ' ', text)
    
    # Remove special characters except for +, #, and . (to preserve C++, C#, .NET)
    # Also keep alphanumeric characters and spaces
    text = re.sub(r'[^a-z0-9\s\+#\.]', ' ', text)
    
    # Collapse multiple spaces into one
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
