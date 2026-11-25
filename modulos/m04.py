MODULE = {
    "num": "04",
    "title": "Clasificar y agrupar texto",
    "sub": "Aprovechar modelos ya entrenados sin entrenar de cero",
    "lessons": [
        {
            "id": "hllm4l1",
            "lnum": 1,
            "title": "Clasificación con modelos de representación",
            "minutes": 9,
            "lead": "Asignar etiquetas a texto es una de las tareas más rentables de la IA aplicada: moderar comentarios, priorizar tickets, detectar intención o filtrar correo. No siempre hace falta un modelo generativo. Un encoder bien elegido, con pocos datos y una cabeza de clasificación, suele ser más barato, rápido y fácil de evaluar.",
            "diagram": ("flow", ["Texto", "Embedding", "Clasificador", "Etiqueta"]),
            "caption": "Un encoder convierte el texto en un vector y un clasificador ligero aprende a separar las categorías con datos etiquetados.",
            "sections": [
                {
                    "h": "Tres caminos hacia una etiqueta",
                    "p": [
                        "El primero es usar un modelo ya ajustado para la tarea. Si existe un detector de spam o de sentimiento entrenado con datos parecidos, adaptarlo suele dar resultados sólidos con muy poco esfuerzo. El riesgo es el desajuste de dominio: un modelo entrenado con reseñas de películas puede fallar con informes técnicos.",
                        "El segundo es congelar un encoder y entrenar un clasificador simple sobre sus embeddings. Se calculan los vectores una vez, se guardan y se ajusta una regresión logística o una red pequeña. Es rápido, barato y sorprendentemente competitivo cuando hay cientos o miles de ejemplos. También facilita comparar varios encoders sin reentrenar todo.",
                        "El tercero es zero-shot: describir las etiquetas en lenguaje natural y dejar que un modelo decida. No requiere datos etiquetados, pero es más frágil ante clases ambiguas y depende mucho de cómo se redacten las descripciones. Sirve para arrancar y generar candidatos, no para dar por cerrada una taxonomía.",
                    ],
                },
                {
                    "h": "Datos, etiquetas y evaluación",
                    "p": [
                        "La calidad del clasificador depende más de las etiquetas que del modelo. Una taxonomía con clases solapadas produce desacuerdos que ningún ajuste arregla. Conviene definir cada categoría con ejemplos, decidir qué hacer con los casos mixtos y medir el acuerdo entre anotadores antes de entrenar.",
                        "El desequilibrio es habitual: la clase «normal» suele ser mayoría. La exactitud global puede parecer alta ignorando por completo la clase que importa. Precisión, recall y F1 por clase revelan lo que la media oculta. La matriz de confusión muestra qué confusiones concretas comete el sistema y orienta la siguiente mejora.",
                        "La fuga de datos es otro peligro silencioso. Duplicados entre entrenamiento y prueba, o textos del mismo usuario repartidos en ambos lados, inflan las métricas. Divide por grupos cuando corresponda y mantén un conjunto de prueba que no se toque durante el ajuste. Una métrica honesta vale más que una alta.",
                    ],
                },
                {
                    "h": "Del modelo a la operación",
                    "p": [
                        "Un clasificador devuelve puntuaciones, no certezas. Elegir el umbral es una decisión de producto: en moderación agresiva quizá prefieras revisar de más; en filtrado automático, evitar falsos positivos. La calibración comprueba si un 0,8 significa realmente ochenta por ciento de acierto en tu distribución.",
                        "Los datos cambian. Aparecen jergas, productos nuevos y formas de escribir que el modelo no vio. La vigilancia de la distribución de entradas y de la confianza media detecta la deriva antes de que el usuario se queje. Reentrenar con ejemplos recientes etiquetados es más efectivo que subir el tamaño del modelo.",
                        "La revisión humana sigue siendo necesaria en decisiones sensibles. Un buen diseño muestra al revisor la etiqueta propuesta, la confianza y el texto relevante, y registra la corrección. Esa corrección no es solo control de calidad: es el dato que alimenta la siguiente versión del clasificador.",
                    ],
                },
            ],
            "brief": [
                "Modelo específico, embeddings con clasificador o zero-shot son tres caminos",
                "Las etiquetas claras importan más que la arquitectura",
                "F1 por clase y matriz de confusión superan a la exactitud global",
                "El umbral y la calibración son decisiones de producto",
            ],
            "keys": [
                "Empieza con el modelo más simple que resuelva la tarea.",
                "Escribe una guía de etiquetado y mide el acuerdo entre anotadores.",
                "Separa los datos por grupos para evitar fugas.",
                "Elige el umbral según el coste de cada error.",
                "Vigila la deriva y reutiliza las correcciones humanas.",
            ],
            "example": "Un equipo clasifica tickets en cinco categorías. Con un encoder congelado y regresión logística obtiene un F1 macro de 0,81 usando 1.200 ejemplos. La clase «facturación» falla porque se solapa con «cuenta». Al redefinir la frontera y añadir ejemplos, sube a 0,88 sin cambiar de modelo ni de infraestructura.",
            "caution": "Una exactitud del 95 % puede ser inútil si la clase relevante representa el 2 % y el modelo nunca la predice. Mira siempre la matriz de confusión y las métricas por clase.",
            "search": "clasificación texto modelos de representación encoder embeddings regresión logística zero-shot etiquetas desequilibrio F1 matriz confusión calibración deriva",
        },
        {
            "id": "hllm4l2",
            "lnum": 2,
            "title": "Clasificación con modelos generativos",
            "minutes": 9,
            "lead": "Los modelos de texto a texto pueden clasificar sin una cabeza especializada: se les da una instrucción y se espera una etiqueta. Esa flexibilidad simplifica el prototipado y permite clases nuevas sin reentrenar, pero introduce costes, latencia y formas sutiles de fallar que conviene controlar.",
            "diagram": ("flow", ["Instrucción", "Texto", "Modelo", "Etiqueta"]),
            "caption": "La tarea se formula como una transformación de texto: la instrucción y el documento entran, y el modelo devuelve una etiqueta o una explicación.",
            "sections": [
                {
                    "h": "Clasificar es generar una etiqueta",
                    "p": [
                        "Un modelo texto a texto, como T5, aprende a convertir una entrada en una salida. Para clasificar se le presenta el documento precedido de una instrucción y se entrena o se pide que genere el nombre de la clase. La etiqueta se convierte así en una secuencia más, sin necesidad de una capa nueva.",
                        "Esta formulación unifica tareas: sentimiento, intención, idioma o detección de toxicidad se expresan como instrucciones distintas sobre el mismo modelo. También permite devolver una justificación breve junto a la etiqueta. Esa explicación ayuda a revisar, aunque no debe confundirse con el razonamiento interno real del sistema.",
                        "El vocabulario de salida importa. Si el modelo puede escribir cualquier cosa, también puede inventar una categoría inexistente. Restringir la generación a las etiquetas válidas, comparar la probabilidad de cada una o validar la salida con un esquema reduce esa libertad y hace el sistema más predecible.",
                    ],
                },
                {
                    "h": "Prompts que clasifican bien",
                    "p": [
                        "Una instrucción clara incluye la tarea, la lista cerrada de etiquetas, el criterio para elegir y el formato de salida. Los ejemplos ayudan cuando las clases son sutiles, pero deben cubrir los casos difíciles, no solo los típicos. Un prompt con diez ejemplos fáciles puede ser peor que uno con tres fronterizos.",
                        "El orden de las etiquetas y de los ejemplos influye. Algunos modelos tienden a preferir la primera opción o la última que vieron. Barajar el orden y comprobar la estabilidad de las predicciones es una prueba sencilla que revela sesgos del prompt. Si la etiqueta cambia al reordenar, el sistema no es fiable.",
                        "Para clases ambiguas conviene pedir abstención. Una categoría «no estoy seguro» bien definida evita respuestas inventadas y deriva los casos a revisión. También es útil pedir la etiqueta y una confianza aproximada, sabiendo que esa confianza es una estimación textual y no una probabilidad calibrada.",
                    ],
                },
                {
                    "h": "Cuándo compensa",
                    "p": [
                        "La clasificación generativa brilla cuando hay pocos datos, las clases cambian con frecuencia o se necesita una explicación. También cuando el volumen es bajo y montar un entrenamiento dedicado no se justifica. En esos casos, un prompt bien diseñado puede estar en producción en una tarde.",
                        "Pierde frente a un encoder cuando el volumen es alto, la latencia es crítica o las etiquetas son estables. Pagar por token cada documento y esperar una generación completa es mucho más caro que una pasada por un clasificador pequeño. La solución híbrida es común: el modelo generativo etiqueta una muestra y el clasificador aprende de ella.",
                        "La evaluación debe ser la misma que en cualquier clasificador: conjunto etiquetado, métricas por clase y análisis de errores. Añadir una revisión de formato y de etiquetas inválidas. Un sistema que acierta el 90 % pero devuelve texto libre una de cada diez veces no está listo para automatizar decisiones.",
                    ],
                },
            ],
            "brief": [
                "Texto a texto convierte la clasificación en generación de una etiqueta",
                "Una lista cerrada y un formato estricto reducen invenciones",
                "El orden de ejemplos y etiquetas puede sesgar la predicción",
                "La vía generativa es flexible pero más cara y lenta a escala",
            ],
            "keys": [
                "Restringe la salida a las etiquetas válidas.",
                "Incluye ejemplos fronterizos, no solo casos fáciles.",
                "Prueba la estabilidad barajando el orden del prompt.",
                "Permite abstención en casos ambiguos.",
                "Compara coste y latencia antes de elegir la vía generativa.",
            ],
            "example": "Una redacción quiere etiquetar noticias en diez temas que aún no están definidos. Empieza con un modelo generativo y un prompt con ejemplos fronterizos; revisa 300 resultados y ajusta las definiciones. Cuando la taxonomía se estabiliza, entrena un encoder con esas etiquetas y reduce el coste por artículo.",
            "caution": "Pedir «responde solo con la etiqueta» no garantiza que el modelo obedezca. Sin validación de la salida, una palabra extra puede romper el pipeline que consume la respuesta.",
            "search": "clasificación generativa texto a texto T5 prompt etiquetas few-shot formato validación abstención coste latencia evaluación híbrido",
        },
        {
            "id": "hllm4l3",
            "lnum": 3,
            "title": "Clustering y modelado de temas",
            "minutes": 9,
            "lead": "Cuando no hay etiquetas, agrupar documentos parecidos revela estructura: temas emergentes, quejas recurrentes, segmentos de clientes. El pipeline moderno combina embeddings, reducción de dimensión y agrupamiento por densidad; después hay que nombrar y validar los grupos, que es donde suele estar el verdadero trabajo.",
            "diagram": ("flow", ["Documentos", "Embeddings", "UMAP", "HDBSCAN"]),
            "caption": "Los documentos se convierten en vectores, se reducen a pocas dimensiones y se agrupan por densidad; después se extraen las palabras que definen cada grupo.",
            "sections": [
                {
                    "h": "Un pipeline, no un algoritmo",
                    "p": [
                        "El primer paso es convertir cada documento en un embedding. La calidad de estos vectores determina lo que el agrupamiento puede descubrir. Un modelo entrenado en otro idioma o en otro tipo de texto mezclará cosas que para el negocio son distintas, y ninguna técnica posterior lo arreglará del todo.",
                        "El segundo paso reduce la dimensionalidad. Los embeddings tienen cientos de dimensiones y muchas son redundantes; UMAP conserva la estructura local y facilita que los algoritmos de densidad encuentren grupos. No es una simple visualización: la elección de vecinos y componentes cambia el resultado y debe probarse.",
                        "El tercer paso agrupa. HDBSCAN descubre grupos de densidad variable, no exige fijar el número de clústeres y marca como ruido los puntos aislados. Esa tolerancia al ruido es valiosa en texto real, donde siempre hay casos raros. k-means, en cambio, obliga a asignar todos los puntos y presupone grupos esféricos.",
                    ],
                },
                {
                    "h": "BERTopic y las palabras que explican",
                    "p": [
                        "BERTopic organiza el pipeline en bloques intercambiables: embedding, reducción, agrupamiento y representación. Su aportación práctica es el último bloque. Para cada grupo calcula la importancia de las palabras frente al resto del corpus, una variante de TF-IDF aplicada a los documentos del clúster.",
                        "Ese cálculo, llamado c-TF-IDF, produce etiquetas legibles sin necesidad de generar texto. Un grupo puede describirse como «factura, cobro, recibo, duplicado». La persona que interpreta decide si eso es «problemas de facturación» o «solicitudes de reembolso». El algoritmo propone; el dominio nombra.",
                        "La modularidad permite añadir bloques: representaciones con modelos generativos, reducción supervisada o agrupamiento jerárquico. También permite actualizar el modelo con documentos nuevos y observar cómo evolucionan los temas. Esa capacidad de seguimiento es útil para analizar opiniones o incidencias a lo largo del tiempo.",
                    ],
                },
                {
                    "h": "Evaluar sin etiquetas",
                    "p": [
                        "La evaluación es intrínsecamente subjetiva. La coherencia de un tema mide si sus palabras y documentos encajan; la diversidad, si los grupos se solapan; la estabilidad, si pequeños cambios en los datos alteran el resultado. Ninguna métrica automática sustituye una lectura de muestras por grupo.",
                        "Los outliers merecen atención. Un porcentaje alto de ruido puede indicar que la reducción aplastó la estructura o que el umbral de densidad es demasiado exigente. También puede revelar documentos genuinamente singulares que conviene revisar aparte. Ajustar para eliminarlos todos suele producir grupos artificiales.",
                        "El uso práctico combina automatización y lectura. Se agrupa para reducir miles de documentos a decenas de temas, se muestran ejemplos representativos y se pide a una persona que nombre y valide. Después se asignan documentos nuevos por similitud al centro del grupo, con un umbral para enviar lo dudoso a revisión.",
                    ],
                },
            ],
            "brief": [
                "Embedding, reducción y agrupamiento por densidad forman el pipeline",
                "HDBSCAN tolera formas variadas y detecta ruido",
                "c-TF-IDF convierte cada grupo en palabras interpretables",
                "La validación humana es parte del método, no un extra",
            ],
            "keys": [
                "Evalúa primero la calidad del embedding en tu corpus.",
                "Ajusta UMAP y HDBSCAN con muestras, no a ciegas.",
                "Lee documentos de cada grupo antes de confiar en su etiqueta.",
                "Interpreta el ruido como señal, no solo como error.",
                "Asigna documentos nuevos con umbral y revisión.",
            ],
            "example": "Una empresa analiza 40.000 encuestas abiertas. El pipeline descubre veinte grupos; tres son ruido y dos parecen duplicados. Tras leer muestras, el equipo fusiona los duplicados y nombra los temas con el vocabulario del negocio. El resultado prioriza seis problemas de producto que no aparecían en la encuesta cerrada.",
            "caution": "Un grupo con palabras bonitas puede ser una mezcla de temas distintos. Si al leer diez documentos ves tres asuntos diferentes, el problema está en el embedding o en la densidad, no en la etiqueta.",
            "search": "clustering texto topic modeling BERTopic embeddings UMAP HDBSCAN c-TF-IDF coherencia outliers evaluación temas documentos",
        },
    ],
    "quiz": {
        "id": "hllm4q",
        "title": "Cierre del módulo 04",
        "summary": [
            "Un encoder con clasificador ligero suele ser la opción más eficiente cuando hay datos etiquetados.",
            "Las etiquetas, el desequilibrio y las fugas de datos determinan la utilidad real de las métricas.",
            "La clasificación generativa aporta flexibilidad a cambio de coste, latencia y necesidad de validación.",
            "El agrupamiento moderno combina embeddings, UMAP, HDBSCAN y representación de temas.",
        ],
        "questions": [
            {
                "q": "¿Cuál es la forma más económica de aprovechar un encoder para clasificar?",
                "options": [
                    "Reentrenar todos los pesos con millones de ejemplos",
                    "Calcular embeddings una vez y entrenar un clasificador simple encima",
                    "Generar texto libre y contar palabras",
                    "Aumentar la temperatura del modelo",
                ],
                "answer": 1,
                "why": "Con el encoder congelado, los vectores se reutilizan y solo se ajusta una capa pequeña. Es rápido, requiere menos datos y permite comparar modelos sin reentrenar.",
            },
            {
                "q": "¿Por qué la exactitud global puede engañar en un problema desequilibrado?",
                "options": [
                    "Porque siempre es menor que el F1",
                    "Porque una clase mayoritaria puede acaparar los aciertos y ocultar el fallo en las minoritarias",
                    "Porque no se puede calcular",
                    "Porque solo funciona con dos clases",
                ],
                "answer": 1,
                "why": "Predecir siempre la clase frecuente da una exactitud alta y un recall pésimo en el resto. Las métricas por clase y la matriz de confusión muestran el daño real.",
            },
            {
                "q": "¿Qué ventaja tiene HDBSCAN frente a k-means en texto?",
                "options": [
                    "No necesita embeddings",
                    "Detecta grupos de densidad variable y puede marcar outliers",
                    "Es siempre más rápido en cualquier dimensión",
                    "Genera explicaciones en lenguaje natural",
                ],
                "answer": 1,
                "why": "HDBSCAN no impone grupos esféricos ni un número fijo, y deja fuera los puntos aislados. Esa tolerancia encaja con corpus reales llenos de casos raros.",
            },
            {
                "q": "¿Qué aporta c-TF-IDF a un modelo de temas?",
                "options": [
                    "Clasifica los documentos con etiquetas supervisadas",
                    "Encuentra las palabras que distinguen cada grupo del resto del corpus",
                    "Reduce la dimensionalidad de los embeddings",
                    "Genera nuevas preguntas para el usuario",
                ],
                "answer": 1,
                "why": "Compara la frecuencia de términos dentro de un clúster con su frecuencia global. Las palabras sobrerrepresentadas se convierten en una descripción legible del tema.",
            },
        ],
        "exercises": [
            "Etiqueta veinte textos con una taxonomía de cuatro clases y calcula el acuerdo con otra persona.",
            "Compara un clasificador de embeddings con un prompt generativo en coste, latencia y F1 usando los mismos datos.",
            "Agrupa cien noticias y escribe una etiqueta humana para cada grupo; anota qué grupos no te convencen.",
        ],
        "search": "cierre clasificación embeddings zero-shot etiquetas desequilibrio F1 clasificación generativa BERTopic UMAP HDBSCAN temas",
    },
}
