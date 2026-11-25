MODULE = {
    "num": "03",
    "title": "Dentro del Transformer",
    "sub": "Qué ocurre entre el prompt y la respuesta",
    "lessons": [
        {
            "id": "hllm3l1",
            "lnum": 1,
            "title": "El recorrido de una predicción",
            "minutes": 9,
            "lead": "Cuando envías un prompt, el modelo no «piensa» una respuesta completa: calcula una distribución sobre el siguiente token, elige uno, lo añade y repite. Comprender ese bucle —capas, logits, softmax y muestreo— permite explicar la latencia, la creatividad y muchas respuestas aparentemente erráticas.",
            "diagram": ("flow", ["Tokens", "Bloques", "Logits", "Softmax"]),
            "caption": "La entrada atraviesa los bloques del Transformer, se proyecta sobre el vocabulario y se normaliza para elegir el siguiente token.",
            "sections": [
                {
                    "h": "La pila de bloques",
                    "p": [
                        "La secuencia de identificadores entra en la matriz de embeddings y recibe información posicional. Después atraviesa una serie de bloques idénticos en estructura pero distintos en pesos. Cada bloque combina una capa de atención con una red feed-forward, unidas por conexiones residuales y normalizaciones que estabilizan el flujo de información.",
                        "La atención mezcla información entre posiciones; la red feed-forward transforma cada posición por separado. Las conexiones residuales permiten que el gradiente fluya y que el modelo conserve la señal original mientras añade matices. Repetir este patrón decenas de veces construye representaciones cada vez más abstractas.",
                        "Al final, una proyección lleva el vector de la última posición al tamaño del vocabulario. Esa proyección produce una puntuación por cada token posible. No es una probabilidad todavía: son logits, números arbitrarios que pueden ser negativos y que solo tienen sentido en comparación con los demás.",
                    ],
                },
                {
                    "h": "De logits a una decisión",
                    "p": [
                        "Softmax convierte los logits en una distribución de probabilidad que suma uno. El token con mayor probabilidad no siempre se elige: en modo muestreo se sortea según esa distribución. Ahí entran la temperatura y los filtros de vocabulario, que se estudian en la lección siguiente.",
                        "El token elegido se añade a la secuencia y el proceso vuelve a empezar. Cada iteración genera un único token, aunque el modelo procese todo el contexto para decidirlo. La respuesta final es el resultado de decenas o cientos de decisiones locales, no de un plan global escrito de antemano.",
                        "Por eso dos ejecuciones con el mismo prompt pueden diferir. También por eso un error temprano arrastra a los siguientes: el modelo condiciona cada paso con lo que ya escribió. La coherencia emerge de la secuencia, y con ella la posibilidad de que una alucinación se vuelva internamente consistente.",
                    ],
                },
                {
                    "h": "Dónde se va el tiempo",
                    "p": [
                        "La generación tiene dos fases. En el prefill, el modelo procesa todo el prompt en paralelo y llena la caché de claves y valores. En el decode, genera un token cada vez y reutiliza esa caché. El prefill se parece a una multiplicación de matrices grande; el decode está limitado por el ancho de banda de memoria.",
                        "Esa diferencia explica por qué un prompt largo tarda en arrancar y por qué la velocidad por token no mejora simplemente con más núcleos. El cuello de botella del decode es leer los pesos y la caché, no hacer más operaciones. Agrupar varias peticiones en un lote mejora el aprovechamiento del hardware.",
                        "La latencia percibida no es solo el tiempo total. El tiempo hasta el primer token y la velocidad de emisión afectan a la sensación de fluidez. Para un chat, conviene optimizar ambos; para un proceso por lotes, importa el coste total. Medir esas métricas por separado evita optimizar la equivocada.",
                    ],
                },
            ],
            "brief": [
                "El modelo predice un token cada vez y lo reincorpora a la entrada",
                "Los bloques alternan atención, feed-forward, residuales y normalización",
                "Softmax transforma logits en una distribución de probabilidad",
                "Prefill y decode tienen cuellos de botella distintos",
            ],
            "keys": [
                "Explica la generación como un bucle de predicción, no como una copia",
                "Distingue logits de probabilidades y de tokens elegidos",
                "Mide tiempo hasta el primer token y velocidad por separado",
                "Recuerda que un token erróneo condiciona los siguientes",
                "Optimiza prefill y decode con estrategias diferentes",
            ],
            "example": "Un equipo se queja de que su asistente tarda cinco segundos en empezar pero luego escribe rápido. El perfil muestra un prompt de ocho mil tokens: el prefill domina la espera. Recortan el contexto recuperado y la latencia inicial baja a menos de dos segundos sin cambiar el modelo.",
            "caution": "Pedir «la respuesta completa» no cambia el mecanismo: el modelo sigue generando token a token. Los modelos que muestran razonamiento extenso pagan ese coste en latencia y en tokens facturables.",
            "search": "forward pass transformer bloques logits softmax muestreo prefill decode latencia tokens por segundo GPU inferencia vocabulario",
        },
        {
            "id": "hllm3l2",
            "lnum": 2,
            "title": "Decodificar y recordar",
            "minutes": 10,
            "lead": "Elegir el siguiente token parece trivial, pero de esa decisión dependen el tono, la variedad y la fiabilidad. Además, el modelo solo puede recordar lo que cabe en su ventana de contexto y lo que guarda en la caché. Decodificación y memoria son dos palancas prácticas para mejorar cualquier aplicación.",
            "diagram": ("curve", {"x": "longitud del contexto", "y": "coste por token", "a": "con KV cache", "b": "sin caché"}),
            "caption": "La caché evita recalcular el pasado, pero su memoria crece con la longitud; sin ella, el coste de cada token nuevo se dispara.",
            "sections": [
                {
                    "h": "Estrategias de decodificación",
                    "p": [
                        "La decodificación voraz elige siempre el token más probable. Es reproducible y adecuada para extracción o código, pero puede volverse repetitiva y perder alternativas globalmente mejores. El muestreo elige al azar según la distribución, lo que introduce variedad y también riesgo de divagación.",
                        "La temperatura reescala los logits antes de softmax. Una temperatura baja agudiza la distribución y acerca el comportamiento al greedy; una alta la aplana y aumenta la diversidad. Top-k limita el sorteo a los k tokens más probables; top-p, o nucleus sampling, acumula probabilidad hasta un umbral y descarta la cola larga.",
                        "Beam search mantiene varias hipótesis y elige la secuencia de mayor probabilidad conjunta. Produce resultados más probables, pero puede sonar genérico y consume más cómputo. Las penalizaciones por repetición y por presencia de tokens corrigen bucles, a costa de poder introducir rarezas. No hay una configuración universal: se ajusta con ejemplos reales.",
                    ],
                },
                {
                    "h": "La ventana de contexto",
                    "p": [
                        "La ventana de contexto es el número máximo de tokens que el modelo puede atender a la vez. Incluye el prompt, los documentos recuperados, el historial y la respuesta en curso. Cuando se supera, hay que truncar, resumir o recuperar menos información; el modelo no recuerda lo que queda fuera.",
                        "Más contexto no equivale a mejor contexto. La evidencia muestra que la información situada en el medio de ventanas muy largas puede aprovecharse peor que la del principio o el final. Amontonar documentos «por si acaso» añade ruido, coste y latencia, y a veces empeora la respuesta.",
                        "La estrategia útil es seleccionar y ordenar. Recupera los fragmentos más relevantes, sitúa los más importantes cerca de la pregunta y elimina duplicados. Si la conversación es larga, resume turnos antiguos y conserva los datos que aún condicionan la tarea. El contexto es un presupuesto, no un almacén.",
                    ],
                },
                {
                    "h": "Caché y perplejidad",
                    "p": [
                        "Durante la generación, la atención necesita las claves y los valores de todos los tokens anteriores. La KV cache los guarda para no recalcularlos en cada paso. Sin ella, el coste crecería de forma cuadrática con la longitud; con ella, cada token nuevo solo calcula su propia proyección y consulta la memoria acumulada.",
                        "La caché ocupa memoria proporcional al número de capas, cabezas, dimensiones y tokens. En contextos largos o lotes grandes puede superar a los propios pesos. Por eso existen variantes que comparten claves y valores entre cabezas o comprimen la caché. Su tamaño condiciona cuántas peticiones simultáneas caben en una GPU.",
                        "La perplejidad mide cuánto se sorprende el modelo ante un texto: es la exponencial de la entropía media por token. Un valor menor indica que el texto le resulta más predecible, pero no garantiza respuestas útiles ni veraces. Sirve para comparar modelos o ajustes en el mismo corpus, no como métrica única de calidad.",
                    ],
                },
            ],
            "brief": [
                "Greedy es reproducible; el muestreo añade variedad y riesgo",
                "Temperatura, top-k y top-p controlan la forma del sorteo",
                "La ventana de contexto es un presupuesto que hay que seleccionar",
                "La KV cache acelera la generación a cambio de memoria",
            ],
            "keys": [
                "Ajusta la decodificación por tarea, no por costumbre.",
                "Usa temperatura baja para extracción y alta solo con verificación.",
                "Ordena el contexto: el medio de ventanas largas se aprovecha peor.",
                "Resume el historial en lugar de acumular turnos sin límite.",
                "Mide memoria de caché al planificar concurrencia.",
            ],
            "example": "Un asistente de atención al cliente divaga y repite frases. El equipo baja la temperatura a 0,3, limita top-p a 0,9 y añade una penalización suave por repetición. La variedad baja, pero las respuestas se vuelven más consistentes. Para el resumen creativo de incidencias mantienen una configuración distinta.",
            "caution": "Subir la temperatura no hace al modelo «más inteligente»: solo reparte probabilidad hacia tokens menos probables. En tareas con respuesta correcta, suele aumentar los errores.",
            "search": "decodificación greedy muestreo temperatura top-k top-p beam search contexto ventana KV cache perplejidad memoria latencia repetición",
        },
        {
            "id": "hllm3l3",
            "lnum": 3,
            "title": "Mejoras modernas de arquitectura",
            "minutes": 9,
            "lead": "El Transformer original funcionaba, pero era caro. La investigación posterior redujo el coste de la atención, estabilizó el entrenamiento, mejoró la codificación de posiciones y añadió capacidad sin activar todos los parámetros. Estas mejoras explican por qué los modelos actuales pueden procesar contextos enormes con presupuestos razonables.",
            "diagram": ("stack", ["Atención eficiente", "RoPE", "Normalización", "MLP con compuerta"]),
            "caption": "Las mejoras modernas se combinan dentro del bloque: atención más barata, posiciones rotatorias, normalización estable y redes feed-forward con compuertas.",
            "sections": [
                {
                    "h": "Atender sin calcular todo",
                    "p": [
                        "La auto-atención compara cada token con todos los demás, de modo que su coste crece con el cuadrado de la longitud. Duplicar el contexto cuadruplica el trabajo de atención. Para secuencias largas, ese término domina el cómputo y la memoria, y limita tanto el entrenamiento como la inferencia.",
                        "La atención multi-consulta comparte una única clave y un único valor entre todas las cabezas, lo que reduce mucho la caché. La atención por grupos ofrece un punto intermedio: varias consultas comparten un grupo de claves y valores. Es el compromiso habitual en modelos abiertos, porque conserva calidad y recorta memoria.",
                        "FlashAttention no cambia la matemática: reorganiza el cálculo por bloques para reducir lecturas y escrituras en memoria. Las ventanas deslizantes limitan cada token a un vecindario, útil para texto local pero insuficiente si la respuesta depende de un dato lejano. Cada técnica ataca una parte distinta del problema.",
                    ],
                },
                {
                    "h": "Bloques más estables y expresivos",
                    "p": [
                        "El orden de normalización importa. Colocar la normalización antes de la atención y del feed-forward, con conexiones residuales limpias, facilita entrenar redes muy profundas. RMSNorm simplifica el cálculo frente a LayerNorm y se ha vuelto común por su eficiencia y estabilidad.",
                        "Las redes feed-forward suelen contener la mayor parte de los parámetros. Sustituir la activación simple por variantes con compuerta, como SwiGLU, mejora la capacidad por parámetro. La compuerta aprende a modular cuánta información pasa, lo que aporta expresividad sin cambiar la estructura general del bloque.",
                        "Los residuales siguen siendo esenciales: permiten que la información y el gradiente atraviesen muchas capas. Un bloque moderno no es una revolución, sino una acumulación de ajustes que, juntos, hacen viable entrenar y servir modelos de cientos de miles de millones de parámetros.",
                    ],
                },
                {
                    "h": "Posición, contexto y expertos",
                    "p": [
                        "RoPE codifica la posición rotando las consultas y las claves de cada token. La atención depende así de la diferencia relativa entre posiciones, lo que generaliza mejor a longitudes no vistas. Sus variantes permiten extender el contexto durante el ajuste, aunque la calidad en textos muy largos sigue necesitando evaluación específica.",
                        "La mezcla de expertos reemplaza una red feed-forward grande por varias especializadas y un enrutador que activa solo unas pocas por token. El modelo puede tener muchos parámetros totales y usar una fracción por paso. El reto es equilibrar la carga: si el enrutador concentra todo en unos expertos, se desperdicia capacidad y se degrada el servicio.",
                        "Ninguna mejora elimina los compromisos. Más contexto cuesta memoria; más expertos complican el despliegue; una atención más barata puede perder detalle global. La arquitectura se elige junto con el hardware, el presupuesto y la tarea. Un modelo eficiente mal servido rinde peor que uno modesto bien ajustado.",
                    ],
                },
            ],
            "brief": [
                "La atención cuadrática es el principal límite para contextos largos",
                "MQA y GQA reducen la caché compartiendo claves y valores",
                "RMSNorm, pre-normalización y SwiGLU estabilizan y mejoran el bloque",
                "RoPE y MoE amplían contexto y capacidad con nuevos compromisos",
            ],
            "keys": [
                "Relaciona cada mejora con el recurso que ahorra.",
                "No confundas FlashAttention con una atención de menor alcance.",
                "Evalúa la calidad en contextos largos, no solo la ventana nominal.",
                "Vigila el equilibrio de expertos si usas MoE.",
                "Diseña arquitectura, hardware y serving como un solo sistema.",
            ],
            "example": "Un servicio de análisis de contratos necesita contextos de 64.000 tokens. Con atención completa, la caché limita a dos peticiones por GPU. Al pasar a un modelo con GQA y FlashAttention, el equipo sirve seis peticiones con una calidad similar en su conjunto de evaluación. La mejora vino del despliegue, no de un modelo más grande.",
            "caution": "Una ventana de 128.000 tokens no garantiza que el modelo use bien todo el contenido. Sin pruebas de recuperación en el medio y en los extremos, el contexto extra es solo un coste mayor.",
            "search": "arquitectura transformer atención eficiente MQA GQA FlashAttention ventana deslizante RMSNorm SwiGLU RoPE mezcla de expertos MoE contexto largo",
        },
    ],
    "quiz": {
        "id": "hllm3q",
        "title": "Cierre del módulo 03",
        "summary": [
            "La generación es un bucle de predicción del siguiente token con softmax y muestreo.",
            "Prefill y decode tienen perfiles de rendimiento distintos y se optimizan por separado.",
            "Temperatura, top-k, top-p y beam search cambian el equilibrio entre variedad y control.",
            "MQA, GQA, FlashAttention, RoPE y MoE responden a límites concretos de memoria y cómputo.",
        ],
        "questions": [
            {
                "q": "¿Qué produce la capa final del modelo antes de aplicar softmax?",
                "options": [
                    "Una lista de documentos recuperados",
                    "Un vector de logits con una puntuación por token del vocabulario",
                    "El texto ya traducido",
                    "Una matriz de embeddings de entrada",
                ],
                "answer": 1,
                "why": "La proyección de salida asigna una puntuación a cada token. Softmax las convierte en probabilidades; el muestreo elige una. Los documentos pertenecen a otra etapa del sistema.",
            },
            {
                "q": "¿Qué efecto tiene bajar la temperatura durante la decodificación?",
                "options": [
                    "Aumenta la variedad de las respuestas",
                    "Agudiza la distribución y favorece los tokens más probables",
                    "Reduce el tamaño del vocabulario",
                    "Elimina la necesidad de contexto",
                ],
                "answer": 1,
                "why": "Al dividir los logits por un valor menor, las diferencias se amplifican y los tokens más probables concentran casi toda la masa. El resultado es más determinista.",
            },
            {
                "q": "¿Para qué sirve la KV cache?",
                "options": [
                    "Para guardar los documentos del usuario en disco",
                    "Para reutilizar claves y valores ya calculados y no reprocesar el contexto",
                    "Para traducir el prompt a otro idioma",
                    "Para aumentar el vocabulario del modelo",
                ],
                "answer": 1,
                "why": "Sin caché, cada token nuevo recalcularía las proyecciones de todo el pasado. La caché acelera la generación a cambio de memoria que crece con el contexto.",
            },
            {
                "q": "¿Qué problema resuelve principalmente GQA?",
                "options": [
                    "La falta de datos de entrenamiento",
                    "El tamaño de la caché de claves y valores en la atención",
                    "La tokenización de emojis",
                    "La elección de la función de activación",
                ],
                "answer": 1,
                "why": "GQA comparte claves y valores entre grupos de consultas, reduciendo la memoria de la caché y manteniendo varias cabezas de consulta para conservar calidad.",
            },
        ],
        "exercises": [
            "Con un modelo pequeño, compara tres temperaturas en la misma tarea y anota variedad, errores y tiempo.",
            "Diseña un experimento para comprobar si tu modelo aprovecha un dato colocado en el centro de un contexto largo.",
            "Calcula de forma aproximada cómo cambia la memoria de la KV cache al duplicar contexto, capas y cabezas.",
        ],
        "search": "cierre transformer logits softmax decodificación temperatura top-p contexto KV cache GQA FlashAttention RoPE MoE",
    },
}
