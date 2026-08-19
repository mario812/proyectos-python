import os
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class DeepSeekAgent:
    """
    Agente simple para interactuar con el modelo DeepSeek.
    """
    
    def __init__(self, api_key=None, model="deepseek-chat"):
        """
        Inicializa el agente con la clave API y modelo.
        """
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "⚠️ No se encontró DEEPSEEK_API_KEY. "
                "Configúrala en .env o pásala al constructor."
            )
        
        # Configurar el cliente OpenAI para DeepSeek
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        )
        self.model = model
        self.history = []  # Historial de conversación
        self.history.append({
            "role": "system",
            "content": "Eres un asistente útil, profesional y conciso."
        })
    
    def chat(self, user_message, temperature=0.7, max_tokens=1000):
        """
        Envía un mensaje al modelo y recibe la respuesta.
        """
        # Agregar mensaje del usuario al historial
        self.history.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            # Llamada a la API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.history,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Extraer respuesta del asistente
            assistant_message = response.choices[0].message.content
            
            # Guardar en historial
            self.history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            return f"❌ Error al comunicarse con DeepSeek: {str(e)}"
    
    def reset_history(self):
        """
        Reinicia el historial de conversación, manteniendo solo el prompt de sistema.
        """
        self.history = [
            {"role": "system", "content": "Eres un asistente útil, profesional y conciso."}
        ]
        print("🔄 Historial reiniciado.")
    
    def save_response(self, user_message, response, filename=None):
        """
        Guarda la conversación en un archivo JSON.
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"output/conversacion_{timestamp}.json"
        
        # Asegurar carpeta output
        os.makedirs("output", exist_ok=True)
        
        # Cargar historial existente o crear nuevo
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        
        # Agregar nueva interacción
        data.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "assistant": response
        })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Conversación guardada en: {filename}")
    
    def show_history(self):
        """
        Muestra el historial de la conversación actual.
        """
        print("\n📜 HISTORIAL DE CONVERSACIÓN:")
        print("-" * 50)
        for i, msg in enumerate(self.history):
            if msg["role"] != "system":  # Omitir prompt de sistema
                print(f"[{msg['role'].upper()}] {msg['content'][:100]}...")
        print("-" * 50)


def main():
    """
    Función principal para usar el agente desde consola.
    """
    print("\n" + "="*60)
    print("🤖 AGENTE DEEPSEEK v1.0")
    print("="*60)
    
    # Crear agente
    try:
        agent = DeepSeekAgent()
        print("✅ Agente inicializado correctamente.")
        print(f"📌 Modelo: {agent.model}")
    except ValueError as e:
        print(e)
        return
    
    print("\n💡 COMANDOS:")
    print("  /reset  - Reiniciar historial")
    print("  /save   - Guardar conversación actual")
    print("  /history- Mostrar historial")
    print("  /exit   - Salir")
    print("-" * 60)
    print("¡Escribe tu mensaje para el asistente!\n")
    
    while True:
        try:
            user_input = input("\n🧑 Tú: ").strip()
            
            if not user_input:
                continue
            
            # Comandos especiales
            if user_input.lower() == "/exit":
                print("👋 ¡Hasta luego!")
                break
            elif user_input.lower() == "/reset":
                agent.reset_history()
                continue
            elif user_input.lower() == "/save":
                if agent.history:
                    agent.save_response("", "")
                else:
                    print("ℹ️ No hay conversación para guardar.")
                continue
            elif user_input.lower() == "/history":
                agent.show_history()
                continue
            
            # Enviar mensaje al agente
            print("\n🤖 Asistente: ", end="", flush=True)
            response = agent.chat(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()
    