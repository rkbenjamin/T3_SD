-- Parámetros con defaults
%default input_path '/data/yahoo.txt';
%default stopwords_path '/data/stopwords.txt';
%default output_path '/output/yahoo_wordcount';

-- 1) Cargar respuestas (una línea = una respuesta)
raw = LOAD '$input_path' USING TextLoader() AS (line:chararray);

-- 2) Pasar a minúsculas
lowered = FOREACH raw GENERATE LOWER(line) AS line;

-- 3) Limpiar: dejar solo letras [a-z] y números, lo demás = espacios
cleaned = FOREACH lowered GENERATE
    REPLACE(line, '[^a-z0-9]+', ' ') AS line;

-- 4) Tokenizar
tokens = FOREACH cleaned GENERATE FLATTEN(TOKENIZE(line)) AS word;

-- 5) Filtrar vacíos
non_empty = FILTER tokens BY word IS NOT NULL AND word != '';

-- 6) Cargar stopwords (una por línea, en minúsculas)
sw = LOAD '$stopwords_path' USING TextLoader() AS (sw:chararray);
sw_trim = FOREACH sw GENERATE TRIM(sw) AS sw;

-- 7) JOIN para eliminar stopwords
joined = JOIN non_empty BY word LEFT OUTER, sw_trim BY sw;

-- 8) Quedarse solo con palabras que NO están en stopwords
filtered = FILTER joined BY sw_trim::sw IS NULL;

-- 9) Proyectar palabra
words = FOREACH filtered GENERATE non_empty::word AS word;

-- 10) Agrupar y contar
grp = GROUP words BY word;
counts = FOREACH grp GENERATE
    group AS word,
    COUNT(words) AS freq;

-- 11) Ordenar por frecuencia
ordered = ORDER counts BY freq DESC;

-- 12) Top 50
topN = LIMIT ordered 50;

-- 13) Guardar resultado
STORE topN INTO '$output_path' USING PigStorage('\t');