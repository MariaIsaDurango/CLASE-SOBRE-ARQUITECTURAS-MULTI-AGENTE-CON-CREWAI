"""
equipo.py  ·  Piezas comunes del taller (agentes, herramienta y tareas).

Los scripts paso1, paso2 y paso3 importan este archivo, así cada paso
solo muestra lo que cambia.
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from crewai import Agent, Task
from crewai.tools import tool

# ── 1. Configuración ───────────────────────────────────────────────────
load_dotenv()  # lee el archivo .env si existe

# MODELO decide qué "cerebro" usan los agentes:
#   demo                         -> modelo simulado: gratis, sin clave (por defecto)
#   gemini/<modelo>              -> Google Gemini, nivel gratuito (necesita GEMINI_API_KEY)
#   gpt-4o-mini (u otro OpenAI)  -> de pago (necesita OPENAI_API_KEY)
MODELO = os.getenv("MODELO", "demo").strip()

if MODELO == "demo":
    from demo_llm import DemoLLM
    LLM = DemoLLM()
    print(">> MODO DEMO: modelo simulado, gratis y sin clave. "
          "CrewAI se ejecuta de verdad; las respuestas son de ejemplo.\n")
elif MODELO.startswith("gemini/"):
    if not (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")):
        raise SystemExit("Falta GEMINI_API_KEY en el archivo .env (clave gratuita en aistudio.google.com).")
    LLM = MODELO
else:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Falta OPENAI_API_KEY en el archivo .env, o usa MODELO=demo (gratis).")
    LLM = MODELO

CARPETA_APUNTES = Path(__file__).parent / "apuntes"


# ── 2. Herramienta: base documental local (sin internet) ───────────────
@tool("leer_apuntes")
def leer_apuntes(nombre_archivo: str = "") -> str:
    """Lee los apuntes del curso. Sin argumento devuelve la lista de
    archivos disponibles; con un nombre de archivo devuelve su contenido."""
    archivos = sorted(p.name for p in CARPETA_APUNTES.glob("*.md"))
    if not nombre_archivo:
        return "Archivos disponibles: " + ", ".join(archivos)
    ruta = CARPETA_APUNTES / Path(nombre_archivo).name  # evita salir de la carpeta
    if not ruta.exists():
        return f"No existe '{nombre_archivo}'. Disponibles: {', '.join(archivos)}"
    return ruta.read_text(encoding="utf-8")


# ── 3. Agentes: rol + objetivo + contexto + herramientas ───────────────
def crear_agentes():
    investigador = Agent(
        role="Investigador documental",
        goal="Extraer de los apuntes del curso los datos relevantes sobre {tema}, "
             "indicando de qué archivo sale cada uno",
        backstory="Trabajas solo con fuentes verificables. Si un dato no está "
                  "en los apuntes, lo dices en lugar de inventarlo.",
        tools=[leer_apuntes],          # el ÚNICO agente con herramienta
        llm=LLM,
        allow_delegation=False,
        max_iter=8,                    # límite de iteraciones del bucle del agente
    )
    analista = Agent(
        role="Analista técnico",
        goal="Organizar los hallazgos y separar hechos, inferencias y lagunas",
        backstory="Detectas contradicciones y huecos de información.",
        llm=LLM,
        allow_delegation=False,
    )
    redactor = Agent(
        role="Redactor técnico",
        goal="Escribir un informe breve y claro sobre {tema} usando solo el análisis",
        backstory="Escribes para un público técnico. Frases cortas y cada "
                  "afirmación con su fuente entre corchetes.",
        llm=LLM,
        allow_delegation=False,
    )
    revisor = Agent(
        role="Revisor de calidad",
        goal="Detectar afirmaciones sin respaldo en el análisis y corregirlas",
        backstory="Eres exigente: si una frase no tiene respaldo, la quitas o la matizas.",
        llm=LLM,
        allow_delegation=False,
    )
    return investigador, analista, redactor, revisor


# ── 4. Tareas: descripción + resultado esperado + dependencias ─────────
def crear_tareas(investigador, analista, redactor, revisor, asignar=True):
    """asignar=False deja las tareas sin agente (lo usa el proceso jerárquico,
    donde el manager decide quién hace cada una)."""
    a = lambda agente: agente if asignar else None

    t_investigar = Task(
        description="Usa la herramienta leer_apuntes para revisar los apuntes "
                    "y reúne los datos relevantes sobre: {tema}.",
        expected_output="Entre 6 y 10 viñetas. Cada una termina con [archivo.md].",
        agent=a(investigador),
    )
    t_analizar = Task(
        description="Clasifica los hallazgos en tres bloques: HECHOS, "
                    "INFERENCIAS y LAGUNAS (lo que los apuntes no cubren).",
        expected_output="Tres listas con esos títulos.",
        agent=a(analista),
        context=[t_investigar],        # recibe la salida del investigador
    )
    t_redactar = Task(
        description="Redacta un informe sobre {tema} basado en el análisis.",
        expected_output="Markdown con: ## Resumen, ## Hallazgos, "
                        "## Limitaciones, ## Fuentes. Máximo 350 palabras.",
        agent=a(redactor),
        context=[t_analizar],
    )
    t_revisar = Task(
        description="Revisa el informe contra el análisis. Elimina o matiza "
                    "lo que no tenga respaldo. Devuelve el informe final.",
        expected_output="El informe final en Markdown con las mismas secciones.",
        agent=a(revisor),
        context=[t_redactar, t_analizar],  # informe + análisis para contrastar
    )
    return [t_investigar, t_analizar, t_redactar, t_revisar]


TEMA_POR_DEFECTO = "cuándo conviene usar RAG, un agente individual o un sistema multi-agente"
