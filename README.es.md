[![Smart-Voice Restaurant Assistant](https://img.shields.io/badge/Smart--Voice%20Restaurant%20Assistant-ff69b4?style=for-the-badge&labelColor=black&logoWidth=40)](https://github.com/AmineBennani7/Proyecto-Reconocimiento-Vocal)


[![en](https://img.shields.io/badge/lang-en-brightgreen.svg)](https://github.com/AmineBennani7/Proyecto-Reconocimiento-Vocal/blob/master/README.md)


# Asistente Virtual para Pedidos en Restaurantes mediante Comandos de Voz para Aplicación Móvil: 

## Sobre este proyecto

Este proyecto consiste en una una aplicación móvil que integra un sistema de reconocimiento de voz para permitir a los usuarios interactuar con un asistente virtual personalizado en el ámbito de la hostelería. Los usuarios podrán solicitar información sobre los platos disponibles y realizar pedidos directamente a través de la aplicación mediante comandos de voz.

El asistente virtual opera de manera inteligente y optimizada, registrando los pedidos realizados por los usuarios y generando una lista completa de los platos seleccionados junto con el precio total al finalizar la interacción. El asistente nunca sale del contexto del contexto del ámbito del restaurante.  Si un plato solicitado no está presente en la base de datos del restaurante, el asistente responde negativamente informando al usuario que el plato no está disponible.

Para el correcto funcionamiento del chatbot, este se conecta a través de **Langchain a la API de OpenAI**, específicamente utilizando el modelo **GPT-4-1106-preview** para proporcionar respuestas inteligentes y contextualmente adecuadas durante las interacciones.

Además, el sistema incluye una aplicación web destinada exclusivamente a empleados o administradores del restaurante. Esta aplicación permitirá gestionar los pedidos recibidos y realizar ajustes relacionados con la configuración de la aplicación móvil y de la personalización del menú del restaurante.

<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
    <img src="imgs/movil3.png" alt="Imagen Izquierda" style="width: 27%;"  />
    <img src="imgs/movil4.png" alt="Imagen Derecha" style="width: 50%;" />
</div>

<img src="imgs/web2.png" alt="Imagen Abajo" style="width: 100%;, height: 100%" />

## Construido con

Este proyecto ha sido desarrollado utilizando las siguientes tecnologías y herramientas principales:
- ![ReactJS](https://img.shields.io/badge/ReactJS-61DAFB?logo=react&logoColor=white)
- ![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?logo=bootstrap&logoColor=white)
- ![Flutter](https://img.shields.io/badge/Flutter-02569B?logo=flutter&logoColor=white)
- ![Dart](https://img.shields.io/badge/Dart-0175C2?logo=dart&logoColor=white)
- ![MongoDB](https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white)
- ![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white)
- ![Langchain](https://img.shields.io/badge/Langchain-007ACC?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABeElEQVR42mL8//8/Ay0AJTjQDAyMjKJBA5YQnBhgoKC0BPDw+xEJAFpZwcFiLx5AJ9/2AopIVh6CbA+GQBFG0DNMOI0iwVMABJWcB9gMB1G0NhaRA7NjJAOZS/EDl4A7l7XEMGFiqgsCEQYmCAvQAegDLsDnABQj8IiYGBgl9E4DKxGFHlAe7uEQByFsXmASvDD8A8VQUVC/kNcDcKATh8wExlDvQMc/gOZhg5D8SggZ0AKbAHHJZAQkGRUjwoIlkI6C5YDAW3hElAaQCoU5AEyACMmPzAI3kV8ArAEiAULDSBlYB6BWFQwABVyEyUKYXYFsCGAH1sKkYCkBiYTA9gpUCAAJIqUKG8IhR7AAA+AN5jhYN0DqAQ4EIzAPhcWBA8E3AM9C8QVBUVU9Q9wPkc2XJmIXmAGJdJwGtVbE4TMOZk4hHkgkEycXA1WlwLI6IeGiiJABZqAigSswgkCjU5BgAApJggMAV1jJKlAMpBYDGicFAABgkUSWDDoTiqQgwCwNDNlHMTESmrMlATGQDAxEgGYOgSGEEAAD2sXEGXERKAAAAAElFTkSuQmCC&logoColor=white)


## Empezando 

1. **Clonar el repositorio :**

  ```bash
git clone https://github.com/AmineBennani7/Proyecto-Reconocimiento-Vocal
  ```

2. **Instalar Dependencias:**

Ejecuta el siguiente comando en tu terminal:

```bash
pip install -r requirements.txt
 ```

3. **Generación de una clave personal en OPENAI:**

Para utilizar el modelo GPT-4-1106-preview de OpenAI en tu aplicación, necesitarás generar una clave personal en la plataforma OpenAI, . Para ello deberás seguir los siguientes pasos: 

3.1. Ir a la página oficial de **[OpenAI](https://platform.openai.com/settings/profile?tab=api-keys)** y crear una cuenta si aún no tienes una

3.2. Ir a la sección de configuración de API  y buscar la opción para **generar una nueva clave de API**. Recuerda mantener segura tu clave de API y no compartirla con nadie.

3.3. Crear un nuevo entorno virtual **.env** e introducir la clave secreta generada en OPENAI
```bash
cd backend/src/chatbot/ && python -m venv .env
```
<img src="imgs/env.png" alt="Imagen Abajo" style="width: 70%;, height: 100%" />

&nbsp;


4. **Ejecutar los siguientes ficheros la primera vez:**

4.1.  Cargar los elementos del menú por defecto en la base de datos, los cuales luego el administrador podrá modificar a través de la aplicación web.

```bash
python "backend/src/database/load_data.py"
```

4.2. Transformar los elementos del menú de la base de datos a un formato CSV que pueda ser leído correctamente por el chatbot.
```bash
python "backend/src/chatbot/get_menu_dataset.py"
```

## Uso del programa
A continuación, se detalla qué es lo que se tiene que ejecutar cada vez que se quiera usar el programa :


Ejecutar el backend para el correcto funcionamiento del chatbot:
```bash
python "backend/src/api/api_main.py"
```

Ejecutar el backend para el correcto funcionamiento del servidor web:
```bash
python "web/server/app.py"
```

Ir al siguiente directorio y ejecutar **main.dart** para hacer funcoinar la aplicación móvil. Previamente, se debería tener configurado el emulador móvil. 
```bash
cd .\mobile\mobile\mobile_order\lib
```
Ejecutar la aplicación web para los empleados y administrador. 
```bash
cd .\web\frontend ; npm start
```


## Más imágenes 

<img src="imgs/web3.png" alt="Imagen Abajo" style="width: 100%;, height: 100%" />
&nbsp;

<img src="imgs/web7.png" alt="Imagen Abajo" style="width: 100%;, height: 100%" />




## Contacto

Amine Bennani - [![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/amine-bennani-51638410a/)

Link del proyecto - [![GitHub](https://img.shields.io/badge/GitHub-Profile-blue?style=for-the-badge&logo=github)](https://github.com/AmineBennani7/Smart-Voice-Restaurant-Assistant)




