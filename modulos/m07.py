MODULE = {
    "num": "07",
    "title": "Adaptar y ampliar el modelo",
    "sub": "Fine-tuning, multimodalidad y sistemas en producción",
    "lessons": [
        {
            "id": "hllm7l1",
            "lnum": 1,
            "title": "Fine-tuning de modelos de representación",
            "minutes": 9,
            "lead": "Ajustar un encoder preentrenado es una de las formas más eficientes de obtener un buen clasificador con datos moderados. En lugar de aprender el idioma desde cero, el modelo parte de representaciones ricas y solo adapta una parte a la tarea. La clave está en elegir qué congelar, cuánto entrenar y cómo evitar memorizar el conjunto pequeño.",
            "diagram": ("flow", ["BERT", "Cabeza", "Ajuste", "Etiqueta"]),
            "caption": "El encoder aporta representaciones; una cabeza de clasificación aprende la tarea y se ajusta con una tasa de aprendizaje pequeña.",
            "sections": [
                {
                    "h": "Ajustar con cabeza de clasificación",
                    "p": [
                        "En un modelo encoder, la representación del token especial de clasificación resume la entrada. Sobre ella se coloca una capa densa con una salida por clase. Durante el ajuste, esa cabeza y parte del encoder se actualizan con el objetivo de clasificación. El modelo deja de optimizar enmascaramiento y empieza a separar tus categorías.",
                        "La tasa de aprendizaje suele ser mucho menor que en el preentrenamiento. Un valor alto destruye representaciones útiles; uno demasiado bajo apenas adapta. Pocas épocas suelen bastar, porque el dataset es pequeño y el modelo ya sabe leer. El sobreajuste aparece rápido: la pérdida de entrenamiento baja mientras la validación empeora.",
                        "Congelar las primeras capas reduce cómputo y protege rasgos generales; ajustar las últimas permite especialización. La decisión depende del tamaño de los datos y de la distancia entre el dominio del modelo y el tuyo. Con miles de ejemplos, ajustar todo suele funcionar; con cientos, conviene probar variantes más conservadoras.",
                    ],
                },
                {
                    "h": "Pocos ejemplos con SetFit",
                    "p": [
                        "SetFit ataca el problema de aprender con muy pocas etiquetas. Primero genera pares de textos de la misma clase y de clases distintas, y ajusta un modelo de frase con aprendizaje contrastivo. Después entrena un clasificador simple sobre los embeddings resultantes. La tarea supervisada se convierte en una señal de similitud.",
                        "La ventaja es que el encoder se adapta al dominio con ejemplos limitados, sin necesitar millones de pares. El clasificador final es ligero y rápido. En muchos problemas de pocas clases, ocho o dieciséis ejemplos por clase producen resultados competitivos frente a un ajuste completo más costoso.",
                        "El reconocimiento de entidades sigue otra formulación: cada token recibe una etiqueta y el modelo debe alinear los subtokens con las palabras originales. La precisión depende de una guía de anotación clara y de cubrir límites de entidad. Un fallo típico es etiquetar solo los casos fáciles y dejar fuera las entidades anidadas o ambiguas.",
                    ],
                },
                {
                    "h": "Dominio, evaluación y despliegue",
                    "p": [
                        "El preentrenamiento continuado con enmascaramiento adapta el vocabulario y el estilo al dominio. Se ocultan tokens del corpus propio y el modelo aprende a reconstruirlos. Es útil con jerga técnica, informes o idiomas poco representados, pero consume recursos y puede degradar capacidades generales si se abusa.",
                        "La evaluación debe parecerse al uso. Un F1 alto en un conjunto limpio puede caer con textos reales, desequilibrio o errores de formato. Analiza por clase, por longitud y por fuente. Guarda un conjunto de prueba reservado y no lo uses para elegir hiperparámetros; de lo contrario, la métrica final está contaminada.",
                        "En producción, el modelo ajustado es solo una parte. Hay que versionar pesos, tokenizador y umbral; monitorizar la distribución de entradas; y planificar la actualización. Un clasificador congelado durante años se degrada aunque el código no cambie. La deriva del lenguaje es silenciosa y constante.",
                    ],
                },
            ],
            "brief": [
                "El ajuste de encoder reutiliza representaciones y entrena una cabeza",
                "Pocas épocas y tasa baja evitan destruir conocimiento previo",
                "SetFit convierte pocos ejemplos en pares contrastivos",
                "El dominio y la deriva exigen evaluación y actualización continuas",
            ],
            "keys": [
                "Empieza con pocas épocas y validación temprana.",
                "Prueba congelar capas antes de ajustar todo el modelo.",
                "Usa SetFit cuando tengas pocos ejemplos por clase.",
                "Adapta el vocabulario con preentrenamiento continuado si la jerga es muy distinta.",
                "Versiona pesos, tokenizador y umbral juntos.",
            ],
            "example": "Un hospital quiere detectar urgencias en notas de triaje con 200 ejemplos. Un ajuste completo sobreajusta. SetFit con doce ejemplos por clase y un encoder clínico alcanza un recall alto en la clase crítica, y el equipo elige el umbral para derivar más casos a revisión.",
            "caution": "Un F1 alto en validación no garantiza utilidad clínica. Si la clase grave es rara, el umbral debe elegirse con el coste de cada falso negativo, no con la media global.",
            "search": "fine-tuning encoder BERT clasificación cabeza congelar capas SetFit few-shot NER preentrenamiento continuado MLM sobreajuste evaluación",
        },
        {
            "id": "hllm7l2",
            "lnum": 2,
            "title": "Fine-tuning generativo y eficiente",
            "minutes": 10,
            "lead": "Ajustar un modelo generativo ya no exige actualizar todos sus parámetros. Las técnicas de ajuste eficiente entrenan una fracción pequeña y obtienen resultados cercanos al ajuste completo con una memoria mucho menor. Aun así, el dato y la evaluación siguen siendo el cuello de botella: sin ejemplos de calidad, el método más barato produce un modelo peor.",
            "diagram": ("stack", ["Modelo base congelado", "Adaptadores LoRA", "Cabeza de salida", "Modelo ajustado"]),
            "caption": "LoRA inserta matrices pequeñas junto a las proyecciones del modelo base; solo esas matrices se entrenan y después pueden fusionarse.",
            "sections": [
                {
                    "h": "Qué ajustar y cuándo",
                    "p": [
                        "El ajuste supervisado enseña formato, estilo y comportamiento con pares de instrucción y respuesta. No es la primera opción para añadir hechos: para eso suele ser mejor RAG, que actualiza el conocimiento sin reentrenar. El ajuste brilla cuando necesitas consistencia de formato, tono, herramientas o razonamiento específico del dominio.",
                        "El ajuste completo actualiza todos los pesos. Da máxima flexibilidad y exige mucha memoria, datos y disciplina para no degradar el modelo. Las técnicas PEFT congelan el modelo base e insertan o seleccionan un pequeño conjunto de parámetros entrenables. El resultado se guarda como un adaptador ligero y se puede intercambiar por tarea.",
                        "La calidad del dataset manda. Un millar de ejemplos cuidados, diversos y correctos supera a cien mil conversaciones ruidosas. Hay que definir el formato, cubrir los casos límite, evitar filtraciones y separar evaluación. Un modelo ajustado con respuestas mediocres aprende a ser mediocre con más confianza.",
                    ],
                },
                {
                    "h": "LoRA y QLoRA en la práctica",
                    "p": [
                        "LoRA descompone la actualización de una matriz grande en dos matrices de bajo rango. Si la matriz original tiene miles de filas y columnas, el adaptador usa una dimensión intermedia pequeña. Eso reduce los parámetros entrenables y la memoria de optimización, sin cambiar la arquitectura en inferencia si se fusionan los pesos.",
                        "El rango controla la capacidad del adaptador; el alpha, la escala de la actualización. Los módulos objetivo suelen incluir las proyecciones de atención y, a veces, las del feed-forward. Más módulos y más rango no siempre mejoran: aumentan coste y riesgo de sobreajuste. Se eligen con un conjunto de validación y una tarea concreta.",
                        "QLoRA cuantiza el modelo base a 4 bits, normalmente con un formato que reparte la precisión, y entrena adaptadores LoRA sobre esa versión. Así un modelo grande cabe en una GPU menor. La cuantización introduce una pequeña pérdida de calidad, que se compensa parcialmente al entrenar en mayor precisión los adaptadores. La evaluación sigue siendo obligatoria.",
                    ],
                },
                {
                    "h": "Evaluar, alinear y desplegar",
                    "p": [
                        "Los benchmarks generales no bastan. Necesitas un conjunto propio con preguntas, respuestas de referencia y criterios de aceptación. Compara el modelo ajustado con el base y con un prompt bien diseñado. Si el ajuste no supera a las alternativas en tu tarea, no justifica su complejidad operativa.",
                        "La alineación con preferencias busca que el modelo elija respuestas más útiles y seguras. RLHF entrena una recompensa a partir de comparaciones humanas y optimiza contra ella; DPO aprende directamente de pares preferido-rechazado. Ambos requieren datos de calidad y cuidado con los atajos: un juez o una recompensa imperfecta puede premiar respuestas largas o aduladoras.",
                        "El despliegue incluye versionar el adaptador, medir latencia y memoria, y vigilar el olvido catastrófico. Un ajuste agresivo puede mejorar una tarea y empeorar capacidades generales. Prueba conversaciones fuera de distribución, entradas hostiles y tareas antiguas. Mantén la posibilidad de revertir al modelo anterior sin reentrenar.",
                    ],
                },
            ],
            "brief": [
                "El ajuste enseña comportamiento; RAG aporta conocimiento actualizado",
                "PEFT entrena una fracción pequeña y guarda adaptadores",
                "LoRA reduce parámetros; QLoRA reduce además la memoria con cuantización",
                "La evaluación propia decide si el ajuste compensa",
            ],
            "keys": [
                "Prueba primero prompting y RAG antes de ajustar.",
                "Cuida la diversidad y corrección del dataset.",
                "Elige rango y módulos con validación, no por receta.",
                "Compara el modelo ajustado contra el base en tu tarea.",
                "Vigila el olvido y mantén una ruta de reversión.",
            ],
            "example": "Un bufete quiere respuestas con su formato de citas. Ajusta un adaptador LoRA con 3.000 ejemplos revisados y evalúa contra el mismo modelo con un prompt detallado. El adaptador mejora el formato y la consistencia, pero no añade jurisprudencia nueva; para eso mantienen RAG sobre su base documental.",
            "caution": "Un adaptador entrenado con datos generados por el propio modelo puede amplificar sus errores. Revisa y mezcla datos humanos antes de usarlo como verdad.",
            "search": "fine-tuning generativo SFT PEFT LoRA QLoRA cuantización adaptadores alineación RLHF DPO evaluación sobreajuste despliegue",
        },
        {
            "id": "hllm7l3",
            "lnum": 3,
            "title": "Multimodalidad y sistemas en producción",
            "minutes": 10,
            "lead": "Los modelos multimodales conectan texto con imágenes y permiten describir, buscar, clasificar y conversar sobre contenido visual. Además, una aplicación real rara vez es una sola llamada: combina modelos, herramientas, memoria y controles. La diferencia entre una demo y un producto está en la evaluación, el coste y la seguridad de ese sistema.",
            "diagram": ("flow", ["Imagen", "Encoder visual", "LLM", "Respuesta"]),
            "caption": "Un encoder convierte la imagen en representaciones que el modelo de lenguaje puede usar junto con el texto para responder.",
            "sections": [
                {
                    "h": "Un espacio común para imagen y texto",
                    "p": [
                        "CLIP entrena dos encoders, uno de imagen y otro de texto, para que las parejas correctas queden cerca en un espacio compartido. Con millones de pares aprende a alinear «un perro en la nieve» con la imagen correspondiente. Esa alineación permite clasificar imágenes comparándolas con descripciones de clase sin entrenar una cabeza nueva.",
                        "El enfoque zero-shot es útil cuando las categorías cambian o hay pocos datos. También habilita búsqueda visual y filtrado. Sus límites aparecen en relaciones espaciales, texto dentro de la imagen, detalles finos y conceptos poco representados. La descripción de las clases importa: pequeñas variaciones cambian el resultado.",
                        "Los embeddings multimodales se usan para recuperar imágenes, moderar contenido y recomendar. Como en texto, la evaluación debe hacerse con el dominio real. Un modelo que funciona con fotos de producto puede fallar con radiografías o capturas de pantalla. La similitud aprendida no es universal.",
                    ],
                },
                {
                    "h": "Generar sobre imágenes",
                    "p": [
                        "BLIP-2 conecta un encoder visual congelado con un modelo de lenguaje mediante un módulo ligero que extrae un pequeño conjunto de representaciones. Esas representaciones se proyectan al espacio del texto y actúan como contexto visual. El modelo de lenguaje puede así describir o responder preguntas sin haber sido entrenado desde cero para ver.",
                        "Los modelos visión-lenguaje actuales siguen una idea similar: convertir la imagen en tokens o vectores que el Transformer puede atender junto con las palabras. Se entrenan con pares imagen-texto, instrucciones y datos de conversación. El resultado es flexible, pero hereda los fallos del reconocimiento visual y la tendencia a inventar detalles.",
                        "Los casos de uso incluyen descripción automática, preguntas sobre documentos escaneados, extracción de campos y asistencia en tiempo real. Antes de confiar, hay que probar imágenes borrosas, giradas, con texto pequeño y con elementos engañosos. La calidad del OCR y de la resolución suele importar más que el tamaño del modelo.",
                    ],
                },
                {
                    "h": "El sistema completo",
                    "p": [
                        "Una aplicación de LLM se compone de capas: interfaz, orquestación, modelo, herramientas, memoria y observabilidad. Frameworks como LangChain ayudan a encadenar prompts, recuperadores y acciones, pero no sustituyen el diseño. La lógica crítica debe ser explícita y testeable, no una cadena opaca de llamadas.",
                        "Los agentes añaden la capacidad de decidir acciones: buscar, ejecutar código, consultar una API. Esa autonomía exige límites. Define qué herramientas existen, con qué permisos, cuántos pasos puede dar y cómo se registra cada acción. Un agente sin presupuesto ni validación puede gastar dinero, filtrar datos o repetir errores en bucle.",
                        "El coste y la latencia se gestionan con caché, modelos más pequeños para tareas simples, procesamiento por lotes y límites de contexto. La seguridad incluye filtrar entradas, proteger secretos, aislar herramientas y revisar resultados sensibles. La evaluación debe cubrir el sistema completo, no solo el modelo. Un buen componente no garantiza un buen producto.",
                    ],
                },
            ],
            "brief": [
                "CLIP alinea imagen y texto en un espacio común para clasificar y buscar",
                "BLIP-2 y los VLM conectan un encoder visual con un modelo de lenguaje",
                "Los agentes añaden acciones y necesitan permisos y límites estrictos",
                "La producción exige evaluar el sistema, no solo el modelo",
            ],
            "keys": [
                "Prueba el modelo visual con imágenes reales y degradadas.",
                "Describe las clases con cuidado en clasificación zero-shot.",
                "Conecta visión y lenguaje mediante representaciones, no con reglas frágiles.",
                "Limita herramientas, pasos y permisos de cualquier agente.",
                "Mide coste, latencia y seguridad extremo a extremo.",
            ],
            "example": "Una aseguradora usa un VLM para extraer datos de partes de accidente. El modelo acierta en fotos nítidas, pero falla con documentos girados. El equipo añade detección de orientación y OCR, y deriva a revisión los campos con baja confianza. La precisión sube sin cambiar el modelo.",
            "caution": "Un agente con acceso a herramientas puede ejecutar una acción irreversible antes de que nadie revise. Los permisos de solo lectura y la confirmación humana no son opcionales en operaciones sensibles.",
            "search": "multimodal CLIP BLIP-2 visión lenguaje VLM embeddings imagen agentes LangChain herramientas orquestación producción coste seguridad evaluación",
        },
    ],
    "quiz": {
        "id": "hllm7q",
        "title": "Cierre del módulo 07",
        "summary": [
            "El ajuste de encoders reutiliza conocimiento y requiere cuidar épocas, capas y umbrales.",
            "SetFit y el preentrenamiento continuado ayudan cuando hay pocos datos o mucho dominio.",
            "LoRA y QLoRA reducen el coste del ajuste generativo, pero no sustituyen un buen dataset.",
            "La multimodalidad y los agentes amplían capacidades y multiplican los puntos de control.",
        ],
        "questions": [
            {
                "q": "¿Qué hace SetFit para clasificar con pocos ejemplos?",
                "options": [
                    "Genera millones de imágenes sintéticas",
                    "Ajusta un encoder con pares contrastivos y entrena un clasificador simple",
                    "Elimina la necesidad de etiquetas",
                    "Cuantiza el modelo a un bit",
                ],
                "answer": 1,
                "why": "SetFit crea pares de textos de la misma clase y de clases distintas, adapta el encoder y luego entrena una cabeza ligera sobre los embeddings resultantes.",
            },
            {
                "q": "¿Qué ventaja principal ofrece LoRA frente al ajuste completo?",
                "options": [
                    "Entrena muchos menos parámetros y ahorra memoria",
                    "Garantiza que el modelo no alucine",
                    "Elimina la necesidad de datos",
                    "Duplica el tamaño del vocabulario",
                ],
                "answer": 0,
                "why": "LoRA congela el modelo base y entrena matrices de bajo rango. El adaptador es pequeño, se puede intercambiar y se fusiona para inferencia.",
            },
            {
                "q": "¿Para qué sirve CLIP en un sistema multimodal?",
                "options": [
                    "Para generar audio a partir de texto",
                    "Para alinear imágenes y descripciones en un espacio vectorial común",
                    "Para comprimir el PDF de entrada",
                    "Para entrenar un tokenizador de código",
                ],
                "answer": 1,
                "why": "CLIP aprende encoders de imagen y texto que colocan las parejas correctas cerca. Eso permite clasificación zero-shot, búsqueda visual y filtrado.",
            },
            {
                "q": "¿Qué control es imprescindible en un agente con herramientas?",
                "options": [
                    "Permitir cualquier acción para que sea autónomo",
                    "Limitar herramientas, permisos y número de pasos, y registrar las acciones",
                    "Ocultar los errores al usuario",
                    "Desactivar la evaluación para ahorrar coste",
                ],
                "answer": 1,
                "why": "La autonomía sin límites puede causar acciones irreversibles o fugas de datos. Los permisos mínimos, el presupuesto de pasos y el registro permiten operar y auditar.",
            },
        ],
        "exercises": [
            "Diseña un experimento de ajuste con 300 ejemplos y otro con un prompt few-shot; define cómo compararás ambos.",
            "Calcula cuántos parámetros entrena un adaptador LoRA para una matriz de 4096×4096 con rango 8.",
            "Elige una tarea visual de tu dominio y escribe cinco casos límite que incluirías en la evaluación.",
        ],
        "search": "cierre fine-tuning encoder SetFit LoRA QLoRA alineación DPO multimodal CLIP BLIP-2 agentes producción evaluación",
    },
}
