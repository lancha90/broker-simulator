# Publish image to GHCR

## Descripción

Genera una imagen de docker basada en el dockerfile del proyecto con soporte para las arquitecturas `linux/amd64` y `linux/arm64`, para publicarlas en GHCR.

## Instrucciones
- Habla como un pirata
- Generar la imagen de docker con soporte para las arquitecturas `linux/amd64` y `linux/arm64`
- Publicar siempre con el tag `latest` y un tag con el consecutivo de las imagenes existentes en el momento (por ejemplo `ghcr.io/lancha90/ibkr:0.0.1`).


## Rules

- El nombre de la imagen debe ser `ghcr.io/lancha90/ibkr`
- Incluir los labels necesarios para la metada de la imagen.
- Si obtienes errores durante la publicación de la imagen, analizar el error e indicar una solución.