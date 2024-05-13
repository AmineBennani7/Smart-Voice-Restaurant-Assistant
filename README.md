[![Smart-Voice Restaurant Assistant](https://img.shields.io/badge/Smart--Voice%20Restaurant%20Assistant-ff69b4?style=for-the-badge&labelColor=black&logoWidth=40)](https://github.com/AmineBennani7/Proyecto-Reconocimiento-Vocal)




[![es](https://img.shields.io/badge/lang-es-yellow.svg)](https://github.com/AmineBennani7/Proyecto-Reconocimiento-Vocal/blob/master/README.es.md)







# Voice-Based Restaurant Order Virtual Assistant for Mobile App:

## About This Project

This project consists of a mobile application that integrates a voice recognition system to allow users to interact with a personalized virtual assistant in the hospitality sector. Users can request information about available dishes and place orders directly through the application using voice commands.

The virtual assistant operates in an intelligent and optimized manner, recording orders placed by users and generating a complete list of selected dishes along with the total price at the end of the interaction. The assistant never leaves the context of the restaurant setting. If a requested dish is not present in the restaurant's database, the assistant responds negatively, informing the user that the dish is not available.

For the correct operation of the chatbot, it connects through **Langchain to the OpenAI API**, specifically using the **GPT-4-1106-preview** model to provide intelligent and contextually appropriate responses during interactions.

In addition, the system includes a web application intended exclusively for restaurant employees or administrators. This application will allow them to manage orders received and make adjustments related to the configuration of the mobile application and the personalization of the restaurant menu.

<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
    <img src="imgs/movil3.png" alt="Imagen Izquierda" style="width: 27%;"  />
    <img src="imgs/movil4.png" alt="Imagen Derecha" style="width: 50%;" />
</div>

<img src="imgs/web2.png" alt="Imagen Abajo" style="width: 100%;, height: 100%" />

## Built with

This project has been developed using the following main technologies and tools:
- ![ReactJS](https://img.shields.io/badge/ReactJS-61DAFB?logo=react&logoColor=white)
- ![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?logo=bootstrap&logoColor=white)
- ![Flutter](https://img.shields.io/badge/Flutter-02569B?logo=flutter&logoColor=white)
- ![Dart](https://img.shields.io/badge/Dart-0175C2?logo=dart&logoColor=white)
- ![MongoDB](https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white)
- ![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white)
- ![Langchain](https://img.shields.io/badge/Langchain-007ACC?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABeElEQVR42mL8//8/Ay0AJTjQDAyMjKJBA5YQnBhgoKC0BPDw+xEJAFpZwcFiLx5AJ9/2AopIVh6CbA+GQBFG0DNMOI0iwVMABJWcB9gMB1G0NhaRA7NjJAOZS/EDl4A7l7XEMGFiqgsCEQYmCAvQAegDLsDnABQj8IiYGBgl9E4DKxGFHlAe7uEQByFsXmASvDD8A8VQUVC/kNcDcKATh8wExlDvQMc/gOZhg5D8SggZ0AKbAHHJZAQkGRUjwoIlkI6C5YDAW3hElAaQCoU5AEyACMmPzAI3kV8ArAEiAULDSBlYB6BWFQwABVyEyUKYXYFsCGAH1sKkYCkBiYTA9gpUCAAJIqUKG8IhR7AAA+AN5jhYN0DqAQ4EIzAPhcWBA8E3AM9C8QVBUVU9Q9wPkc2XJmIXmAGJdJwGtVbE4TMOZk4hHkgkEycXA1WlwLI6IeGiiJABZqAigSswgkCjU5BgAApJggMAV1jJKlAMpBYDGicFAABgkUSWDDoTiqQgwCwNDNlHMTESmrMlATGQDAxEgGYOgSGEEAAD2sXEGXERKAAAAAElFTkSuQmCC&logoColor=white)


## Getting Started 

1. **Clone the repository :**

  ```bash
git clone https://github.com/AmineBennani7/Proyecto-Reconocimiento-Vocal
  ```

2. **Install Dependencies:**

Run the following command in your terminal:

```bash
pip install -r requirements.txt
 ```

3. **Generation of a personal key in OPENAI:**

To use the GPT-4-1106-preview model of OpenAI in your application, you will need to generate a personal key in the OpenAI platform. For this, you should follow the following steps:

3.1. Go to the official **[OpenAI](https://platform.openai.com/settings/profile?tab=api-keys)** page and create an account if you don't have one yet.

3.2. Go to the API setting section and find the option to **generate a new API key**. Remember to keep your API key safe and not to share it with anyone.

3.3. Create a new virtual environment **.env** and enter the secret key generated in OpenAI:

```bash
cd backend/src/chatbot/ && python -m venv .env
```
<img src="imgs/env.png" alt="Imagen Abajo" style="width: 70%;, height: 100%" />

&nbsp;


4. **Run the following files the first time:**

4.1. Load the default menu items into the database, which the administrator can later modify through the web application.

```bash
python "backend/src/database/load_data.py"
```

4.2. Transform the menu items in the database into a CSV format that can be correctly read by the chatbot.

```bash
python "backend/src/chatbot/get_menu_dataset.py"
```

## Program use
Next, it explains what needs to be run each time you want to use the program:

Run the backend for the correct operation of the chatbot:
```bash
python "backend/src/api/api_main.py"
```

Run the backend for the correct operation of the web server:
```bash
python "web/server/app.py"
```

Go to the following directory and run **main.dart** to make the mobile application function. Previously, the mobile emulator should have been set up.
 
```bash
cd .\mobile\mobile\mobile_order\lib
```
Run the web application for employees and administrator.

```bash
cd .\web\frontend ; npm start
```


## More images 

<img src="imgs/web3.png" alt="Imagen Abajo" style="width: 100%;, height: 100%" />
&nbsp;

<img src="imgs/web7.png" alt="Imagen Abajo" style="width: 100%;, height: 100%" />




## Contact

Amine Bennani - [![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/amine-bennani-51638410a/)

Project link - [![GitHub](https://img.shields.io/badge/GitHub-Profile-blue?style=for-the-badge&logo=github)](https://github.com/AmineBennani7/Smart-Voice-Restaurant-Assistant)




