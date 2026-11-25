MODULE = {
    "num": "01",
    "title": "Del texto al modelo",
    "sub": "Cómo el lenguaje se convirtió en vectores y atención",
    "lessons": [
        {
            "id": "hllm1l1",
            "lnum": 1,
            "title": "Lenguaje convertido en vectores",
            "minutes": 9,
            "lead": "Un modelo de lenguaje no ve letras ni palabras: ve números. La historia de la IA del lenguaje es, en buena medida, la historia de cómo representar el texto para que las operaciones matemáticas capturen significado. Pasar de contar palabras a aprender vectores densos fue el primer salto que hizo posibles los modelos actuales.",
            "diagram": ("stack", ["Texto", "Bag-of-words", "Embeddings densos", "Contexto"]),
            "caption": "Cada nivel añade información: del recuento de palabras se pasa a vectores aprendidos y, después, a representaciones que dependen del contexto.",
            "sections": [
                {
                    "h": "Contar palabras tiene un techo",
                    "p": [
                        "La forma más antigua de representar un texto es contar sus palabras. El resultado, llamado bag-of-words, es un vector enorme donde cada posición corresponde a un término del vocabulario y el valor es su frecuencia. Es simple, rápido y todavía útil para líneas base, pero destruye el orden: «el perro muerde al hombre» y «el hombre muerde al perro» producen el mismo vector.",
                        "El recuento tampoco entiende sinónimos. «Coche» y «automóvil» ocupan dimensiones distintas aunque signifiquen casi lo mismo, mientras que «banco» de sentarse y «banco» de dinero comparten una sola posición. El modelo ve coincidencias superficiales, no relaciones de significado, y necesita muchísimos ejemplos para compensar esa ceguera.",
                        "A esto se suma la dispersión. Un vocabulario de cien mil palabras genera vectores de cien mil dimensiones en los que casi todo son ceros. Comparar dos documentos se vuelve costoso y estadísticamente frágil: la mayoría de las dimensiones no aporta señal. La representación dispersa funciona como índice, no como comprensión.",
                    ],
                },
                {
                    "h": "Vectores densos y aprendidos",
                    "p": [
                        "Un embedding es un vector relativamente corto, de cientos o miles de dimensiones, en el que cada número se aprende a partir de datos. En lugar de reservar una dimensión por palabra, el entrenamiento coloca palabras con usos parecidos en regiones cercanas del espacio. La geometría del vector pasa a codificar similitud.",
                        "Esa propiedad es la que hace útiles a los embeddings. Si «factura» y «recibo» están cerca, un buscador puede encontrar un documento aunque no comparta la palabra exacta. Si «Madrid» está cerca de «España» y lejos de «ensalada», el modelo captura parte de la estructura del mundo sin que nadie le haya dado una definición explícita.",
                        "Los vectores pueden representar unidades muy distintas: tokens, palabras, frases, documentos, imágenes o productos. La idea común es siempre la misma: convertir un objeto en una posición dentro de un espacio donde la distancia aproxima la relación semántica. Esa abstracción sirve para buscar, clasificar, recomendar y alimentar la memoria de un modelo generativo.",
                    ],
                },
                {
                    "h": "Del símbolo a la red neuronal",
                    "p": [
                        "Los primeros sistemas de lenguaje se construían con reglas gramaticales y diccionarios. Funcionaban en dominios estrechos y se rompían ante la ambigüedad. Después llegaron los modelos estadísticos, que estimaban la probabilidad de una palabra dado su contexto; mejoraron la cobertura, pero seguían tratando cada palabra como un símbolo aislado.",
                        "El cambio decisivo fue aprender representaciones con redes neuronales. word2vec popularizó la idea de que una palabra se define por las que la acompañan: si dos términos aparecen en contextos similares, sus vectores deben parecerse. Otros métodos, como GloVe o los modelos de lenguaje neuronales, ampliaron esa intuición y demostraron que la geometría aprendida generaliza.",
                        "La atención y el Transformer dieron el paso siguiente: representaciones que cambian según la frase completa. Ya no basta con saber que «banco» es una palabra polisémica; el vector de «banco» en «me senté en el banco» debe diferir del de «fui al banco a pagar». Esa contextualización es la base de los modelos que se estudian en los próximos módulos.",
                    ],
                },
            ],
            "brief": [
                "Bag-of-words cuenta términos y pierde orden, sinónimos y contexto",
                "Un embedding es un vector denso donde la cercanía expresa similitud",
                "Los vectores pueden representar tokens, frases, documentos o productos",
                "La contextualización distingue significados según la frase",
            ],
            "keys": [
                "Usa bag-of-words como línea base, no como solución semántica.",
                "Piensa en embeddings como coordenadas de significado, no como tablas.",
                "Comprueba la calidad de un embedding con tareas reales de tu dominio.",
                "Distingue representación de palabra de representación contextual.",
                "Recuerda que la geometría aprendida hereda sesgos de los datos.",
            ],
            "example": "Un equipo de soporte quiere encontrar tickets parecidos. Con bag-of-words, «no puedo entrar en mi cuenta» y «la sesión no me deja acceder» apenas se relacionan. Al convertir cada ticket en un embedding de frase, ambos caen cerca y el sistema recupera casos resueltos con el mismo problema aunque el vocabulario sea distinto.",
            "caution": "Un embedding no es una definición objetiva: refleja los datos con los que se entrenó. Si el corpus asocia ciertos trabajos o países con atributos negativos, el buscador reproducirá esa asociación aunque nadie la haya programado.",
            "search": "representación texto bag-of-words embeddings densos similitud semántica word2vec tokens frases documentos contexto historia IA lenguaje vectores",
        },
        {
            "id": "hllm1l2",
            "lnum": 2,
            "title": "Atención: el mecanismo que cambió todo",
            "minutes": 10,
            "lead": "Antes de 2017, procesar una frase implicaba recorrerla paso a paso y comprimir todo en un vector final. El Transformer sustituyó esa cadena por un mecanismo de atención que permite a cada posición consultar directamente a cualquier otra. Entender qué preguntan las consultas, qué ofrecen las claves y qué transportan los valores aclara casi todo lo que viene después.",
            "diagram": ("attention", ["El", "gato", "no", "cruzó", "la", "calle", "porque", "tenía", "miedo"]),
            "caption": "La última posición consulta el contexto anterior y reparte su atención entre las piezas que explican el significado; las líneas representan ese peso.",
            "sections": [
                {
                    "h": "El cuello de botella de la secuencia",
                    "p": [
                        "Las redes recurrentes leían una palabra, actualizaban un estado y pasaban a la siguiente. Esa dependencia secuencial impedía paralelizar el entrenamiento y dificultaba conservar información de las primeras posiciones. Todo el pasado debía caber en un estado oculto de tamaño fijo, una compresión agresiva que se perdía en frases largas.",
                        "La atención resolvió ambos problemas. En lugar de arrastrar un resumen, cada posición puede mirar directamente a las demás y decidir a cuáles dar importancia. El camino entre dos palabras deja de depender de la distancia que las separa: la información puede viajar en un solo paso, y el cálculo se organiza como operaciones matriciales que aprovechan muy bien la GPU.",
                        "La idea no nació con el Transformer, pero su formulación como auto-atención escalada lo convirtió en el bloque central. El artículo que la popularizó mostró que se podía prescindir de la recurrencia y entrenar redes más grandes y más rápidas. Casi todos los modelos de lenguaje actuales descienden de esa decisión de diseño.",
                    ],
                },
                {
                    "h": "Consultas, claves y valores",
                    "p": [
                        "Cada token se proyecta en tres vectores: una consulta, una clave y un valor. La consulta expresa qué busca esa posición; la clave, qué ofrece cada posición; el valor, la información que se transferirá si la coincidencia es alta. Comparar consultas con claves produce una puntuación de relevancia para cada par de posiciones.",
                        "Las puntuaciones se dividen por la raíz de la dimensión para evitar valores demasiado grandes, se normalizan con softmax y se usan como pesos para combinar los valores. El resultado es un vector nuevo para cada token, enriquecido con la información que sus vecinos aportan. Varias cabezas de atención repiten el proceso en paralelo y capturan relaciones distintas.",
                        "La atención multi-cabeza permite que una cabeza siga dependencias gramaticales, otra resuelva pronombres y otra conecte términos del mismo tema. Sus salidas se concatenan y se proyectan de nuevo. Ninguna cabeza está programada para una tarea concreta; la especialización emerge del entrenamiento y no conviene interpretarla como una explicación literal.",
                    ],
                },
                {
                    "h": "Encoder, decoder y las tres familias",
                    "p": [
                        "En un modelo encoder-only, como BERT, todas las posiciones se ven entre sí y construyen representaciones bidireccionales. Es ideal para comprender: clasificar, reconocer entidades, medir similitud o responder preguntas extractivas. No genera texto libre porque no está entrenado para predecir la continuación, sino para reconstruir fragmentos ocultos.",
                        "En un modelo decoder-only, como la familia GPT, una máscara causal impide mirar el futuro. Cada posición solo puede atender a las anteriores, lo que convierte el entrenamiento en una tarea de predecir el siguiente token en todos los puntos de la secuencia. Esa misma restricción es la que permite generar texto de izquierda a derecha.",
                        "Los modelos encoder-decoder, como T5, separan lectura y escritura: el encoder comprende la entrada y el decoder produce la salida condicionada por ella. Son naturales para traducción, resumen o transformación de formato. Las tres familias comparten el bloque de atención, pero eligen máscaras y objetivos distintos según el uso previsto.",
                    ],
                },
            ],
            "brief": [
                "La atención conecta posiciones sin recorrer la secuencia paso a paso",
                "Consulta, clave y valor deciden qué información se transfiere",
                "Varias cabezas capturan relaciones diferentes en paralelo",
                "Encoder comprende, decoder genera y encoder-decoder transforma",
            ],
            "keys": [
                "Explica la atención como una mezcla ponderada de valores, no como magia.",
                "Relaciona cada familia de modelo con la tarea que resuelve mejor.",
                "No interpretes los pesos de atención como una explicación causal.",
                "La máscara causal es lo que hace posible la generación autorregresiva.",
                "La paralelización es una ventaja de ingeniería, no un detalle menor.",
            ],
            "example": "En «el gato no cruzó la calle porque tenía miedo», la palabra «tenía» necesita saber quién siente el miedo. La atención conecta esa forma verbal con «gato». Si la frase fuera «porque estaba cortada», la conexión relevante se desplazaría hacia «calle». El mismo mecanismo resuelve ambigüedades distintas según el contexto.",
            "caution": "Un mapa de atención vistoso no demuestra que el modelo haya razonado así. Los pesos son una parte de un circuito complejo con residuales, normalizaciones y múltiples capas; usarlos como prueba de causalidad lleva a conclusiones falsas.",
            "search": "atención transformer auto-atención consulta clave valor softmax multi-cabeza encoder decoder máscara causal BERT GPT T5 contexto",
        },
        {
            "id": "hllm1l3",
            "lnum": 3,
            "title": "Cómo se entrena y se usa un LLM",
            "minutes": 9,
            "lead": "Un modelo de lenguaje moderno no nace sabiendo seguir instrucciones. Primero aprende a continuar texto a gran escala; después se ajusta con ejemplos y, por último, se alinea con preferencias humanas. Conocer esas etapas evita atribuir al modelo capacidades que en realidad pertenecen a una fase concreta del entrenamiento.",
            "diagram": ("loop", ["Preentrenamiento", "Ajuste supervisado", "Preferencias", "Evaluación"]),
            "caption": "El ciclo de vida típico de un LLM: aprender el idioma, aprender la tarea y ajustar el comportamiento antes de evaluar y desplegar.",
            "sections": [
                {
                    "h": "Tres etapas con objetivos distintos",
                    "p": [
                        "El preentrenamiento recorre grandes corpus y entrena al modelo para predecir el siguiente token. No necesita etiquetas humanas: la propia secuencia proporciona la respuesta. De ahí surgen el conocimiento del idioma, la gramática, los hechos y cierta capacidad de razonamiento. El resultado es un modelo base, potente pero poco disciplinado.",
                        "El ajuste supervisado, o SFT, entrena con pares de instrucción y respuesta deseada. Aquí el modelo aprende el formato de asistente: seguir una petición, responder con un tono concreto, rechazar ciertas solicitudes o usar una herramienta. Es una fase mucho más pequeña en datos, pero decisiva para que el modelo resulte usable.",
                        "La fase de preferencias compara respuestas y ajusta el modelo para favorecer las mejor valoradas. RLHF entrena primero un modelo de recompensa y luego optimiza la política; DPO evita ese paso intermedio y aprende directamente de pares preferidos y rechazados. El objetivo es alinear utilidad, seguridad y estilo, no añadir conocimiento nuevo.",
                    ],
                },
                {
                    "h": "Parámetros, escala y límites",
                    "p": [
                        "Los parámetros son los números aprendidos que definen el comportamiento. Un modelo pequeño puede tener unos pocos miles de millones; uno grande, cientos. Más parámetros suelen permitir más capacidad, pero también más coste de memoria, más latencia y más energía. La calidad de los datos y del ajuste importa tanto como el tamaño.",
                        "La definición de «grande» se mueve con la tecnología. Modelos que hoy caben en un portátil habrían sido extraordinarios hace unos años, y las técnicas de cuantización y destilación acercan capacidades antes reservadas a centros de datos. Por eso conviene hablar de capacidad efectiva y de coste por tarea, no solo de número de parámetros.",
                        "La escala también trae límites. El modelo puede memorizar datos sensibles, reproducir sesgos, inventar hechos o fallar en tareas que requieren cálculo exacto. No es una base de datos ni un oráculo. Es un predictor estadístico muy expresivo que necesita contexto, verificación y límites explícitos cuando la respuesta importa.",
                    ],
                },
                {
                    "h": "Abierto, cerrado y responsabilidad",
                    "p": [
                        "Los modelos propietarios se consumen por API: se paga por uso, no se descargan y suelen ofrecer mayor capacidad sin infraestructura propia. Los modelos abiertos permiten ejecutarlos localmente, inspeccionarlos, ajustarlos y mantener los datos dentro de la organización. La elección depende de privacidad, coste, latencia, control y volumen, no de una preferencia ideológica.",
                        "La primera generación práctica suele ser una llamada mínima: construir el prompt, enviarlo, recibir texto y medir. Antes de escribir una aplicación compleja conviene comprobar la calidad en veinte casos reales, el coste por respuesta y el comportamiento ante entradas vacías o maliciosas. Esa prueba temprana evita arquitecturas construidas sobre una capacidad supuesta.",
                        "El desarrollo responsable incluye evaluar, documentar y limitar. Hay que saber qué datos se envían, cuánto se retienen, qué errores son aceptables y quién revisa las decisiones sensibles. Un sistema que redacta borradores necesita supervisión humana; uno que responde a clientes necesita trazabilidad. La tecnología cambia, pero la obligación de rendir cuentas no.",
                    ],
                },
            ],
            "brief": [
                "Preentrenamiento aprende el idioma; SFT aprende la tarea; las preferencias ajustan el estilo",
                "Un modelo base no es lo mismo que un asistente instruido",
                "Más parámetros no garantizan mejor resultado en tu problema",
                "Abierto y propietario son decisiones de coste, control y privacidad",
            ],
            "keys": [
                "Distingue qué capacidad aporta cada fase del entrenamiento.",
                "Evalúa el modelo en tus casos antes de diseñar alrededor de él.",
                "Calcula coste por tarea, no solo precio por token.",
                "Documenta datos enviados, retención y revisión humana.",
                "Elige abierto o propietario según restricciones reales del producto.",
            ],
            "example": "Una clínica quiere resumir notas de consulta. Un modelo abierto cuantizado permite mantener los datos dentro de su servidor, pero requiere hardware y validación clínica. Una API externa ofrece mejor calidad y menos mantenimiento, pero obliga a revisar el contrato de datos. El equipo prueba ambos con cincuenta notas anonimizadas y decide con evidencia, no con reputación.",
            "caution": "Un buen resultado en una demostración no garantiza un producto fiable. Los modelos cambian, las entradas reales son más sucias y los casos límite aparecen después. Sin un conjunto de evaluación propio, el equipo descubre los fallos con los usuarios.",
            "search": "entrenamiento LLM preentrenamiento ajuste supervisado SFT preferencias RLHF DPO modelo base parámetros escala modelos abiertos API responsabilidad evaluación",
        },
    ],
    "quiz": {
        "id": "hllm1q",
        "title": "Cierre del módulo 01",
        "summary": [
            "Representar texto como vectores densos permitió capturar similitud semántica más allá de las palabras exactas.",
            "La atención conecta cualquier par de posiciones y sustituyó el cuello de botella de las redes recurrentes.",
            "Encoder, decoder y encoder-decoder se especializan en comprender, generar o transformar.",
            "Preentrenamiento, ajuste supervisado y preferencias producen capacidades distintas y un modelo base no es un asistente.",
        ],
        "questions": [
            {
                "q": "¿Cuál es la limitación principal de bag-of-words para comparar dos frases?",
                "options": [
                    "Necesita una GPU para funcionar",
                    "Ignora el orden y no reconoce sinónimos ni contexto",
                    "Solo admite textos en inglés",
                    "No puede representar más de diez palabras",
                ],
                "answer": 1,
                "why": "El recuento trata cada término como una dimensión aislada. Dos frases con las mismas palabras en distinto orden, o con sinónimos, pueden quedar idénticas o completamente separadas.",
            },
            {
                "q": "En la auto-atención, ¿qué papel cumple la consulta de un token?",
                "options": [
                    "Almacenar el texto original sin transformarlo",
                    "Expresar qué información busca esa posición para compararla con las claves",
                    "Normalizar la salida final del modelo",
                    "Impedir que el modelo mire hacia el futuro",
                ],
                "answer": 1,
                "why": "La consulta se compara con las claves de las demás posiciones. Esa comparación produce los pesos que deciden cuánto valor de cada posición se incorpora.",
            },
            {
                "q": "¿Qué diferencia a un modelo decoder-only de un encoder-only?",
                "options": [
                    "El decoder usa una máscara causal y genera token a token; el encoder ve toda la entrada",
                    "El encoder no utiliza atención",
                    "El decoder no se puede entrenar con texto",
                    "El encoder solo sirve para traducir",
                ],
                "answer": 0,
                "why": "La máscara causal impide mirar el futuro y hace posible la generación autorregresiva. El encoder, sin esa máscara, construye representaciones bidireccionales útiles para comprender.",
            },
            {
                "q": "¿Qué fase enseña a un modelo a responder como asistente siguiendo instrucciones?",
                "options": [
                    "El preentrenamiento con texto de internet",
                    "El ajuste supervisado con pares de instrucción y respuesta",
                    "La cuantización de los pesos",
                    "El aumento de la ventana de contexto",
                ],
                "answer": 1,
                "why": "El preentrenamiento aprende el idioma, pero el formato de asistente se aprende en el ajuste supervisado y se pule con preferencias. La cuantización solo cambia la precisión numérica.",
            },
        ],
        "exercises": [
            "Toma tres frases de tu dominio y explica qué capturaría bag-of-words y qué se perdería frente a un embedding.",
            "Dibuja el flujo consulta-clave-valor para una frase de seis tokens e indica qué posición miraría un pronombre.",
            "Elige una tarea real y decide si necesitas un encoder, un decoder o un encoder-decoder; justifica la elección.",
        ],
        "search": "cierre representación embeddings atención transformer familias de modelos entrenamiento preentrenamiento SFT preferencias modelos abiertos evaluación",
    },
}
