# Apuntes · Sistemas multi-agente (27 de octubre)

- Un sistema multi-agente reparte un problema entre varios agentes especializados, cada uno con su rol, sus herramientas y su propio contexto, que se coordinan.
- Patrones habituales: secuencial (pipeline), supervisor u orquestador, jerárquico (supervisores de supervisores) y red (peer-to-peer).
- Anthropic informó en 2025 de que su sistema de investigación multi-agente superó en un 90,2 % a un agente individual en su evaluación interna, usando unas 15 veces más tokens que un chat.
- Según Anthropic, los sistemas multi-agente encajan en tareas paralelizables y con mucha información; encajan peor cuando todos los agentes necesitan el mismo contexto, como en muchas tareas de programación.
- Los errores se propagan: un dato falso del primer agente contamina a los siguientes si nadie lo verifica.
- Si un problema es predecible y repetitivo, un flujo determinista (código normal) suele ser más barato y fiable que cualquier agente.
