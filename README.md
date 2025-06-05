# GondolaInteligente

Este repositorio contiene scripts de ejemplo para detección de objetos y control de stock.

## Automatización con Google Sheets

El archivo `sheet_scheduler.py` permite consultar una hoja de cálculo de Google Sheets y enviar avisos por correo cuando el stock de un SKU alcanza los valores mínimo o máximo.

### Uso rápido
1. Coloque las credenciales de su cuenta de servicio en `service_account_file.json` o defina la variable de entorno `GOOGLE_SERVICE_ACCOUNT_FILE` con la ruta al archivo.
2. Establezca el nombre del documento en la variable de entorno `GOOGLE_SPREADSHEET_NAME`.
3. Configure las variables `NOTIFY_EMAIL_USER`, `NOTIFY_EMAIL_PASSWORD` y `NOTIFY_EMAIL_TO` para el envío de correos.
4. Ejecute:

```bash
python sheet_scheduler.py
```

La tarea se ejecutará cada hora y enviará un correo si algún SKU tiene niveles fuera de los rangos configurados en la hoja.
