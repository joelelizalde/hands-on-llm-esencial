MODULE = {
    "num": "05",
    "title": "Prompt engineering",
    "sub": "Diseñar instrucciones que funcionan",
    "lessons": [
        {
            "id": "hllm5l1",
            "lnum": 1,
            "title": "Los ingredientes de un buen prompt",
            "minutes": 9,
            "lead": "Un prompt no es una frase mágica: es una especificación en lenguaje natural. Cuanto más claro sea el papel que debe adoptar el modelo, la tarea, el contexto, las restricciones y el formato de salida, menos espacio queda para la interpretación. La mayoría de los malos resultados empiezan en una instrucción ambigua.",
            "diagram": ("stack", ["Rol", "Tarea", "Contexto", "Formato"]),
            "caption": "Un prompt completo se construye por capas: quién responde, qué debe hacer, con qué información y en qué formato.",
            "sections": [
                {
                    "h": "Anatomía de una instrucción",
                    "p": [
                        "El papel orienta el tono y el nivel de detalle: «actúa como revisor de contratos» no añade conocimiento, pero selecciona registros aprendidos. La tarea debe ser un verbo concreto: resumir, extraer, comparar, clasificar. «Habla sobre este texto» deja al modelo elegir entre decenas de objetivos posibles.",
                        "El contexto aporta los datos que el modelo no puede inventar: el documento, la política, el historial o los ejemplos. Delimitarlo con marcas claras evita que se confunda con la instrucción. Si el texto del usuario puede contener órdenes, hay que separarlo explícitamente y decir que se trata de material a analizar, no de instrucciones a obedecer.",
                        "Las restricciones definen el espacio de respuestas: longitud, idioma, tono, fuentes permitidas, qué hacer si falta información. El formato cierra la especificación: lista, tabla, JSON con campos concretos o párrafo. Cuanto más se parece el prompt a un contrato verificable, más fácil es comprobar si el modelo lo cumplió.",
                    ],
                },
                {
                    "h": "Controlar la salida",
                    "p": [
                        "El formato se refuerza con ejemplos y con validación posterior. Pedir JSON no garantiza JSON válido; conviene definir el esquema, mostrar un ejemplo mínimo y comprobar el resultado con un parser. Si el proveedor permite esquemas o funciones, úsalos: eliminan la ambigüedad mejor que cualquier súplica en el prompt.",
                        "La longitud se controla con instrucciones y con límites de tokens, pero ambos pueden recortar una respuesta a medias. Para resúmenes, indica qué debe conservarse y qué puede omitirse. Para respuestas breves, pide primero la conclusión y después, si hace falta, la justificación. Un límite sin criterio produce texto truncado, no concisión.",
                        "Las instrucciones contradictorias son una fuente común de fallos: «sé breve» y «explica cada detalle» a la vez, o «usa solo el contexto» y «responde con conocimiento general». El modelo resolverá el conflicto de forma impredecible. Ordena las prioridades y elimina lo que no sea necesario; un prompt más corto y coherente suele ganar.",
                    ],
                },
                {
                    "h": "Tratar el prompt como código",
                    "p": [
                        "Un prompt en producción necesita versión, responsable y historial de cambios. Un pequeño ajuste de redacción puede mejorar un caso y romper diez. Guarda el texto junto al conjunto de evaluación y ejecuta las pruebas antes de desplegar. Sin esa disciplina, nadie sabe qué prompt produjo qué comportamiento.",
                        "El conjunto de evaluación debe representar las entradas reales, incluidas las sucias: vacías, muy largas, con errores, en varios idiomas o con intentos de manipulación. Compara versiones con métricas concretas y revisa muestras. La mejora media puede ocultar un empeoramiento grave en un segmento pequeño pero importante.",
                        "La documentación también protege frente a la inyección de prompts. Si el sistema lee páginas web o correos, cualquiera puede incluir instrucciones hostiles. Separa datos de instrucciones, limita las herramientas disponibles y valida las acciones antes de ejecutarlas. El prompt no es una frontera de seguridad.",
                    ],
                },
            ],
            "brief": [
                "Rol, tarea, contexto, restricciones y formato forman la especificación",
                "Delimitar el material evita confundirlo con instrucciones",
                "Pedir un formato no basta: hay que validarlo",
                "Los prompts se versionan y se prueban como cualquier código",
            ],
            "keys": [
                "Empieza por un verbo de tarea inequívoco.",
                "Delimita claramente los datos que el modelo debe analizar.",
                "Define el formato y valídalo con un parser.",
                "Elimina instrucciones que compitan entre sí.",
                "Versiona el prompt y prueba regresiones antes de cambiar.",
            ],
            "example": "Un equipo pide «resume esta reunión» y recibe actas de distinta longitud y formato. Reescribe el prompt: papel de secretario, tarea de extraer decisiones y acciones, contexto del acta, formato de tres secciones y regla de escribir «sin decisiones» cuando corresponda. Las variaciones caen y la revisión humana se vuelve rápida.",
            "caution": "Añadir «por favor, sé preciso» no mejora la precisión. Sin criterios concretos sobre qué es correcto, el modelo solo puede adivinar qué significa la petición.",
            "search": "prompt engineering ingredientes rol tarea contexto restricciones formato control salida JSON delimitadores versionado evaluación inyección",
        },
        {
            "id": "hllm5l2",
            "lnum": 2,
            "title": "Aprender del contexto",
            "minutes": 9,
            "lead": "Los modelos pueden resolver una tarea nueva sin actualizar sus pesos si reciben ejemplos adecuados en el prompt. Esa capacidad, el aprendizaje en contexto, es potente y frágil: depende de qué ejemplos eliges, en qué orden los pones y de si la tarea cabe realmente en una demostración. Descomponer el problema suele ser más fiable que un mega-prompt.",
            "diagram": ("loop", ["Instrucción", "Ejemplos", "Salida", "Revisión"]),
            "caption": "El ciclo del aprendizaje en contexto: la instrucción y los ejemplos producen una salida que se revisa y se usa para ajustar el siguiente prompt.",
            "sections": [
                {
                    "h": "Zero-shot, one-shot y few-shot",
                    "p": [
                        "En zero-shot solo se describe la tarea. Funciona bien con modelos instruidos y tareas comunes, pero deja margen a interpretaciones. En one-shot se añade un ejemplo completo de entrada y salida. En few-shot se incluyen varios, lo que muestra el formato, el nivel de detalle y los casos límite que se esperan.",
                        "Los ejemplos son datos de entrenamiento temporales. Deben ser correctos, representativos y estar balanceados entre clases. Si todos los positivos son largos y los negativos cortos, el modelo puede aprender esa correlación espuria. Incluye casos difíciles y, si es posible, ejemplos donde la respuesta correcta es «no se puede determinar».",
                        "El orden importa. Los modelos pueden favorecer la última etiqueta que vieron o repetir el patrón del ejemplo final. Baraja los ejemplos, comprueba la estabilidad y no confíes en un prompt que solo funciona con una disposición concreta. Si el rendimiento cambia mucho al reordenar, la tarea no está bien especificada.",
                    ],
                },
                {
                    "h": "Descomponer en vez de acumular",
                    "p": [
                        "Un prompt que pide extraer, clasificar, resumir y redactar en una sola pasada suele producir un resultado mediocre en varias partes. La cadena de prompts divide el trabajo: primero se extraen datos, luego se validan y después se redacta con esos datos. Cada paso tiene una entrada y una salida comprobables.",
                        "La descomposición también permite usar herramientas distintas. Un paso puede ser una búsqueda, otro una llamada a un modelo pequeño y otro una regla determinista. El resultado es más fácil de depurar porque se sabe dónde falló. Un pipeline de tres pasos simples suele superar a un prompt heroico imposible de mantener.",
                        "El coste es mayor: más llamadas, más latencia y más superficie de error. Compensa cuando la precisión importa o cuando hay validaciones intermedias. Para una tarea corta y bien definida, un solo prompt puede ser suficiente. La decisión se toma midiendo, no por preferencia estética.",
                    ],
                },
                {
                    "h": "Conversación, memoria y límites",
                    "p": [
                        "En un chat, el prompt del sistema fija el comportamiento y las reglas; los turnos del usuario y del asistente aportan el historial. Ese historial crece y consume contexto. Resumir turnos antiguos o conservar solo los datos relevantes mantiene la coherencia sin arrastrar ruido. La memoria no es gratuita.",
                        "El contexto recuperado compite con la conversación. Si insertas documentos, indica de dónde vienen y cómo debe usarlos el modelo. Un texto recuperado puede contener instrucciones maliciosas; el sistema debe tratar todo contenido externo como datos no confiables. La separación entre instrucción y material es una medida de seguridad, no solo de estilo.",
                        "Cuando la información es insuficiente, el prompt debe permitir decir «no lo sé». Los modelos tienden a completar huecos con plausibilidad. Una regla explícita de abstención, junto con la petición de citar la fuente, reduce alucinaciones y facilita la revisión. Es mejor una respuesta incompleta y honesta que una invención elegante.",
                    ],
                },
            ],
            "brief": [
                "Few-shot muestra formato y criterio, no solo la tarea",
                "Ejemplos desequilibrados enseñan correlaciones falsas",
                "Descomponer la tarea facilita validar y depurar cada paso",
                "El historial y el contexto externo consumen presupuesto y riesgo",
            ],
            "keys": [
                "Elige ejemplos representativos y balanceados entre clases.",
                "Baraja el orden para comprobar la estabilidad del resultado.",
                "Divide tareas complejas en pasos con salidas verificables.",
                "Resume el historial en lugar de acumularlo sin límite.",
                "Permite la abstención cuando falte información.",
            ],
            "example": "Un clasificador de correos confunde solicitudes de baja con quejas. El equipo añade tres ejemplos fronterizos de cada clase y una regla para citar la frase que justifica la etiqueta. El F1 de la clase minoritaria sube y los revisores pueden comprobar la evidencia en segundos.",
            "caution": "Un ejemplo con un error enseña ese error. Revisar los ejemplos del prompt es tan importante como revisar el código que los inserta.",
            "search": "few-shot zero-shot one-shot ejemplos en contexto orden etiquetas cadena de prompts descomposición historial memoria abstención seguridad",
        },
        {
            "id": "hllm5l3",
            "lnum": 3,
            "title": "Razonar y verificar",
            "minutes": 10,
            "lead": "Pedir al modelo que explique sus pasos puede mejorar tareas de lógica y matemáticas, pero también produce explicaciones convincentes que no reflejan el cálculo real. La técnica útil no es confiar más en el texto, sino combinarlo con muestras, herramientas y validaciones externas que permitan comprobar el resultado.",
            "diagram": ("flow", ["Pregunta", "Razonamiento", "Verificación", "Respuesta"]),
            "caption": "El razonamiento intermedio solo aporta valor si la respuesta final se contrasta con una validación o una herramienta.",
            "sections": [
                {
                    "h": "Cadena de pensamiento",
                    "p": [
                        "La cadena de pensamiento pide al modelo que escriba pasos intermedios antes de la respuesta. En problemas de varias etapas, esos pasos actúan como espacio de trabajo y suelen mejorar el acierto. También hacen visible dónde se torció el razonamiento, lo que ayuda a depurar el prompt o el dato de entrada.",
                        "No siempre conviene. En tareas simples añade latencia y tokens sin mejorar; en modelos que ya razonan internamente, pedir pasos puede duplicar el trabajo. Y en aplicaciones sensibles, mostrar el razonamiento puede filtrar información o dar una falsa sensación de auditoría. La explicación es una narración, no una traza verificada.",
                        "La fidelidad es el punto delicado. Un modelo puede llegar a la respuesta correcta por una ruta equivocada o justificar una respuesta errónea con pasos plausibles. Por eso la cadena de pensamiento se usa para explorar, no como prueba. La verificación debe venir de una fuente externa: cálculo, prueba unitaria, consulta a base de datos o revisión humana.",
                    ],
                },
                {
                    "h": "Muestras, árboles y herramientas",
                    "p": [
                        "Self-consistency genera varios razonamientos con muestreo y elige la respuesta que más se repite. La intuición es estadística: si distintos caminos convergen, la respuesta tiene más apoyo. Cuesta varias veces más y solo tiene sentido cuando existe una respuesta final discreta que se pueda comparar.",
                        "El árbol de pensamiento explora varias ramas, evalúa parcialmente cada una y profundiza en las prometedoras. Es útil en problemas con decisiones secuenciales y poda, pero requiere un evaluador y un presupuesto de búsqueda. Sin control, se convierte en una explosión de llamadas caras que no garantiza mejor calidad.",
                        "ReAct alterna razonamiento y acción: el modelo decide qué herramienta usar, observa el resultado y continúa. Así puede buscar, calcular o consultar una API en lugar de inventar. El patrón es la base de muchos agentes. Su punto débil es la acumulación de errores y la necesidad de límites estrictos sobre qué acciones puede ejecutar.",
                    ],
                },
                {
                    "h": "Verificar antes de confiar",
                    "p": [
                        "La forma más robusta de controlar la salida es restringirla. Las gramáticas y los esquemas JSON obligan al decodificador a producir estructuras válidas. Los validadores comprueban tipos, rangos y campos obligatorios. Si el resultado no cumple, se reintenta con el error como contexto o se deriva a una persona.",
                        "Para datos factuales, exige citas y comprueba que la cita existe y respalda la afirmación. Para código, ejecuta pruebas. Para matemáticas, usa una calculadora. Para decisiones de negocio, define reglas deterministas que el modelo no pueda saltarse. Cuanto más crítico es el resultado, menos debe depender de la introspección del modelo.",
                        "Los modelos de razonamiento actuales dedican más cómputo a pensar antes de responder y suelen mejorar en problemas complejos. No eliminan la necesidad de evaluar: siguen alucinando, siguen siendo sensibles al enunciado y pueden gastar presupuesto en callejones sin salida. Úsalos donde la tarea lo justifique y mide el coste real por respuesta correcta.",
                    ],
                },
            ],
            "brief": [
                "La cadena de pensamiento ayuda, pero no garantiza fidelidad",
                "Self-consistency y árbol de pensamiento exploran varias rutas",
                "ReAct conecta razonamiento con herramientas y observaciones",
                "Gramáticas, esquemas y pruebas verifican mejor que la confianza",
            ],
            "keys": [
                "Usa razonamiento explícito solo cuando la tarea lo justifique.",
                "No trates la explicación del modelo como una auditoría.",
                "Compara respuestas discretas con varias muestras si el coste lo permite.",
                "Limita las acciones de un agente y valida cada resultado.",
                "Verifica con código, datos o personas según el riesgo.",
            ],
            "example": "Un asistente resuelve problemas de inventario con una calculadora en lugar de hacer aritmética mental. El modelo interpreta la pregunta, extrae cantidades y llama a la herramienta; el resultado se valida contra las reglas de negocio. La precisión sube y el origen de cada número queda registrado.",
            "caution": "Una cadena de pensamiento larga puede impresionar sin ser correcta. Si la respuesta no se contrasta, el sistema solo ha producido una explicación más elaborada de un posible error.",
            "search": "razonamiento cadena de pensamiento chain of thought self-consistency árbol de pensamiento tree of thought ReAct herramientas verificación gramáticas JSON pruebas",
        },
    ],
    "quiz": {
        "id": "hllm5q",
        "title": "Cierre del módulo 05",
        "summary": [
            "Un prompt es una especificación: rol, tarea, contexto, restricciones y formato.",
            "Los ejemplos en contexto enseñan formato y criterio, pero pueden introducir sesgos.",
            "Descomponer una tarea compleja facilita la validación y el diagnóstico.",
            "El razonamiento debe acompañarse de verificación externa cuando la respuesta importa.",
        ],
        "questions": [
            {
                "q": "¿Qué elemento de un prompt define cómo debe estructurarse la respuesta?",
                "options": [
                    "El rol del asistente",
                    "El formato de salida y su validación",
                    "La temperatura del servidor",
                    "El número de parámetros del modelo",
                ],
                "answer": 1,
                "why": "El formato concreta si se espera lista, tabla, JSON o párrafo. Validarlo con un parser o esquema comprueba que el modelo lo cumplió.",
            },
            {
                "q": "¿Por qué puede ser mala idea incluir solo ejemplos fáciles en un prompt few-shot?",
                "options": [
                    "Porque ocupan demasiados tokens",
                    "Porque el modelo no aprende a resolver los casos fronterizos que importan",
                    "Porque el modelo deja de entender el idioma",
                    "Porque impiden usar JSON",
                ],
                "answer": 1,
                "why": "Los ejemplos definen el criterio. Si todos son obvios, el modelo no ve cómo decidir en las situaciones ambiguas donde realmente falla.",
            },
            {
                "q": "¿Cuál es el uso más sólido de la cadena de pensamiento?",
                "options": [
                    "Sustituir la verificación con pruebas",
                    "Explorar pasos intermedios en tareas de varias etapas, contrastando la respuesta final",
                    "Garantizar que el modelo no alucine",
                    "Reducir el coste de cada llamada",
                ],
                "answer": 1,
                "why": "Los pasos ayudan a trabajar problemas complejos, pero la explicación no es una prueba de corrección. La respuesta debe validarse con una fuente independiente.",
            },
            {
                "q": "¿Qué hace ReAct?",
                "options": [
                    "Entrena el modelo desde cero con refuerzo",
                    "Alterna razonamiento, acción sobre una herramienta y observación del resultado",
                    "Comprime el vocabulario del tokenizador",
                    "Convierte texto en imágenes",
                ],
                "answer": 1,
                "why": "ReAct permite que el modelo decida una acción, reciba el resultado y continúe razonando. Es útil para buscar o calcular, siempre con límites y validación.",
            },
        ],
        "exercises": [
            "Reescribe un prompt vago de tu trabajo con rol, tarea, contexto, restricciones y formato; pruébalo con cinco entradas.",
            "Crea un conjunto de seis ejemplos fronterizos para una clasificación y comprueba si el orden altera la salida.",
            "Diseña un flujo con una herramienta externa y una validación para una tarea donde el modelo no deba calcular solo.",
        ],
        "search": "cierre prompt engineering formato few-shot cadena de prompts razonamiento self-consistency ReAct verificación esquemas evaluación",
    },
}
