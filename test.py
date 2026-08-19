# test.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

try:
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com"
    )
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": "Hola, ¿cómo estás?"}],
        max_tokens=50
    )
    
    print("✅ Conexión exitosa!")
    print(f"Respuesta: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    