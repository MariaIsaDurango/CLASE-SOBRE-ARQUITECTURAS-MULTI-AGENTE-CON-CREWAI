"""
PASO 2 · Crew jerárquica
Ejecuta:  python paso2_jerarquico.py
Mismos agentes y tareas, pero las tareas NO tienen agente asignado:
un manager (creado por CrewAI con manager_llm) decide quién hace cada una,
revisa los resultados y valida cuándo están completas.
Compara el tiempo y los tokens con el paso 1.
"""
import time
from crewai import Crew, Process
from equipo import crear_agentes, crear_tareas, TEMA_POR_DEFECTO, MODELO

agentes = crear_agentes()
tareas = crear_tareas(*agentes, asignar=False)   # sin agente: decide el manager

crew = Crew(
    agents=list(agentes),
    tasks=tareas,
    process=Process.hierarchical,
    manager_llm=MODELO,           # obligatorio en jerárquico (o manager_agent=...)
    verbose=True,
)

inicio = time.time()
resultado = crew.kickoff(inputs={"tema": TEMA_POR_DEFECTO})
segundos = time.time() - inicio

print("\n===== INFORME FINAL =====\n", resultado.raw)
print(f"\nTiempo: {segundos:.1f} s")
print("Tokens:", resultado.token_usage)

with open("informe_jerarquico.md", "w", encoding="utf-8") as f:
    f.write(resultado.raw)
