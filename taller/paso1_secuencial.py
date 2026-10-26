"""
PASO 1 · Crew secuencial
Ejecuta:  python paso1_secuencial.py
Las 4 tareas se ejecutan en el orden de la lista y cada una recibe
como contexto la salida de las anteriores que indica `context`.
"""
import time
from crewai import Crew, Process
from equipo import crear_agentes, crear_tareas, TEMA_POR_DEFECTO

agentes = crear_agentes()
tareas = crear_tareas(*agentes)

crew = Crew(
    agents=list(agentes),
    tasks=tareas,
    process=Process.sequential,   # orden fijo, definido por nosotros
    verbose=True,                 # muestra en consola lo que hace cada agente
)

inicio = time.time()
resultado = crew.kickoff(inputs={"tema": TEMA_POR_DEFECTO})
segundos = time.time() - inicio

# Salida de cada tarea: así vemos la contribución de cada agente
for i, salida in enumerate(resultado.tasks_output, 1):
    print(f"\n===== Tarea {i} · {salida.agent} =====\n{salida.raw[:600]}")

print("\n===== INFORME FINAL =====\n", resultado.raw)
print(f"\nTiempo: {segundos:.1f} s")
print("Tokens:", resultado.token_usage)

with open("informe_secuencial.md", "w", encoding="utf-8") as f:
    f.write(resultado.raw)
