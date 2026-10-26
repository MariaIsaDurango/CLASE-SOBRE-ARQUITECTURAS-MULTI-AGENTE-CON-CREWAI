"""
PASO 3 · Validar la salida con un guardrail
Ejecuta:  python paso3_guardrail.py
Un guardrail es una función que revisa la salida de una tarea.
Si devuelve (False, motivo), el agente rehace la tarea con ese motivo
como feedback, hasta guardrail_max_retries veces.
"""
from crewai import Crew, Process
from equipo import crear_agentes, crear_tareas, TEMA_POR_DEFECTO

SECCIONES = ["## Resumen", "## Hallazgos", "## Limitaciones", "## Fuentes"]


def validar_informe(salida):
    texto = salida.raw
    faltan = [s for s in SECCIONES if s not in texto]
    if faltan:
        return (False, f"Faltan las secciones: {', '.join(faltan)}")
    palabras = len(texto.split())
    if palabras > 400:
        return (False, f"El informe tiene {palabras} palabras; máximo 400.")
    if "[" not in texto:
        return (False, "Ninguna afirmación cita su fuente entre corchetes.")
    return (True, texto)


agentes = crear_agentes()
tareas = crear_tareas(*agentes)
tareas[-1].guardrail = validar_informe      # se aplica a la tarea del revisor
tareas[-1].guardrail_max_retries = 2

crew = Crew(agents=list(agentes), tasks=tareas,
            process=Process.sequential, verbose=True)

resultado = crew.kickoff(inputs={"tema": TEMA_POR_DEFECTO})
print("\n===== INFORME VALIDADO =====\n", resultado.raw)
print("Tokens:", resultado.token_usage)
