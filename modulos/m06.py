MODULE = {
    "num": "06",
    "title": "Búsqueda semántica y RAG",
    "sub": "Conectar el modelo con conocimiento que no memorizó",
    "lessons": [
        {
            "id": "hllm6l1",
            "lnum": 1,
            "title": "Búsqueda semántica",
            "minutes": 9,
            "lead": "La búsqueda por palabras clave encuentra lo que dice el documento; la búsqueda semántica encuentra lo que significa. Convertir consultas y documentos en vectores permite recuperar paráfrasis, sinónimos y preguntas formuladas de otra manera. Pero un buen buscador no es solo un índice vectorial: también es reordenamiento, filtros y evaluación.",
            "diagram": ("flow", ["Consulta", "Embedding", "Índice", "Rerank"]),
            "caption": "La consulta se convierte en vector, se buscan candidatos cercanos y un modelo más preciso reordena los primeros resultados.",
            "sections": [
                {
                    "h": "De la palabra exacta a la intención",
                    "p": [
                        "La búsqueda léxica, como BM25, puntúa documentos por coincidencia de términos y su rareza. Es rápida, transparente y excelente cuando el usuario conoce la palabra exacta: un número de referencia, un nombre propio o un código de error. Falla cuando la consulta usa sinónimos o cuando el documento emplea otra formulación.",
                        "La búsqueda densa compara embeddings y recupera textos cercanos en significado. Encuentra «cómo cancelo mi suscripción» en un documento titulado «baja del servicio», aunque no compartan palabras. También funciona entre idiomas si el modelo fue entrenado para ello. Su punto débil es lo contrario: puede pasar por alto una coincidencia exacta que era decisiva.",
                        "La combinación suele ser mejor que cualquiera por separado. La búsqueda híbrida fusiona puntuaciones léxicas y vectoriales, a menudo con una normalización de rangos. Así conserva la precisión de los términos exactos y la cobertura semántica. El peso relativo se ajusta con un conjunto de consultas reales, no con una regla universal.",
                    ],
                },
                {
                    "h": "Indexar para responder rápido",
                    "p": [
                        "Comparar una consulta contra millones de vectores uno por uno es inviable en producción. Los índices aproximados, como HNSW o IVF, organizan el espacio para visitar solo una parte de los candidatos. Sacrifican algo de exhaustividad a cambio de latencia y memoria. El parámetro de búsqueda controla ese intercambio.",
                        "El filtrado por metadatos es igual de importante. El usuario suele querer documentos de su país, su versión del producto o un rango de fechas. Aplicar filtros antes o después de la búsqueda cambia el rendimiento y los resultados. Un índice que ignora los permisos puede devolver información que el usuario no debería ver.",
                        "La unidad indexada condiciona todo. Un documento entero produce un vector difuso; un fragmento demasiado pequeño pierde contexto. La estrategia de división, el solapamiento y la conservación de títulos y rutas se estudian en la lección siguiente, pero ya afectan a la calidad de la búsqueda. El índice no arregla una mala segmentación.",
                    ],
                },
                {
                    "h": "Reordenar y medir",
                    "p": [
                        "El recuperador denso suele usar un bi-encoder: codifica consulta y documento por separado, lo que permite precalcular. Un cross-encoder, en cambio, procesa la pareja completa y puntúa la relevancia con más precisión. Es demasiado caro para todo el corpus, pero excelente para reordenar los primeros cincuenta candidatos.",
                        "Las métricas deben reflejar el uso. Recall@k mide si el documento relevante aparece entre los primeros k; MRR premia que la primera respuesta correcta esté arriba; nDCG considera el orden y la relevancia graduada. Para un chatbot que pasa cinco fragmentos al modelo, recall@5 importa más que la posición exacta; para una lista de resultados, no.",
                        "Sin un conjunto de evaluación, el equipo optimiza a ciegas. Reúne consultas reales, marca los documentos relevantes y mide antes y después de cada cambio. Incluye consultas sin respuesta, errores ortográficos y preguntas ambiguas. La búsqueda perfecta en diez ejemplos fáciles no predice el comportamiento con usuarios.",
                    ],
                },
            ],
            "brief": [
                "La búsqueda léxica acierta términos exactos; la densa acierta significado",
                "La hibridación combina ambas y suele superar a cada una",
                "Los índices aproximados cambian exhaustividad por latencia",
                "El reranking y la evaluación son partes del buscador",
            ],
            "keys": [
                "Elige la señal según la consulta: exacta, semántica o ambas.",
                "Filtra por permisos y metadatos antes de exponer resultados.",
                "Mide recall@k y nDCG con consultas reales.",
                "Reserva el cross-encoder para reordenar pocos candidatos.",
                "Incluye consultas sin respuesta en la evaluación.",
            ],
            "example": "Un buscador de documentación técnica solo usa vectores y falla con códigos de error. Al añadir BM25 y fusionar resultados, los códigos exactos suben y las preguntas conceptuales mantienen su cobertura. Un cross-encoder reordena los veinte primeros y el equipo mide una mejora clara en nDCG@10.",
            "caution": "Un índice vectorial no entiende de permisos. Si filtras después de recuperar, ya has leído documentos restringidos y puedes filtrarlos mal. Aplica el control de acceso en la consulta.",
            "search": "búsqueda semántica dense retrieval embeddings índice vectorial HNSW IVF BM25 híbrida reranking cross-encoder recall nDCG evaluación",
        },
        {
            "id": "hllm6l2",
            "lnum": 2,
            "title": "RAG de principio a fin",
            "minutes": 10,
            "lead": "La generación aumentada por recuperación une un buscador con un modelo generativo. En lugar de confiar en la memoria del modelo, se recuperan fragmentos relevantes y se le piden respuestas basadas en ellos. Suena simple, pero la calidad depende de cada eslabón: parsing, chunking, recuperación, prompt y verificación.",
            "diagram": ("flow", ["Documentos", "Chunks", "Índice", "Generación"]),
            "caption": "El conocimiento se ingiere, se divide, se indexa y se recupera en el momento de responder; el modelo redacta con esas fuentes.",
            "sections": [
                {
                    "h": "El pipeline completo",
                    "p": [
                        "La ingestión empieza por extraer texto limpio de PDF, HTML, bases de datos o wikis. Una tabla mal parseada o un encabezado perdido se convierte en contexto basura. Después se divide en fragmentos, se calculan embeddings y se guardan con metadatos: fuente, sección, fecha, permisos y versión. Sin metadatos, la respuesta no se puede citar ni gobernar.",
                        "En consulta, el sistema puede reescribir la pregunta, recuperar candidatos, reordenarlos y seleccionar los que caben en el contexto. El prompt ensambla instrucciones, fuentes y pregunta. El modelo genera una respuesta y, si se le pide, cita los fragmentos usados. La respuesta vuelve al usuario con enlaces verificables.",
                        "Cada etapa añade latencia. La recuperación y el reranking pueden dominar el tiempo total si el modelo es rápido. La caché de consultas frecuentes, la indexación incremental y la selección de menos fragmentos mejoran la experiencia. También conviene registrar qué se recuperó para poder depurar respuestas incorrectas.",
                    ],
                },
                {
                    "h": "Chunking con criterio",
                    "p": [
                        "El tamaño del fragmento equilibra precisión y contexto. Fragmentos pequeños se comparan mejor con preguntas concretas, pero pueden perder la frase que explica el resultado. Fragmentos grandes contienen más información y también más ruido, y consumen ventana y presupuesto. No hay un número mágico: depende del documento y de la pregunta.",
                        "La estructura del documento es una guía mejor que cortar cada mil caracteres. Respeta títulos, secciones, listas y tablas; conserva el encabezado en cada fragmento para que no pierda significado. El solapamiento entre fragmentos evita cortar una idea a la mitad, a costa de duplicar contenido y aumentar el índice.",
                        "Las estrategias jerárquicas mejoran el contexto: se indexan fragmentos pequeños, pero al recuperar se entrega también su sección padre o un resumen. Así el modelo ve el detalle y el marco. Otra opción es generar resúmenes por documento y usarlos como puerta de entrada. El chunking es diseño de información, no un paso mecánico.",
                    ],
                },
                {
                    "h": "Generar con las fuentes delante",
                    "p": [
                        "El prompt de RAG debe dejar claro que las fuentes son datos, no instrucciones, y que la respuesta se limita a lo que respaldan. Pedir citas por identificador facilita la verificación. Si la respuesta no está en el contexto, el modelo debe decirlo en lugar de completar con conocimiento general no verificado.",
                        "La selección de fragmentos importa tanto como la recuperación. Cinco pasajes redundantes desperdician contexto; cinco pasajes de temas distintos confunden. Deduplica, ordena por relevancia y, si hay conflicto entre fuentes, indícalo. La fecha y la versión del documento ayudan a resolver contradicciones.",
                        "La evaluación separa dos preguntas: ¿recuperé lo necesario? y ¿respondí fielmente a lo recuperado? Un sistema puede recuperar bien y redactar mal, o redactar con fluidez sobre un contexto irrelevante. Medir ambas partes evita culpar al modelo de un fallo del índice o al revés. La respuesta final se revisa con muestras y con usuarios.",
                    ],
                },
            ],
            "brief": [
                "RAG encadena ingestión, chunking, indexación, recuperación y generación",
                "Los metadatos permiten citar, filtrar y gobernar el conocimiento",
                "El chunking debe respetar la estructura y conservar contexto",
                "La fidelidad a las fuentes se evalúa aparte de la recuperación",
            ],
            "keys": [
                "Limpia y estructura el documento antes de partirlo.",
                "Guarda fuente, sección, fecha y permisos con cada fragmento.",
                "Respeta encabezados y tablas al dividir el texto.",
                "Ordena las fuentes como datos y exige citas verificables.",
                "Mide recuperación y fidelidad por separado.",
            ],
            "example": "Un asistente de soporte responde con seguridad sobre una política derogada. El registro muestra que recuperó el documento antiguo porque no filtraba por fecha. Al añadir vigencia a los metadatos y priorizar la versión más reciente, la respuesta se corrige y la cita permite comprobarlo.",
            "caution": "RAG no elimina las alucinaciones. Si el contexto es irrelevante o contradictorio, el modelo puede combinar fragmentos y producir una respuesta falsa con apariencia de fundamento.",
            "search": "RAG retrieval augmented generation pipeline ingestión chunking metadatos índice recuperación prompt citas fidelidad evaluación alucinación",
        },
        {
            "id": "hllm6l3",
            "lnum": 3,
            "title": "RAG avanzado y evaluación",
            "minutes": 9,
            "lead": "Cuando el RAG básico se queda corto, el problema rara vez se resuelve cambiando de modelo. Suele haber consultas mal formuladas, fragmentos mal elegidos o respuestas que no se pueden comprobar. Las mejoras avanzadas atacan esas piezas y, sobre todo, se miden con un conjunto de evaluación que separa recuperación de generación.",
            "diagram": ("bars", [("Recall", 0.86), ("Precisión", 0.72), ("Fidelidad", 0.91)]),
            "caption": "Un panel de métricas por componente revela qué eslabón falla: recuperar, ordenar o redactar sin inventar.",
            "sections": [
                {
                    "h": "Mejorar la consulta",
                    "p": [
                        "Las preguntas de los usuarios son cortas, ambiguas y llenas de referencias a la conversación. La reescritura convierte «¿y eso cuánto tarda?» en una consulta completa con el tema y el contexto. También puede expandir sinónimos o generar varias variantes y fusionar sus resultados.",
                        "HyDE genera un documento hipotético que respondería a la pregunta y busca con su embedding. Funciona cuando la pregunta y el documento usan registros muy distintos. El riesgo es que el documento inventado introduzca detalles falsos; se usa como puente de recuperación, no como respuesta.",
                        "El enrutamiento dirige cada consulta al índice adecuado: facturación, soporte técnico, recursos humanos o código. Un solo índice mezclado diluye la precisión. El enrutador puede ser un clasificador pequeño o reglas; lo importante es medir si acierta y qué ocurre cuando falla.",
                    ],
                },
                {
                    "h": "Mejorar el contexto",
                    "p": [
                        "La búsqueda híbrida y el reranking son las mejoras con mejor relación coste-beneficio. Después, la compresión de contexto elimina frases irrelevantes de cada fragmento antes de pasarlo al modelo. Menos ruido y menos tokens suelen dar respuestas más precisas y más baratas.",
                        "Las técnicas jerárquicas y contextuales enriquecen cada fragmento con un resumen de su sección o con la pregunta que responde. Ese contexto adicional ayuda al modelo a interpretar tablas, abreviaturas y referencias. Cuesta más indexación, pero mejora la recuperación en documentos técnicos y legales.",
                        "Los grafos de conocimiento añaden relaciones entre entidades: personas, productos, dependencias. Son útiles cuando la respuesta exige conectar varios documentos, no solo encontrar el pasaje más parecido. Su coste de construcción y mantenimiento es alto; conviene reservarlos para dominios donde la relación es el valor principal.",
                    ],
                },
                {
                    "h": "Evaluar por componentes",
                    "p": [
                        "Un conjunto de evaluación de RAG debe incluir pregunta, respuesta esperada y documentos relevantes. Con eso se mide el recuperador —recall, precisión, posición— y el generador —fidelidad al contexto, relevancia de la respuesta, formato y citas—. Separar las métricas evita atribuir al modelo un fallo de búsqueda.",
                        "La fidelidad comprueba si cada afirmación se sostiene en las fuentes; la relevancia, si la respuesta atiende la pregunta. Un juez automático puede ayudar a escalar la revisión, pero debe calibrarse contra juicios humanos y revisarse por muestras. Una métrica automática no validada puede dar una falsa sensación de rigor.",
                        "El análisis de fallos es la parte más valiosa. Clasifica los errores: documento ausente, fragmento irrelevante, contexto truncado, respuesta inventada, cita incorrecta. Cada categoría tiene una solución distinta. Sin esa taxonomía, el equipo cambia el prompt una y otra vez y no entiende por qué el sistema no mejora.",
                    ],
                },
            ],
            "brief": [
                "Reescribir y enrutar consultas mejora la recuperación",
                "Híbrida, reranking y compresión aportan mucho por poco coste",
                "Los grafos ayudan cuando importan las relaciones entre entidades",
                "Evaluar recuperación y generación por separado guía la mejora",
            ],
            "keys": [
                "Reescribe consultas conversacionales antes de buscar.",
                "Mide cada componente con preguntas y documentos etiquetados.",
                "Añade híbrida y reranking antes de probar técnicas exóticas.",
                "Comprueba la fidelidad de las citas, no solo su existencia.",
                "Clasifica los fallos antes de cambiar el modelo.",
            ],
            "example": "Un RAG jurídico responde mal a preguntas que cruzan dos normativas. El análisis muestra que recupera un solo artículo. El equipo añade expansión de consulta y un grafo de referencias entre normas; las respuestas citan ambos documentos y la revisión humana encuentra menos omisiones.",
            "caution": "Añadir más contexto no corrige una recuperación mala. Si los fragmentos relevantes no están entre los candidatos, ningún prompt puede inventar la respuesta correcta de forma fiable.",
            "search": "RAG avanzado reescritura de consulta HyDE multi-query enrutamiento híbrida reranking compresión GraphRAG evaluación fidelidad RAGAS fallos",
        },
    ],
    "quiz": {
        "id": "hllm6q",
        "title": "Cierre del módulo 06",
        "summary": [
            "La búsqueda híbrida combina precisión léxica y cobertura semántica.",
            "El chunking y los metadatos determinan qué puede recuperar y citar el sistema.",
            "RAG separa el conocimiento del modelo y lo hace actualizable y verificable.",
            "La evaluación por componentes distingue fallos de recuperación de fallos de generación.",
        ],
        "questions": [
            {
                "q": "¿Cuándo es especialmente útil la búsqueda léxica frente a la densa?",
                "options": [
                    "Cuando la consulta usa sinónimos que no aparecen en el documento",
                    "Cuando se busca un código, nombre propio o término exacto",
                    "Cuando el usuario escribe en otro idioma",
                    "Cuando no hay índice construido",
                ],
                "answer": 1,
                "why": "BM25 puntúa coincidencias exactas y términos raros. Para referencias, identificadores y nombres, esa precisión supera a la similitud semántica.",
            },
            {
                "q": "¿Qué problema resuelve el reranking?",
                "options": [
                    "Extraer texto de un PDF",
                    "Reordenar los candidatos con un modelo más preciso antes de responder",
                    "Reducir el vocabulario del tokenizador",
                    "Entrenar el modelo desde cero",
                ],
                "answer": 1,
                "why": "El recuperador inicial prioriza cobertura; el cross-encoder examina la pareja consulta-documento y mejora el orden de los primeros resultados.",
            },
            {
                "q": "¿Por qué conviene conservar el encabezado de sección en cada fragmento?",
                "options": [
                    "Para aumentar el número de tokens",
                    "Para que el fragmento mantenga el contexto que le da significado",
                    "Para que el índice sea más grande",
                    "Para evitar usar metadatos",
                ],
                "answer": 1,
                "why": "Un pasaje aislado puede ser ambiguo. El título de la sección sitúa el contenido y ayuda tanto al recuperador como al modelo a interpretarlo.",
            },
            {
                "q": "¿Qué mide la fidelidad en un sistema RAG?",
                "options": [
                    "La velocidad de la respuesta",
                    "Si las afirmaciones se sostienen en las fuentes recuperadas",
                    "El número de documentos indexados",
                    "La calidad gramatical del prompt",
                ],
                "answer": 1,
                "why": "La fidelidad comprueba que la respuesta no añade datos sin respaldo. Es distinta de la relevancia, que mide si contesta la pregunta, y del recall del recuperador.",
            },
        ],
        "exercises": [
            "Construye diez consultas con sus documentos relevantes y calcula recall@5 antes y después de añadir híbrida.",
            "Toma un documento largo y prueba tres tamaños de chunk; anota qué se pierde y qué se duplica.",
            "Clasifica cinco respuestas erróneas de un RAG en fallos de recuperación, contexto o generación.",
        ],
        "search": "cierre búsqueda semántica híbrida chunking RAG reranking citas fidelidad evaluación reescritura GraphRAG fallos",
    },
}
