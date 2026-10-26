# Apuntes · RAG avanzado y su evaluación (15 y 20 de octubre)

- RAG (Retrieval-Augmented Generation) recupera fragmentos de documentos y los añade al prompt para que el modelo responda con información que no está en su entrenamiento.
- La búsqueda híbrida combina búsqueda semántica (embeddings) con búsqueda léxica (BM25) y fusiona los resultados, por ejemplo con RRF.
- El reranking usa un modelo cross-encoder para reordenar los documentos recuperados y poner los más relevantes primero.
- Corrective RAG (CRAG) evalúa si el contexto recuperado es correcto, ambiguo o incorrecto y, si no basta, busca en fuentes externas.
- Faithfulness mide si la respuesta se apoya en el contexto recuperado, sin inventar.
- Answer relevancy mide si la respuesta contesta a la pregunta formulada.
- RAG es un mecanismo de recuperación de información: no toma decisiones ni ejecuta acciones por sí mismo.
