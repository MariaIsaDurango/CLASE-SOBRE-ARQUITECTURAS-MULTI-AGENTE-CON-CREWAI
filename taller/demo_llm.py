"""
demo_llm.py  ·  Modelo simulado para el MODO DEMO (gratis, sin clave, sin cuenta).

CrewAI funciona de verdad: crea los agentes, ejecuta las tareas en orden,
pasa el contexto entre ellas, llama a la herramienta leer_apuntes y aplica
el guardrail. Lo único simulado es el "cerebro": en lugar de llamar a un
modelo de pago, este archivo devuelve respuestas de ejemplo según el rol.

Sirve para entender la ARQUITECTURA. Para respuestas reales y distintas
cada vez, usa un modelo real (ver .env.example).
"""
import json
from crewai import BaseLLM

RESPUESTAS = {
    "Investigador documental": """- RAG recupera fragmentos de documentos y los añade al prompt [01_rag.md]
- RAG es un mecanismo de recuperación: no toma decisiones ni ejecuta acciones [01_rag.md]
- Un agente trabaja en bucle: razona, actúa con herramientas y observa [02_agentes.md]
- Un agente con demasiadas herramientas elige peor y gasta más tokens [02_agentes.md]
- La memoria de corto plazo está limitada por la ventana de contexto [03_planificacion_memoria.md]
- Un modelo que revisa su propio trabajo detecta peor sus errores [03_planificacion_memoria.md]
- Un sistema multi-agente reparte el problema entre agentes especializados [04_multiagente.md]
- Anthropic informó +90,2 % de rendimiento usando unas 15 veces más tokens [04_multiagente.md]""",

    "Analista técnico": """HECHOS
- RAG recupera información; no decide ni actúa [01_rag.md]
- Un agente decide y usa herramientas en bucle [02_agentes.md]
- Multi-agente reparte el trabajo entre especialistas y cuesta más tokens [04_multiagente.md]

INFERENCIAS
- Para responder preguntas sobre documentos basta RAG
- Para tareas de varios pasos con herramientas conviene un agente
- Multi-agente compensa solo si la tarea se divide en especialidades

LAGUNAS
- Los apuntes no dan cifras de costo para tareas concretas
- No hay comparativas propias de tiempo de respuesta""",

    "Redactor técnico": """## Resumen
RAG, un agente individual y un sistema multi-agente resuelven problemas distintos y se pueden combinar [01_rag.md] [02_agentes.md].

## Hallazgos
- Usa RAG cuando el problema es encontrar información en documentos [01_rag.md].
- Usa un agente cuando hay que decidir pasos y usar herramientas [02_agentes.md].
- Usa multi-agente cuando la tarea tiene fases con especialidades distintas, como investigar, analizar, redactar y revisar [04_multiagente.md].
- Multi-agente puede rendir más, pero consume muchos más tokens [04_multiagente.md].

## Limitaciones
Los apuntes no incluyen cifras de costo ni de tiempo para casos concretos.

## Fuentes
[01_rag.md] [02_agentes.md] [03_planificacion_memoria.md] [04_multiagente.md]""",
}
RESPUESTAS["Revisor de calidad"] = RESPUESTAS["Redactor técnico"].replace(
    "Multi-agente puede rendir más, pero consume muchos más tokens [04_multiagente.md].",
    "Multi-agente puede rendir más en algunas tareas, pero consume muchos más tokens [04_multiagente.md].",
)


class DemoLLM(BaseLLM):
    """Devuelve respuestas de ejemplo en el formato que CrewAI espera."""

    def __init__(self):
        super().__init__(model="demo")

    def supports_function_calling(self) -> bool:
        return False

    def call(self, messages, tools=None, callbacks=None, available_functions=None,
             from_task=None, from_agent=None, response_model=None):
        texto = json.dumps(messages, ensure_ascii=False) if not isinstance(messages, str) else messages
        rol = getattr(from_agent, "role", "") or ""

        # El investigador primero usa su herramienta, luego responde
        if rol == "Investigador documental" and "Archivos disponibles" not in texto:
            return ('Thought: Primero miro qué apuntes hay disponibles.\n'
                    'Action: leer_apuntes\n'
                    'Action Input: {"nombre_archivo": ""}')

        respuesta = RESPUESTAS.get(rol, RESPUESTAS["Revisor de calidad"])
        return f"Thought: Ya tengo lo necesario para entregar mi parte.\nFinal Answer: {respuesta}"
