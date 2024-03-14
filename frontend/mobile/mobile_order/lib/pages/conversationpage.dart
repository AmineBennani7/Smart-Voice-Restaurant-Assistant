import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:avatar_glow/avatar_glow.dart';
import 'package:speech_to_text_google_dialog/speech_to_text_google_dialog.dart';
import 'package:flutter_tts/flutter_tts.dart';


class ConversationPage extends StatefulWidget {
  const ConversationPage({Key? key}) : super(key: key);

  @override
  _ConversationPageState createState() => _ConversationPageState();
}

class _ConversationPageState extends State<ConversationPage> {
  bool isRecording = false;
  String textSpeech = '';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromARGB(255, 252, 252, 242),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0, // Elimina la sombra del app bar
        
        leading: IconButton(
          padding: const EdgeInsets.only(left: 40.0),
          icon: Icon(Icons.arrow_back),
          iconSize: 30.0,
          onPressed: () {
            Navigator.of(context).pop(); // Vuelve atrás al presionar el botón
          },
        ),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      floatingActionButton: GestureDetector(
        onTap: toggleListening, // Utiliza el método toggleListening en lugar de repetir la lógica de pulsar el botón
        child: AvatarGlow(
          startDelay: const Duration(milliseconds: 10),
          glowColor: const Color.fromARGB(255, 44, 37, 37),
          glowShape: BoxShape.circle,
          curve: Curves.fastOutSlowIn,
          animate: isRecording,
          duration: const Duration(milliseconds: 1500),
          child: Material(
            elevation: 8.0,
            shape: const CircleBorder(),
            color: isRecording
                ? Colors.red // Change the color while recording
                : const Color.fromARGB(255, 222, 167, 72),
            child: CircleAvatar(
              backgroundImage: AssetImage('lib/images/microphone.png'),
              radius: 75.0,
            ),
          ),
        ),
      ),
      bottomNavigationBar: SizedBox(height: 150.0),
      body: Padding(
        padding: const EdgeInsets.all(40.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Center(
              child: Padding(
                padding: const EdgeInsets.only(top: 70.0, bottom: 0.0),
                child: Image.asset(
                  'lib/images/pizza.png',
                  width: 70.0,
                  height: 60.0,
                ),
              ),
            ),
            const SizedBox(height: 40.0),
            const Text(
              'Conversa con nuestro chatbot :',
              style: TextStyle(fontSize: 22.0, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height:80.0),
            Text(
              textSpeech,
              style: const TextStyle(fontSize: 25.0),
            ),
          ],
        ),
      ),
    );
  }

  void toggleListening() async {
  setState(() {
    isRecording = !isRecording;
  });

  if (isRecording) {
    // Iniciar la escucha
    bool isServiceAvailable = await SpeechToTextGoogleDialog.getInstance()
        .showGoogleDialog(
      onTextReceived: (data) async {
        setState(() {
          textSpeech = data.toString();
        });
        
        // Enviar solicitud POST al servidor
        await sendTextToAPI(textSpeech);
      },
      locale: "es-ES", //  español
    );

    if (!isServiceAvailable) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: const Text('El servicio no está disponible'),
        backgroundColor: Colors.red,
        behavior: SnackBarBehavior.floating,
        margin: EdgeInsets.only(
          bottom: MediaQuery.of(context).size.height - 100,
          left: 16,
          right: 16,
        ),
      ));
    }
  } else {
    // Detener la escucha (no se necesita hacer nada aquí)
  }
}

Future<void> sendTextToAPI(String text) async {
  final response = await http.post(
    Uri.parse('http://10.0.2.2:5000/chat'), //Android emulador proporcionan una dirección especial 10.0.2.2 que puedes utilizar en lugar de localhost o 127.0.0.1 
                                            //para referirte a tu máquina anfitriona. Por lo tanto, si haces una solicitud a http://10.0.2.2:5000, l
                                            //a aplicación en el emulador Android podrá comunicarse con tu servidor Flask que se ejecuta en tu máquina física.

    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(<String, String>{
      'user_question': text,
    }),
  );

  if (response.statusCode == 200) {
    // Si la solicitud es exitosa, muestra la respuesta de la API en la pantalla
    setState(() {
      textSpeech = json.decode(response.body)["response"];
    });
  } else {
    // Si hay un error en la solicitud, muestra un mensaje de error en la pantalla
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      content: Text('Error: ${response.statusCode}'),
      backgroundColor: Colors.red,
      behavior: SnackBarBehavior.floating,
      margin: EdgeInsets.only(
        bottom: MediaQuery.of(context).size.height - 100,
        left: 16,
        right: 16,
      ),
    ));
  }
}}