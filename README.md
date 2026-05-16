# Monitor Económico PYME Chile

Herramienta de consola en Python que consulta indicadores económicos chilenos en tiempo real y genera un reporte de conversión de presupuesto. Pensada para el día a día del área financiera de una PYME.

---

## Contexto del proyecto

Las pequeñas y medianas empresas chilenas operan con múltiples monedas de referencia: UF para contratos, dólar y euro para importaciones, UTM para trámites tributarios. Revisar cada valor por separado en distintas fuentes consume tiempo y abre la puerta a errores cuando los datos que se usan están desactualizados.

Este programa resuelve eso en una sola ejecución: consulta `https://mindicador.cl/api`, extrae UF, UTM, dólar y euro, y calcula cuánto equivale un presupuesto en CLP en cada una de esas unidades. El resultado aparece directo en consola, sin fricción.

---

## Indicadores que procesa

| Indicador | Descripción |
|-----------|-------------|
| UF | Unidad de Fomento |
| UTM | Unidad Tributaria Mensual |
| Dólar observado | Tipo de cambio USD/CLP |
| Euro | Tipo de cambio EUR/CLP |

Con esos valores calcula automáticamente el equivalente del presupuesto configurado en UF, USD y EUR.

---

## Configuración mediante variables de entorno

Ningún valor está hardcodeado en el código. Todo se controla desde el entorno:

| Variable | Descripción | Por defecto |
|----------|-------------|-------------|
| `API_BASE_URL` | URL base de la API | `https://mindicador.cl/api` |
| `API_TIMEOUT` | Segundos máximos de espera | `10` |
| `PRESUPUESTO_CLP` | Monto de referencia en pesos | `1500000` |
| `API_TOKEN_CHILE` | Token opcional de autenticación | vacío |

---

## Cómo ejecutar

### Instalación de dependencias

```bash
pip3 install -r requirements.txt
```

### Ejecución básica

```bash
python3 app.py
```

### Con presupuesto personalizado

```bash
export PRESUPUESTO_CLP=3000000
python3 app.py
```

### Con Docker (configuración por defecto)

```bash
chmod +x build.sh
./build.sh
```

### Con Docker y variables personalizadas

```bash
export API_BASE_URL="https://mindicador.cl/api"
export API_TIMEOUT=10
export PRESUPUESTO_CLP=5000000
./build.sh
```

El script `build.sh` construye la imagen, elimina el contenedor anterior si existe y guarda la salida en `evidencias/docker/output.txt` con el resultado de `docker ps -a`, los logs del contenedor y los datos reales obtenidos desde la API.

---

## Casos de error cubiertos

La aplicación detecta y reporta de forma clara los siguientes problemas:

- Timeout al conectar con la API
- Error de red o DNS
- Respuesta HTTP 404
- Credenciales inválidas o rechazadas
- JSON malformado en la respuesta
- Campos esperados ausentes en el JSON
- Errores HTTP genéricos

---

## Integración con Jenkins

### BuildAppJob

Trabajo de tipo freestyle. Clona el repositorio desde GitHub y ejecuta:

```bash
chmod +x build.sh
./build.sh
```

### SamplePipeline

Pipeline declarativo con dos etapas: **Preparation** y **Build**. El script completo se encuentra en:

```
evidencias/jenkins/pipeline_script.txt
```

Capturas requeridas en `evidencias/jenkins/`:

- `stage_view.png`
- `console_output_build.png`
- `credentials.png`

---

## Estructura del proyecto

```
Evaluacion2/
├── app.py
├── build.sh
├── requirements.txt
├── Dockerfile
├── .gitignore
├── README.md
└── evidencias/
    ├── docker/
    │   └── output.txt
    └── jenkins/
        ├── pipeline_script.txt
        ├── stage_view.png
        ├── console_output_build.png
        └── credentials.png
```