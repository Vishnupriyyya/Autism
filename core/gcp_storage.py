"""
GCP Cloud Storage integration for media files (images, audio, video).
Use with django-storages for production deployment.

Environment variables for GCP:
- GOOGLE_APPLICATION_CREDENTIALS: Path to service account JSON
- GCP_STORAGE_BUCKET: Bucket name for media files
"""

import os

# Optional: Use django-storages for GCP
# from google.cloud import storage

def get_media_url(path):
    """Return full media URL; in GCP mode, returns Cloud Storage public URL."""
    bucket = os.environ.get("GCP_STORAGE_BUCKET")
    if bucket:
        return f"https://storage.googleapis.com/{bucket}/{path}"
    return f"/media/{path}"
