MODULE = {
    "num": "02",
    "title": "Tokens y embeddings",
    "sub": "La materia prima numérica del modelo",
    "lessons": [
        {
            "id": "hllm2l1",
            "lnum": 1,
            "title": "Tokenización en la práctica",
            "minutes": 9,
            "lead": "Antes de calcular nada, el modelo tiene que decidir qué unidades de texto procesa. El tokenizador corta la entrada en piezas, las traduce a identificadores y añade marcas especiales. Esa decisión parece mecánica, pero determina el coste, el multilingüismo y la capacidad de representar palabras poco frecuentes.",
            "diagram": ("flow", ["Texto", "Normalizar", "Subpalabras", "IDs"]),
            "caption": "El tokenizador normaliza el texto, lo divide en subpalabras y las convierte en identificadores del vocabulario antes de que empiece el modelo.",
            "sections": [
                {
                    "h": "Del carácter al identificador",
                    "p": [
                        "El primer paso suele ser una normalización ligera: unificar espacios, tratar mayúsculas o descomponer acentos según la variante. Después, un algoritmo de segmentación divide el texto en tokens. Finalmente, cada token se busca en el vocabulario y se sustituye por un número entero. El modelo solo ve esa secuencia de identificadores.",
                        "El vocabulario incluye tokens especiales que no provienen del texto: inicio y fin de secuencia, relleno, separadores de turno o máscaras. Su posición y significado dependen del modelo; usar los de otro tokenizador produce resultados silenciosamente incorrectos. Por eso el tokenizador y los pesos deben descargarse siempre juntos.",
                        "La salida no es reversible al cien por cien. Varias cadenas pueden normalizarse al mismo token, y algunos caracteres raros se representan con varios fragmentos. Para medir longitudes, costes o límites de contexto hay que contar tokens, no palabras ni caracteres. Una regla práctica en español es que un token ronda las tres cuartas partes de una palabra, con mucha variación.",
                    ],
                },
                {
                    "h": "Subpalabras y BPE",
                    "p": [
                        "La tokenización por subpalabras busca un equilibrio: un vocabulario manejable que pueda construir cualquier palabra. Byte Pair Encoding empieza con unidades mínimas y fusiona repetidamente los pares más frecuentes del corpus. El resultado son piezas como «token», «ización» o «es» que se recombinan para formar términos nuevos.",
                        "Este enfoque resuelve el problema de las palabras fuera del vocabulario. Un neologismo, una marca o una palabra en otro idioma se descompone en fragmentos conocidos en lugar de convertirse en un símbolo desconocido. También reparte la información: las raíces frecuentes ocupan un token y las terminaciones se reutilizan en muchas palabras.",
                        "La variante byte-level garantiza que cualquier secuencia de bytes tenga representación, a costa de fragmentar más los textos alejados del corpus de entrenamiento. Un tokenizador entrenado sobre todo en inglés gastará más tokens en español, árabe o código. Esa diferencia encarece la API y reduce el espacio útil dentro de la ventana de contexto.",
                    ],
                },
                {
                    "h": "Comparar tokenizadores con datos",
                    "p": [
                        "No todos los tokenizadores parten el mismo texto igual. Para compararlos se mide la fertilidad: cuántos tokens produce por palabra o por carácter en un corpus representativo. Un modelo con vocabulario adaptado a tu idioma procesará más contenido en la misma ventana y pagará menos por documento.",
                        "También importan los números, los emojis y el código. Una cifra larga puede ocupar muchos tokens y romper el razonamiento aritmético; una indentación repetida consume contexto sin aportar significado. Si tu aplicación trata facturas, nombres químicos o programas, conviene inspeccionar cómo se fragmentan esos casos concretos.",
                        "La longitud del token es una decisión de ingeniería, no un detalle. Afecta a la latencia, al coste, a la cantidad de ejemplos que caben en un prompt y a la calidad de las tareas que dependen de caracteres. Medir con el tokenizador real del modelo evita sorpresas cuando el sistema llegue a producción.",
                    ],
                },
            ],
            "brief": [
                "El tokenizador normaliza, segmenta y convierte texto en identificadores",
                "BPE construye un vocabulario de subpalabras reutilizables",
                "La tokenización byte-level cubre cualquier texto, pero puede fragmentar más",
                "Contar tokens es distinto de contar palabras o caracteres",
            ],
            "keys": [
                "Carga siempre tokenizador y pesos del mismo modelo.",
                "Mide la fertilidad en el idioma y el formato de tus datos.",
                "Revisa cómo se parten números, emojis y código.",
                "Ajusta límites de contexto con tokens reales, no con estimaciones.",
                "Elige modelos con vocabulario adecuado si el coste por texto importa.",
            ],
            "example": "Un equipo calcula que una consulta media tiene 120 palabras y reserva 200 tokens de contexto. Al medir con el tokenizador real descubre que los nombres de producto y las referencias alfanuméricas se fragmentan y que la media sube a 340 tokens. Reajusta el presupuesto y evita truncar justo la parte que contiene la pregunta.",
            "caution": "Usar el tokenizador de otro modelo no lanza un error: produce identificadores válidos con significados distintos. El fallo aparece como una calidad inexplicablemente mala, no como una excepción.",
            "search": "tokenización tokenizador tokens subpalabras BPE byte-level vocabulario identificadores fertilidad contexto coste multilingüe números emojis",
        },
        {
            "id": "hllm2l2",
            "lnum": 2,
            "title": "Embeddings de tokens y contexto",
            "minutes": 9,
            "lead": "Dentro del modelo, cada identificador se convierte en un vector. Ese vector inicial es estático, pero las capas de atención lo transforman hasta producir una representación que depende de la frase completa. La diferencia entre ambos niveles explica por qué un mismo término puede significar cosas distintas sin cambiar de identificador.",
            "diagram": ("matrix", {"rows": 6, "cols": 10, "mark": 34}),
            "caption": "La matriz de embeddings asigna una fila a cada token del vocabulario; las dimensiones se aprenden y se reorganizan en las capas siguientes.",
            "sections": [
                {
                    "h": "La matriz que traduce identificadores",
                    "p": [
                        "El modelo guarda una matriz con una fila por token y una columna por dimensión. El identificador funciona como índice: la fila correspondiente es el embedding de entrada. Esos valores se aprenden durante el preentrenamiento y contienen regularidades de uso, no definiciones escritas por una persona.",
                        "A ese vector se le suma información posicional para que el modelo sepa dónde está cada token. Sin ella, la atención sería invariante al orden y «perro muerde hombre» equivaldría a «hombre muerde perro». Las posiciones pueden codificarse con senos y cosenos, con embeddings aprendidos o con rotaciones relativas como RoPE.",
                        "La dimensión típica va de unos cientos a varios miles. Más dimensiones permiten matices, pero multiplican memoria y cómputo. La matriz de embeddings puede compartir pesos con la capa de salida, lo que reduce parámetros y alinea la representación de entrada con la predicción del siguiente token.",
                    ],
                },
                {
                    "h": "El mismo token, vectores distintos",
                    "p": [
                        "Tras la primera capa, el vector de un token deja de ser una simple consulta al diccionario. La atención mezcla información de las posiciones relevantes y el bloque feed-forward transforma el resultado. En la capa final, «banco» en una oración financiera y «banco» en un parque ya no comparten representación.",
                        "Las capas iniciales suelen capturar rasgos locales y sintácticos; las intermedias, relaciones semánticas; las finales, información orientada al objetivo de entrenamiento. No hay una capa universalmente mejor para todas las tareas. Extraer representaciones para clasificar exige probar y validar qué profundidad funciona mejor.",
                        "Esta contextualización es la ventaja central frente a los embeddings estáticos de palabra. También implica que no se puede precalcular un único vector por palabra para todo uso: hay que procesar la frase. Los modelos de representación y los generativos aprovechan ese mismo principio con objetivos distintos.",
                    ],
                },
                {
                    "h": "Medir similitud sin engañarse",
                    "p": [
                        "La similitud coseno compara la dirección de dos vectores y es la métrica habitual porque ignora la magnitud. Un valor cercano a uno indica orientaciones parecidas; cerca de cero, independencia; negativo, oposición. Para embeddings normalizados, el producto escalar ofrece el mismo orden y es más rápido de calcular.",
                        "Sin embargo, comparar estados ocultos crudos de un modelo generativo no siempre produce buenos resultados. Esas representaciones pueden estar dominadas por unas pocas direcciones comunes y mostrar alta similitud entre textos poco relacionados. Los modelos de embedding de frase se entrenan específicamente para que la distancia sea útil.",
                        "Antes de confiar en una métrica conviene mirar ejemplos cercanos y lejanos, comprobar la distribución de puntuaciones y evaluar con un conjunto etiquetado. La similitud geométrica es una herramienta, no una verdad semántica. Un umbral copiado de otro dominio suele clasificar mal en el tuyo.",
                    ],
                },
            ],
            "brief": [
                "Cada token se indexa en una matriz de embeddings aprendida",
                "La posición se añade para que el orden importe",
                "Las capas convierten el vector estático en una representación contextual",
                "La similitud coseno ayuda, pero debe validarse en el dominio",
            ],
            "keys": [
                "No confundas embedding de entrada con estado oculto final.",
                "Prueba varias capas al extraer representaciones para una tarea.",
                "Normaliza los vectores si vas a usar producto escalar.",
                "Valida umbrales de similitud con datos etiquetados propios.",
                "Prefiere modelos de embedding de frase para comparar textos completos.",
            ],
            "example": "Un buscador interno compara el estado oculto de la última capa de un modelo generativo y obtiene resultados mediocres. Al cambiar a un modelo de embedding de frase entrenado con pares pregunta-respuesta, los documentos relevantes suben y la similitud entre textos no relacionados baja. La diferencia está en el objetivo de entrenamiento, no en la dimensión.",
            "caution": "Un vector de 4.096 dimensiones no es automáticamente mejor que uno de 384. Si el modelo no fue entrenado para medir similitud, la dimensión extra solo añade coste y ruido.",
            "search": "embeddings tokens matriz contextual posición similitud coseno estados ocultos capas dimensionalidad representación semántica normalización",
        },
        {
            "id": "hllm2l3",
            "lnum": 3,
            "title": "Embeddings de texto y recomendación",
            "minutes": 9,
            "lead": "Un embedding de frase resume un párrafo entero en un vector comparable. Esa idea alimenta buscadores, sistemas de recomendación y agrupamiento de documentos. Detrás hay decisiones sobre cómo agregar tokens, cómo entrenar con pares y cómo evitar que el sistema amplifique los sesgos de popularidad.",
            "diagram": ("flow", ["Texto", "Embedding", "Índice", "Sugerencia"]),
            "caption": "El texto se convierte en un vector, se indexa y se compara con otros para recuperar o recomendar el elemento más afín.",
            "sections": [
                {
                    "h": "De tokens a un vector de frase",
                    "p": [
                        "Para representar una frase hay que reducir muchos vectores de token a uno solo. Una opción es promediar; otra, usar el token especial de clasificación; otra, aplicar pooling ponderado por atención. Los modelos de embedding de frase se entrenan para que esa agregación produzca vectores útiles al comparar oraciones completas.",
                        "El entrenamiento contrastivo construye parejas positivas y negativas. Las positivas son paráfrasis, pregunta-respuesta o título-resumen; las negativas son textos no relacionados, a veces difíciles de distinguir. La pérdida acerca las positivas y aleja las negativas, de modo que la geometría resultante sirva para recuperar.",
                        "La calidad depende de los negativos. Si son demasiado fáciles, el modelo aprende a separar temas obvios pero falla ante matices. Los negativos minados, que el propio modelo confunde, fuerzan representaciones más finas. Es la misma lógica de un buen examen: las preguntas triviales no discriminan.",
                    ],
                },
                {
                    "h": "word2vec y la intuición vectorial",
                    "p": [
                        "word2vec popularizó la idea de aprender vectores prediciendo contexto. En skip-gram, una palabra central debe predecir las que aparecen alrededor; en continuous bag-of-words, el contexto predice la palabra central. Entrenar millones de frases coloca términos de uso parecido en posiciones cercanas.",
                        "El método original usaba softmax sobre todo el vocabulario, caro de calcular. La solución fue el muestreo negativo: en cada paso se distingue la palabra observada de unas pocas palabras aleatorias. Ese truco hace viable el entrenamiento y sigue apareciendo en sistemas de recuperación y recomendación.",
                        "Las analogías vectoriales, como «rey - hombre + mujer ≈ reina», se volvieron famosas, pero no deben tomarse como razonamiento conceptual. Reflejan regularidades del corpus y fallan en muchos casos. Su valor histórico está en demostrar que la semántica distribucional se puede capturar con geometría.",
                    ],
                },
                {
                    "h": "Recomendar con vectores",
                    "p": [
                        "En recomendación, cada usuario y cada elemento pueden representarse en el mismo espacio. Un modelo de dos torres aprende una torre para usuarios y otra para elementos, y acerca los pares que interactúan. La puntuación de una recomendación es la similitud entre ambos vectores, calculable con un índice aproximado.",
                        "Este enfoque maneja bien catálogos grandes y permite incorporar contenido: título, descripción o imagen. También sufre el problema de arranque en frío cuando un elemento nuevo no tiene interacciones. Los embeddings de contenido ofrecen una salida, aunque su calidad depende de que la descripción refleje lo que al usuario le importa.",
                        "El riesgo es el bucle de retroalimentación. Si el sistema solo muestra lo popular, recoge interacciones de lo popular y refuerza esa preferencia. La evaluación debe incluir diversidad, cobertura y justicia, no solo precisión inmediata. Un recomendador que optimiza clics puede degradar la experiencia a largo plazo.",
                    ],
                },
            ],
            "brief": [
                "Un embedding de frase agrega tokens en un vector comparable",
                "El aprendizaje contrastivo acerca positivas y aleja negativas",
                "Los negativos difíciles mejoran la capacidad de discriminación",
                "La recomendación vectorial hereda sesgos de popularidad y feedback",
            ],
            "keys": [
                "Elige el pooling según el modelo, no por intuición.",
                "Entrena o ajusta con negativos representativos del dominio.",
                "Evalúa recuperación con métricas de ranking, no solo exactitud.",
                "Incorpora contenido para mitigar el arranque en frío.",
                "Vigila diversidad y bucles de retroalimentación en recomendación.",
            ],
            "example": "Una plataforma de cursos convierte cada descripción en un embedding y recomienda los más cercanos al perfil del estudiante. Al principio solo usa clics, y el sistema repite los mismos cursos populares. Al añadir negativos difíciles y métricas de diversidad, las recomendaciones cubren mejor el catálogo sin perder relevancia.",
            "caution": "Dos textos pueden tener una similitud alta porque comparten plantilla o jerga, no porque traten el mismo tema. Revisa los vecinos reales antes de confiar en el ranking.",
            "search": "embeddings de frase documentos word2vec skip-gram muestreo negativo contrastivo recomendación dos torres similitud ranking sesgo popularidad",
        },
    ],
    "quiz": {
        "id": "hllm2q",
        "title": "Cierre del módulo 02",
        "summary": [
            "El tokenizador define las unidades que el modelo puede procesar y condiciona coste y contexto.",
            "BPE y sus variantes construyen vocabularios de subpalabras reutilizables.",
            "La representación de un token cambia con el contexto a través de las capas.",
            "Los embeddings de frase y de usuario permiten buscar, agrupar y recomendar.",
        ],
        "questions": [
            {
                "q": "¿Por qué no se debe usar el tokenizador de un modelo con los pesos de otro?",
                "options": [
                    "Porque el tokenizador es más lento",
                    "Porque los identificadores apuntan a filas distintas y el significado se corrompe",
                    "Porque cambia el color de la interfaz",
                    "Porque impide usar la GPU",
                ],
                "answer": 1,
                "why": "Cada vocabulario asigna identificadores a sus propias piezas. Un identificador válido en un modelo puede corresponder a otro token en el segundo, sin que aparezca ningún error.",
            },
            {
                "q": "¿Qué ventaja aporta la tokenización por subpalabras?",
                "options": [
                    "Elimina por completo los errores gramaticales",
                    "Representa palabras nuevas combinando fragmentos conocidos",
                    "Reduce el vocabulario a una sola palabra",
                    "Hace innecesario el entrenamiento",
                ],
                "answer": 1,
                "why": "Al descomponer términos poco frecuentes en piezas del vocabulario, el modelo puede representarlos sin un símbolo especial de desconocido.",
            },
            {
                "q": "¿Qué hace el entrenamiento contrastivo con las parejas de textos?",
                "options": [
                    "Acerca las relacionadas y aleja las no relacionadas en el espacio vectorial",
                    "Convierte todo el texto en bag-of-words",
                    "Elimina las palabras vacías del vocabulario",
                    "Genera imágenes a partir de descripciones",
                ],
                "answer": 0,
                "why": "La pérdida contrastiva premia que las parejas positivas queden cerca y que las negativas queden lejos, de modo que la distancia sirva para recuperar o clasificar.",
            },
            {
                "q": "¿Por qué un recomendador puramente vectorial puede volverse repetitivo?",
                "options": [
                    "Porque los vectores no se pueden normalizar",
                    "Porque aprende de las interacciones que él mismo genera y refuerza lo popular",
                    "Porque siempre elige el vector de mayor dimensión",
                    "Porque no admite catálogos grandes",
                ],
                "answer": 1,
                "why": "El bucle de retroalimentación concentra la exposición en pocos elementos, que reciben más clics y refuerzan su ventaja. Medir diversidad y cobertura ayuda a detectarlo.",
            },
        ],
        "exercises": [
            "Cuenta con el tokenizador de un modelo real los tokens de un párrafo en español y en inglés, y calcula la diferencia porcentual.",
            "Escribe cinco consultas y cinco documentos de tu dominio; ordena a mano los documentos relevantes y compáralo después con un ranking por similitud.",
            "Diseña un par de torres para recomendar un catálogo pequeño e indica qué señales usarías para cada torre.",
        ],
        "search": "cierre tokens tokenización BPE embeddings contextuales frase word2vec contrastivo recomendación similitud ranking sesgo",
    },
}
