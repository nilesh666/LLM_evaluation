from dotenv import load_dotenv
import os

load_dotenv()

google_api = os.getenv("GOOGLE_GEN_AI")
langfuse_public_api=os.getenv("LANGFUSE_PUBLIC_KEY")
langfuse_secret_api=os.getenv("LANGFUSE_SECRET_KEY")
langfuse_host=os.getenv("LANGFUSE_HOST")
