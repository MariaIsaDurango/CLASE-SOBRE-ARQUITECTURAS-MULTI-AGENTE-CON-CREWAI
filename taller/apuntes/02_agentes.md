# Apuntes · Agentes de IA y uso de herramientas (21 y 22 de octubre)

- Un agente es un modelo de lenguaje que trabaja en un bucle: razona, elige una acción, la ejecuta y observa el resultado, hasta cumplir un objetivo.
- El patrón ReAct alterna razonamiento (Thought) y acción (Action) con observaciones.
- Tool use: el modelo no ejecuta código; decide qué herramienta llamar y con qué argumentos, y la aplicación ejecuta la llamada y le devuelve el resultado.
- Cada herramienta necesita un nombre, una descripción clara y unos parámetros definidos; de ello depende que el modelo la elija bien.
- Un agente con demasiadas herramientas tiende a elegir peor y gasta más tokens decidiendo.
- Conviene limitar los permisos de cada herramienta: un agente solo debe poder hacer lo que su tarea requiere.
