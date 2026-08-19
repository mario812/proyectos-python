import os
import math
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Cargar variables de entorno
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Error: Variable GEMINI_API_KEY no encontrada en el entorno.")

# ==========================================
# 1. Definición de herramientas (Tools)
# ==========================================

def calculate_expression(expression: str) -> str:
    """Evalúa una expresión matemática segura en Python.
    
    Args:
        expression: Cadena con la fórmula matemática a evaluar (ej: '25 * 4 + sqrt(144)').
    """
    try:
        allowed_globals = {
            "__builtins__": {},
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "pi": math.pi,
            "pow": math.pow,
            "log": math.log
        }
        result = eval(expression, allowed_globals)
        return f"Resultado: {result}"
    except Exception as e:
        return f"Error al calcular la expresión: {str(e)}"

def check_crypto_price(symbol: str) -> str:
    """Obtiene el precio simulado o de referencia de un criptoactivo o divisa.
    
    Args:
        symbol: Ticker o símbolo del activo (ej: 'SOL', 'BTC', 'ETH').
    """
    mock_database = {
        "SOL": "178.50 USD (+4.2% 24h)",
        "BTC": "94,200.00 USD (+1.8% 24h)",
        "ETH": "3,450.00 USD (-0.5% 24h)"
    }
    symbol_upper = symbol.strip().upper()
    price = mock_database.get(symbol_upper, "Activo no encontrado en la base de datos local.")
    return f"Precio para {symbol_upper}: {price}"

# ==========================================
# 2. Inicialización del Cliente y Agente
# ==========================================

client = genai.Client(api_key=api_key)

SYSTEM_INSTRUCTION = """
Eres un agente de IA autónomo y analítico.
Tu tarea es responder preguntas de los usuarios utilizando tus herramientas disponibles cuando sea necesario.
Si una pregunta involucra cálculos matemáticos o consulta de precios, SIEMPRE usa las herramientas antes de responder.
"""

# Configuración del agente con llamada a funciones activada
agent_config = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION,
    temperature=0.2,
    tools=[calculate_expression, check_crypto_price]
)

# Inicializar sesión de chat persistente (mantiene memoria conversacional)
agent_session = client.chats.create(
    model="gemini-2.5-flash",
    config=agent_config
)

# ==========================================
# 3. Bucle de ejecución (Loop interactivo)
# ==========================================

def run_agent_loop():
    print("=== Agente Gemini Activo ===")
    print("Herramientas integradas: [Calculadora, Consulta de Precios]")
    print("Escribe 'salir' para terminar.\n")

    while True:
        try:
            user_input = input("Usuario > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["salir", "exit", "quit"]:
                print("Finalizando sesión del agente.")
                break

            # Envío del mensaje al agente
            response = agent_session.send_message(user_input)
            print(f"\nAgente > {response.text}\n")

        except KeyboardInterrupt:
            print("\nInterrupción detectada. Cerrando...")
            break
        except Exception as err:
            print(f"\n[Error]: {err}\n")

if __name__ == "__main__":
    run_agent_loop()
    