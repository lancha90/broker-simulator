# Crear una app en python para simular un broker de acciones y crypto

## Descripción del Task
Crear una nueva app en python para simular una broker de acciones y criptomonedas. El broker debe contar con una tabla de balance la cual se actualizar despues de cada venta y compra, una tabla con el historia de trades que se realicen, una tabla para registrar los usuarios. Cada registro de la tabla de balance, tabla del balance por acción que se debe actualizar durante la compra y venta  y tabla de historia de trades debe estar relacionada con la tabla de usuarios.

## Contexto
Actualmente me encuentro construyendo un broker simulado para probar bots autonomos de trading, para lo cual necesito crear la app descrita. Todo el sistema debe ser simple pero funcional.

## Requisitos Específicos

### Servicio para consultar el balance

La app debe tener un servicio especifico para la consulta del balance.

### Servicio para consultar el precio de una acción

La app debe tener un servicio especifico para la consulta del precio actual del servicio. El resultado debe almacenarse en memoria durante 3 minutos. 

La información debe obtenerse usando de alguna de los siguientes fuentes (usar fallbacks).

#### Yahoo

**URL:** `https://query1.finance.yahoo.com/v8/finance/chart/${ticker}?interval=1d&range=1d`
**Method HTTP:** `GET`
**Response:** ```
{
  "chart": {
    "result": [
      {
        "meta": {
          "currency": "USD",
          "symbol": "APP",
          "exchangeName": "NMS",
          "fullExchangeName": "NasdaqGS",
          "instrumentType": "EQUITY",
          "firstTradeDate": 1618493400,
          "regularMarketTime": 1755028801,
          "hasPrePostMarketData": true,
          "gmtoffset": -14400,
          "timezone": "EDT",
          "exchangeTimezoneName": "America/New_York",
          "regularMarketPrice": 467,
          "fiftyTwoWeekHigh": 525.15,
          "fiftyTwoWeekLow": 75.89,
          "regularMarketDayHigh": 470.19,
          "regularMarketDayLow": 458.48,
          "regularMarketVolume": 4507844,
          "longName": "AppLovin Corporation",
          "shortName": "Applovin Corporation",
          "chartPreviousClose": 465.58,
          "priceHint": 2,
          "currentTradingPeriod": {
            "pre": {
              "timezone": "EDT",
              "start": 1754985600,
              "end": 1755005400,
              "gmtoffset": -14400
            },
            "regular": {
              "timezone": "EDT",
              "start": 1755005400,
              "end": 1755028800,
              "gmtoffset": -14400
            },
            "post": {
              "timezone": "EDT",
              "start": 1755028800,
              "end": 1755043200,
              "gmtoffset": -14400
            }
          },
          "dataGranularity": "1d",
          "range": "1d",
          "validRanges": [
            "1d",
            "5d",
            "1mo",
            "3mo",
            "6mo",
            "1y",
            "2y",
            "5y",
            "ytd",
            "max"
          ]
        },
        "timestamp": [1755028801],
        "indicators": {
          "quote": [
            {
              "volume": [4507844],
              "high": [470.190002441406],
              "close": [467],
              "low": [458.480010986328],
              "open": [466.920013427734]
            }
          ],
          "adjclose": [
            {
              "adjclose": [467]
            }
          ]
        }
      }
    ],
    "error": null
  }
}
```
**atributo**: El valor de la acción se debe obtener del siguiente atributo que se encuentra dentro del json `chart?.result?.[0]?.meta?.regularMarketPrice`


#### Alphavantage

**URL:** `https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=${ticker}&apikey=${process.env.ALPHAVANTAGE_API_KEY}`
**Method HTTP:** `GET`
**Response:** ```
{
    "Global Quote": {
        "01. symbol": "APP",
        "02. open": "466.7000",
        "03. high": "470.1900",
        "04. low": "458.4800",
        "05. price": "467.0000",
        "06. volume": "4534018",
        "07. latest trading day": "2025-08-12",
        "08. previous close": "465.5800",
        "09. change": "1.4200",
        "10. change percent": "0.3050%"
    }
}
```
**atributo**: El valor de la acción se debe obtener del siguiente atributo que se encuentra dentro del json `['Global Quote']?.['05. price']`


### Servicio para realizar un trade (compra y venta)

Servicio que debe recibir un ticker (identificador de la acción), una acción (sell o buy) y un precio.

Para la venta el precio debe ser menor o igual al precio que se puede obtener de la misma fuente de "Servicio para consultar el precio de una acción"

Para la compra el precio debe ser mayor o igual al precio que se puede obtener de la misma fuente de "Servicio para consultar el precio de una acción"

### Servicio para consultar el portafolio actual

Servicio que va a retornar las acciones que se tienen compradas del `balance por acción`

### Healthcheck

servicio de health check con la información del servidor donde esta corriendo

## Instrucciones para Claude Code

1. **Analizar el código actual**: Analiza profundamente el requerimiento.
2. **Diseña la solución**: Diseña un plan para implementar el problema descrito.
3. **Implementa la solución**: Implementa la solución siguiente usando las "Consideraciones Técnicas".
4. **Manejo de errores**: Asegúrate de implementar un manejo de errores adecuado.
5. **Test**: No implementar test
6. **Deploy**: Genera un archivo deploy.md con las instrucciones para desplegar esta solución y un par de opciones gratuitas para desplegar la solución.
7. **Documentación**: Actualiza/crea el archivo CLAUDE.md y README.md de acuerdo a los cambios realizados.
8. **API doc**: Generar un archivo `postman.json` con una colección de postman de todos los endpoints disponibles.

## Consideraciones Técnicas

- para la conexión con la base de datos, usar supabase API.
- usar una arquitectura hexagonal para la estructura de paquetes.
- python para la construcción de la app
- todos los endpoints expuestos deben usar un mecanismo de seguridad, usando el header `Authentication` el cual va a ser un api key que debe estar mapeado en la tabla users.
- La cache se debe manejar en la memoria local de la app, pero dejar la app preparada para una posterior implementación de una cache distribuida.
- usar una nomenclatura api rest para los servicios, que permita el versionamiento de los endpoints.

