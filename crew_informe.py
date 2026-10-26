from crewai import Agent, Task, Crew, Process

# 1) LOS GUERREROS: cada agente = rol + objetivo + historia (+ herramientas)
investigador = Agent(
    role="Investigador técnico",
    goal="Reunir datos verificables sobre {tema}, cada uno con su fuente",
    backstory="Bibliotecario obsesivo: nunca afirma nada sin una referencia.",
    llm="gpt-4o-mini",
    allow_delegation=False,
    verbose=True,
)

analista = Agent(
    role="Analista",
    goal="Ordenar los hallazgos y separar hechos, inferencias y dudas",
    backstory="Detecta contradicciones y patrones donde otros ven ruido.",
    llm="gpt-4o-mini",
    allow_delegation=False,
)

redactor = Agent(
    role="Redactor técnico",
    goal="Escribir un informe claro sobre {tema} usando solo el análisis recibido",
    backstory="Explica lo complejo con frases cortas y cita cada dato.",
    llm="gpt-4o-mini",
    allow_delegation=False,
)

revisor = Agent(
    role="Revisor de calidad",
    goal="Detectar afirmaciones sin respaldo y proponer correcciones concretas",
    backstory="El juez más exigente del torneo. Nada pasa sin pruebas.",
    llm="gpt-4o-mini",
    allow_delegation=False,
)

# 2) LAS MISIONES: cada tarea = descripción + resultado esperado + responsable
t_investigar = Task(
    description="Investiga {tema}. Lista hallazgos clave con su fuente.",
    expected_output="8-10 hallazgos en viñetas, cada uno con su fuente.",
    agent=investigador,
)

t_analizar = Task(
    description="Clasifica los hallazgos en: hechos, inferencias, sin confirmar.",
    expected_output="Tabla con tres bloques y las contradicciones detectadas.",
    agent=analista,
    context=[t_investigar],  # recibe la salida del investigador
)

t_redactar = Task(
    description="Redacta un informe de 1 página sobre {tema} a partir del análisis.",
    expected_output="Informe en Markdown: resumen, hallazgos, límites, fuentes.",
    agent=redactor,
    context=[t_analizar],
)

t_revisar = Task(
    description="Revisa el informe. Corrige lo que no tenga respaldo en el análisis.",
    expected_output="Informe final corregido + lista de cambios realizados.",
    agent=revisor,
    context=[t_redactar, t_analizar],
    output_file="informe_final.md",
)

# 3) EL EQUIPO: agentes + tareas + modo de combate (proceso)
crew = Crew(
    agents=[investigador, analista, redactor, revisor],
    tasks=[t_investigar, t_analizar, t_redactar, t_revisar],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    resultado = crew.kickoff(inputs={"tema": "baterías de estado sólido"})
    print(resultado.raw)
    print(resultado.token_usage)
