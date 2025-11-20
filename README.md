# Tarea 3 – Sistemas Distribuidos
## Análisis Lingüístico Offline con Hadoop y Pig

Este repositorio contiene la tercera entrega del proyecto del curso **Sistemas Distribuidos**, cuyo objetivo es implementar un módulo de **procesamiento batch** utilizando **Hadoop, HDFS y Pig** para analizar de forma global un conjunto de textos provenientes de dos fuentes:

- Respuestas de **Yahoo Answers** (texto humano, informal y diverso).
- Respuestas generadas por el **LLM** implementado en entregas anteriores.

El propósito del procesamiento batch es obtener métricas agregadas —tales como frecuencias de palabras, patrones lingüísticos y comparaciones entre corpus— que complementan el flujo asíncrono desarrollado en la Tarea 2.

---

##Arquitectura del sistema

El sistema sigue un flujo **batch offline**, independiente del procesamiento asíncrono de las entregas previas.

### **Flujo general**
1. Exportación de respuestas desde la base de datos hacia archivos `.txt`.
2. Carga de los archivos en el sistema distribuido **HDFS**.
3. Procesamiento Pig:
   - Limpieza textual  
   - Conversión a minúsculas  
   - Tokenización  
   - Eliminación de stopwords  
   - Conteo de palabras  
   - Ordenamiento descendente  
4. Extracción de resultados desde HDFS hacia el host.
5. Visualización mediante gráficos y tablas (Top 10 y Top 50).

La arquitectura se ejecuta dentro de un único contenedor que incluye Hadoop, HDFS y Pig ya configurados.

---

## Ejecución del sistema

### **1. Construir y levantar el contenedor**

```bash
docker compose up -d
```

### 2. Ingresar al contenedor
```bash
docker exec -it tarea3-pig bash
```

### 3. Verificar HDFS
```bash
hdfs dfs -ls /
hdfs dfs -ls /data
```

### 4. Ejecutar el script Pig
```bash
pig /workspace/pig_scripts/wordcount.pig
```

### 5. Descargar resultados
```bash
hdfs dfs -get /output /workspace/results
```
