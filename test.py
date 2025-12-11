import google.generativeai as genai
from utils.config import google_api

genai.configure(api_key=google_api)

models=genai.list_models()
print(list(models))