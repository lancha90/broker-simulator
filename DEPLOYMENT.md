# Guía de Deployment en Render.com

## Pasos para Desplegar

### 1. Preparar el Repositorio

Asegúrate de que tu código esté en un repositorio de GitHub. Los archivos necesarios ya están configurados:

- `requirements.txt` - Dependencias de Python
- `render.yaml` - Configuración de deployment
- `.env.example` - Variables de entorno requeridas

### 2. Crear Cuenta en Render

1. Ve a [render.com](https://render.com)
2. Crea una cuenta (puedes usar tu cuenta de GitHub)
3. Conecta tu repositorio de GitHub

### 3. Configurar el Servicio Web

#### Opción A: Usando render.yaml (Recomendado)
1. En el dashboard de Render, selecciona "New" → "Blueprint"
2. Conecta tu repositorio
3. Render detectará automáticamente el archivo `render.yaml`

#### Opción B: Configuración Manual
1. Selecciona "New" → "Web Service"
2. Conecta tu repositorio
3. Configura:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker`
   - **Python Version**: 3.11.0

### 4. Configurar Variables de Entorno

En la configuración del servicio, añade estas variables:

#### Variables Requeridas:
- `SUPABASE_URL`: Tu URL de proyecto Supabase
- `SUPABASE_KEY`: Tu clave anónima de Supabase

#### Variables Opcionales:
- `ALPHAVANTAGE_API_KEY`: Para datos de precios alternativos
- `ENVIRONMENT`: `production` (para deshabilitar reload)
- `SSL_VERIFY`: `true` (por defecto)

### 5. Deployment

1. Haz clic en "Create Web Service"
2. Render iniciará el proceso de build y deploy
3. El servicio estará disponible en `https://tu-servicio.onrender.com`

### 6. Configurar Base de Datos

#### En Supabase:
1. Ve a tu proyecto en [supabase.com](https://supabase.com)
2. En SQL Editor, ejecuta el script de `database_setup.sql`
3. Copia la URL y la API Key anónima
4. Configúralas en las variables de entorno de Render

### 7. Verificar Deployment

1. Visita `https://tu-servicio.onrender.com/health`
2. Deberías ver la respuesta del health check
3. La documentación de la API estará en `/docs`

## Configuración Automática de Render

El archivo `render.yaml` incluye:

```yaml
services:
  - type: web
    name: ibkr-broker-simulator
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn main:app --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker
    healthCheckPath: /health
```

## Monitoreo y Logs

- **Logs**: Disponibles en el dashboard de Render
- **Métricas**: CPU, memoria y respuestas HTTP
- **Health Check**: Automático en `/health`

## Plan Free vs Paid

### Plan Free:
- 750 horas/mes
- Se duerme después de inactividad
- 512MB RAM
- Shared CPU

### Plan Paid:
- Siempre activo
- Más recursos
- Dominios custom
- Backups automáticos

## Troubleshooting

### Error de Build
- Verifica `requirements.txt`
- Revisa los logs de build

### Error de Start
- Confirma que todas las variables de entorno estén configuradas
- Revisa la conexión a Supabase

### Error 503
- El servicio puede estar "dormido" (plan free)
- Espera unos segundos para que se active

## Comandos Útiles

### Desarrollo Local
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor de desarrollo
python main.py
```

### Variables de Entorno Locales
Copia `.env.example` a `.env` y configura tus valores:
```bash
cp .env.example .env
```

## Seguridad

- Las variables de entorno están marcadas como `sync: false` para mayor seguridad
- SSL verification está habilitado por defecto
- API keys no se exponen en logs

## URLs Importantes

- **API**: `https://tu-servicio.onrender.com`
- **Docs**: `https://tu-servicio.onrender.com/docs`
- **Health**: `https://tu-servicio.onrender.com/health`
- **Dashboard Render**: `https://dashboard.render.com`