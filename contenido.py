"""Contenido del curso «LLM en la práctica · Edición esencial».

Cada módulo vive en modulos/mNN.py y expone un diccionario MODULE.
Este archivo los reúne y añade los metadatos del curso y el glosario.
"""

from modulos import m01, m02, m03, m04, m05, m06, m07

MODULES = [
    m01.MODULE,
    m02.MODULE,
    m03.MODULE,
    m04.MODULE,
    m05.MODULE,
    m06.MODULE,
    m07.MODULE,
]

COURSE = {
    "title": "LLM en la práctica",
    "brand": "HLLM",
    "subtitle": "Edición esencial",
    "tagline": "Del token a la aplicación",
    "description": (
        "Edición esencial en español de «Hands-On Large Language Models», de Jay "
        "Alammar y Maarten Grootendorst: cómo se representan los tokens, cómo "
        "atiende un Transformer, cómo se decodifica una respuesta, y cómo se "
        "construyen clasificadores, buscadores, sistemas RAG, ajustes finos y "
        "aplicaciones multimodales con texto y diagramas originales."
    ),
    "book": "Hands-On Large Language Models",
    "author": "Jay Alammar y Maarten Grootendorst",
    "pdf": "Hands-On-LLM-Esencial.pdf",
    "year": "2026",
    "global": "HLLM",
    "theme_key": "hllm_theme",
}

# Glosario: (término, definición breve, id de lección donde se desarrolla)
GLOSARIO = [
    ("Alineación", "Proceso de ajustar un modelo para que sus respuestas coincidan con las preferencias y los límites humanos.", "hllm7l2"),
    ("Alucinación", "Respuesta fluida y plausible que no está respaldada por los datos ni por el contexto disponible.", "hllm6l2"),
    ("Aprendizaje contrastivo", "Entrenamiento que acerca las parejas relacionadas y aleja las no relacionadas en el espacio de embeddings.", "hllm2l3"),
    ("Atención", "Mecanismo que pondera la información de unas posiciones del contexto al construir la representación de otra.", "hllm1l2"),
    ("Atención multi-consulta", "Variante en la que varias cabezas de consulta comparten una sola proyección de clave y valor para ahorrar memoria.", "hllm3l3"),
    ("Auto-atención", "Atención en la que las consultas, claves y valores proceden de la misma secuencia de entrada.", "hllm1l2"),
    ("Bag-of-words", "Representación de un texto como recuento de palabras, sin orden ni contexto.", "hllm1l1"),
    ("Beam search", "Estrategia de decodificación que mantiene varias continuaciones candidatas y elige la de mayor probabilidad total.", "hllm3l2"),
    ("BERT", "Modelo encoder entrenado para predecir palabras ocultas; produce representaciones ricas para clasificar y buscar.", "hllm4l1"),
    ("BERTopic", "Marco de modelado de temas que combina embeddings, reducción de dimensión, agrupamiento y palabras clave.", "hllm4l3"),
    ("BPE", "Tokenización por pares de bytes que fusiona los símbolos más frecuentes hasta formar un vocabulario de subpalabras.", "hllm2l1"),
    ("Búsqueda aproximada", "Recuperación de vecinos cercanos que sacrifica algo de exhaustividad para responder en milisegundos.", "hllm6l1"),
    ("Chunking", "División de documentos largos en fragmentos recuperables que caben en el contexto del modelo.", "hllm6l2"),
    ("Clasificación", "Tarea de asignar una etiqueta predefinida a un texto, una imagen u otra entrada.", "hllm4l1"),
    ("Clúster", "Grupo de elementos que se parecen entre sí más que al resto del conjunto.", "hllm4l3"),
    ("Contexto", "Conjunto de tokens que el modelo puede consultar en una generación; su tamaño limita lo que cabe en la ventana.", "hllm3l2"),
    ("Cuantización", "Reducción de la precisión numérica de los pesos para ahorrar memoria y acelerar la inferencia.", "hllm7l2"),
    ("Decodificación", "Proceso de convertir probabilidades en tokens concretos hasta completar una respuesta.", "hllm3l1"),
    ("Embedding", "Vector denso que representa el significado de un token, una frase o un documento.", "hllm1l1"),
    ("Embedding contextual", "Vector de un token que cambia según las palabras que lo rodean.", "hllm2l2"),
    ("Embedding de frase", "Vector que resume el significado de una oración o un párrafo completo para compararlo con otros.", "hllm2l3"),
    ("Encoder", "Parte del Transformer que lee la entrada completa y construye representaciones bidireccionales.", "hllm1l2"),
    ("Decoder", "Parte del Transformer que genera la salida token a token usando una máscara causal.", "hllm1l2"),
    ("Entrenamiento autosupervisado", "Aprendizaje que obtiene la señal de la propia estructura de los datos, sin etiquetas manuales.", "hllm1l3"),
    ("Fine-tuning", "Ajuste de un modelo ya entrenado con datos y un objetivo específicos.", "hllm7l1"),
    ("Few-shot", "Uso de unos pocos ejemplos dentro del prompt para indicar la tarea al modelo.", "hllm5l2"),
    ("FlashAttention", "Implementación de atención consciente de la memoria que reduce lecturas y escrituras intermedias.", "hllm3l3"),
    ("Grupo de consultas (GQA)", "Compromiso entre atención multi-cabeza y multi-consulta: varios conjuntos de consultas comparten claves y valores.", "hllm3l3"),
    ("HDBSCAN", "Algoritmo de agrupamiento por densidad que descubre grupos de forma y tamaño variables y marca el ruido.", "hllm4l3"),
    ("In-context learning", "Capacidad de resolver una tarea nueva a partir de instrucciones y ejemplos incluidos en el prompt.", "hllm5l2"),
    ("Índice vectorial", "Estructura que permite buscar embeddings similares sin comparar contra todos los documentos.", "hllm6l1"),
    ("Inferencia", "Ejecución del modelo ya entrenado para producir una predicción o una respuesta.", "hllm3l1"),
    ("Instrucción", "Texto que indica al modelo qué hacer, con qué información y en qué formato responder.", "hllm5l1"),
    ("KV cache", "Almacén de claves y valores ya calculados que evita recomputar el contexto en cada token nuevo.", "hllm3l2"),
    ("LoRA", "Ajuste eficiente que congela los pesos base y entrena dos matrices pequeñas de bajo rango.", "hllm7l2"),
    ("Logits", "Puntuaciones sin normalizar que el modelo asigna a cada token del vocabulario antes de aplicar softmax.", "hllm3l1"),
    ("Máscara causal", "Restricción que impide a cada posición mirar hacia el futuro durante la generación.", "hllm1l2"),
    ("Mezcla de expertos (MoE)", "Arquitectura que activa solo unas pocas subredes especializadas por token para reducir cómputo.", "hllm3l3"),
    ("Modelo base", "Modelo preentrenado en texto general, antes de recibir instrucciones o preferencias.", "hllm1l3"),
    ("Modelo de representación", "Modelo que convierte texto en vectores útiles para clasificar, buscar o agrupar.", "hllm1l2"),
    ("Modelo generativo", "Modelo que produce texto nuevo prediciendo el siguiente token de forma repetida.", "hllm1l2"),
    ("Multimodal", "Modelo o sistema que combina texto con imágenes, audio u otros tipos de datos.", "hllm7l3"),
    ("NER", "Reconocimiento de entidades nombradas: localizar personas, lugares, organizaciones y fechas en un texto.", "hllm7l1"),
    ("Overfitting", "Situación en la que el modelo memoriza los datos de entrenamiento y pierde capacidad de generalizar.", "hllm7l1"),
    ("Parámetro", "Valor numérico aprendido durante el entrenamiento que define el comportamiento del modelo.", "hllm1l3"),
    ("Perplejidad", "Medida de cuánto se sorprende un modelo ante un texto; más baja suele indicar mejor ajuste.", "hllm3l2"),
    ("PEFT", "Familia de técnicas de ajuste fino eficiente que entrenan solo una fracción pequeña de los pesos.", "hllm7l2"),
    ("Preentrenamiento", "Primera fase de entrenamiento a gran escala sobre texto general para aprender el idioma.", "hllm1l3"),
    ("Prompt", "Entrada completa que recibe el modelo: instrucción, contexto, ejemplos y formato esperado.", "hllm5l1"),
    ("Prompt engineering", "Diseño sistemático de entradas para obtener respuestas más útiles, fiables y verificables.", "hllm5l1"),
    ("QLoRA", "LoRA aplicado sobre un modelo base cuantizado a 4 bits, que reduce mucho la memoria necesaria.", "hllm7l2"),
    ("RAG", "Generación aumentada por recuperación: se buscan documentos relevantes y se pasan al modelo como contexto.", "hllm6l2"),
    ("Razonamiento en cadena", "Técnica que pide al modelo explicitar pasos intermedios antes de dar la respuesta final.", "hllm5l3"),
    ("ReAct", "Patrón de agente que alterna razonamiento, acción y observación del resultado de la herramienta.", "hllm5l3"),
    ("Reranking", "Segunda etapa de búsqueda que reordena los candidatos con un modelo más preciso y más costoso.", "hllm6l1"),
    ("RLHF", "Ajuste con retroalimentación humana: se entrena una recompensa y se optimiza el modelo hacia ella.", "hllm7l2"),
    ("RoPE", "Codificación posicional rotatoria que representa la posición relativa dentro de la atención.", "hllm3l3"),
    ("Sampling", "Selección aleatoria de un token según la distribución de probabilidad del modelo.", "hllm3l2"),
    ("Self-consistency", "Técnica que genera varios razonamientos y elige la respuesta final más repetida.", "hllm5l3"),
    ("SetFit", "Método de clasificación few-shot que ajusta un encoder con pares generados y luego entrena un clasificador simple.", "hllm7l1"),
    ("Similitud coseno", "Medida del ángulo entre dos vectores; vale 1 cuando apuntan en la misma dirección.", "hllm2l3"),
    ("Softmax", "Función que convierte puntuaciones arbitrarias en una distribución de probabilidad que suma uno.", "hllm3l1"),
    ("Temperatura", "Parámetro que aplana o agudiza la distribución de probabilidad antes de muestrear el siguiente token.", "hllm3l2"),
    ("Token", "Unidad mínima de texto que el modelo convierte en un identificador numérico.", "hllm2l1"),
    ("Tokenizador", "Componente que divide el texto en tokens y los traduce a identificadores del vocabulario.", "hllm2l1"),
    ("Transformer", "Arquitectura basada en atención que procesa secuencias en paralelo y sostiene a los LLM actuales.", "hllm1l2"),
    ("UMAP", "Técnica de reducción de dimensión que conserva la estructura local para visualizar y agrupar embeddings.", "hllm4l3"),
    ("Zero-shot", "Uso del modelo sin ejemplos de la tarea, confiando solo en la instrucción y el conocimiento aprendido.", "hllm4l1"),
]
