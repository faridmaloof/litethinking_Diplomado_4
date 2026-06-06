# Reglas de Interceptación

Este directorio contiene archivos JSON con reglas de interceptación que se aplican al tráfico HTTP/HTTPS. Los cambios en estos archivos se aplican automáticamente sin reiniciar el contenedor (hot-reload).

## Formato de las Reglas

Cada archivo JSON puede contener múltiples reglas con el siguiente formato:

```json
{
  "Nombre_Regla": {
    "Tipo_intercepcion": "Request" | "Response",
    "Ruta": "ruta/api/ejemplo",
    "Metodo": "GET" | "POST" | "PUT" | "DELETE" | etc.,
    "Descripcion": "Descripción opcional de la regla",
    "Tipo_modificacion": "Completo" | "Parcial",
    "Datos": {
      "campo1": "valor1",
      "campo2": "<FuncionDinamica()>",
      "...": "..."
    }
  }
}
```

## Tipos de Interceptación

- `Request`: Intercepta y modifica las solicitudes entrantes
- `Response`: Intercepta y modifica las respuestas salientes

## Tipos de Modificación

- `Completo`: Reemplaza completamente el body con los datos especificados
- `Parcial`: Combina los datos especificados con el body original

## Funciones Dinámicas

Puedes usar funciones dinámicas entre `< >` que se evalúan en tiempo de ejecución:

- `<Aleatorio([lista])>` - Selecciona un elemento aleatorio de una lista
- `<Aleatorio(min, max)>` - Genera un número entero aleatorio en el rango especificado
- `<UUID()>` - Genera un UUID único
- `<FechaActual('formato')>` - Fecha/hora actual en el formato especificado
- `<TextoAleatorio(longitud)>` - Genera texto aleatorio de la longitud especificada
- `<Base64('texto')>` - Codifica texto en base64
- `<Delay(ms)>` - Introduce un retraso en milisegundos
- `<Error(codigo)>` - Simula un código de error HTTP

## Ejemplos

Ver los archivos `example_api_a.json` y `example_api_b.json` para ejemplos prácticos.