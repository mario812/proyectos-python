import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Verificar que la clave existe
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    print("❌ Error: No se encontró DEEPSEEK_API_KEY en .env")
    print("📝 Crea un archivo .env con:")
    print("DEEPSEEK_API_KEY=tu_clave_aqui")
    exit(1)

try:
    # Importar después de verificar la clave
    import openai
    
    print(f"📦 Versión de OpenAI: {openai.__version__}")
    
    # Configurar el cliente de forma directa
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )
    
    # Hacer una prueba simple
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Eres un asistente útil."},
            {"role": "user", "content": "Responde con 'OK' si puedes leer este mensaje."}
        ],
        max_tokens=10
    )
    
    print("✅ ¡Conexión exitosa!")
    print(f"📨 Respuesta: {response.choices[0].message.content}")
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("Ejecuta: pip install openai==1.12.0")
    
except Exception as e:
    error_msg = str(e)
    
    if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
        print("❌ Error de autenticación. Verifica tu clave API en .env")
    elif "proxies" in error_msg:
        print("❌ Error de proxies detectado. Usando método alternativo...")
        # Intento con método alternativo
        try:
            import httpx
            client = openai.OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com",
                http_client=httpx.Client()
            )
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": "Hola"}],
                max_tokens=5
            )
            print("✅ ¡Conexión exitosa con método alternativo!")
            print(f"📨 Respuesta: {response.choices[0].message.content}")
        except Exception as e2:
            print(f"❌ También falló el método alternativo: {e2}")
    else:
        print(f"❌ Error: {error_msg}")
        