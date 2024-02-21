#pip install pymsteams
import pymsteams

def enviar_notificacion_a_teams(ticket_doc):
    # Inicializar el mensaje de Microsoft Teams
    myTeamsMessage = pymsteams.connectorcard("https://uses0.webhook.office.com/webhookb2/7dcd3cef-d35c-4bff-b9b7-aad246c024a3@ef4a684e-81b5-491c-a98e-c7b31be6c469/IncomingWebhook/75c11eb3a7f2477fa9f0041e7d50fc84/b14c93cf-6593-4128-8d9c-228d9378864e")
    
  
    # Personalizar el mensaje con la información del ticket
    mensaje = "Nuevo pedido recibido"
    
    # Agregar la línea de Platos
    mensaje += "\nPlatos:"
    
    for plato in ticket_doc['platos']:
        mensaje += f"\n- {plato['nombre']}, Tamaño: {plato['tamaño']}, Precio: {plato['precio']}, Cantidad: {plato['cantidad']}"

    mensaje += f"\nPrecio total: {ticket_doc['precio_total']}"
        
    # Configurar el color del mensaje
    myTeamsMessage.color("#F8C471")
    
    # Agregar el mensaje al objeto Teams
    myTeamsMessage.text(mensaje)
    
    # Enviar el mensaje
    myTeamsMessage.send()



