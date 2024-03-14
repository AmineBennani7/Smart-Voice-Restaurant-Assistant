import 'package:flutter/material.dart';
import 'package:avatar_glow/avatar_glow.dart';
import 'package:speech_to_text_google_dialog/speech_to_text_google_dialog.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ConversationPage extends StatefulWidget {
  const ConversationPage({Key? key}) : super(key: key);

  @override
  _ConversationPageState createState() => _ConversationPageState();
}

class _ConversationPageState extends State<ConversationPage> {
  bool isRecording = false;
  String textSpeech = '';
  final FlutterTts flutterTts = FlutterTts();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromARGB(255, 252, 252, 242),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          padding: const EdgeInsets.only(left: 16.0),
          icon: Icon(Icons.arrow_back),
          iconSize: 30.0,
          onPressed: () {
            Navigator.of(context).pop();
          },
        ),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      floatingActionButton: GestureDetector(
        onTap: toggleListening,
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
                ? Colors.red
                : const Color.fromARGB(255, 222, 167, 72),
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Image.asset(
                'lib/images/microphone.png',
                width: 40.0,
                height: 40.0,
              ),
            ),
          ),
        ),
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              SizedBox(height: 12.0),
              Image.asset(
                'lib/images/pizza.png',
                width: 70.0,
                height: 60.0,
              ),
              SizedBox(height: 40.0),
              Text(
                'Conversa con nuestro chatbot :',
                style: TextStyle(fontSize: 22.0, fontWeight: FontWeight.bold),
                textAlign: TextAlign.center,
              ),
              SizedBox(height: 40.0),
              Text(
                textSpeech,
                style: TextStyle(fontSize: 25.0),
                textAlign: TextAlign.center,
              ),
            ],
          ),
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
        locale: "es-ES",
      );

      if (!isServiceAvailable) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: const Text('El servicio no está disponible'),
          backgroundColor: Colors.red,
          behavior: SnackBarBehavior.floating,
        ));
      }
    } else {
      // Detener la escucha (no se necesita hacer nada aquí)
    }
  }

  Future<void> sendTextToAPI(String text) async {
    final response = await http.post(
      Uri.parse('http://10.0.2.2:5000/chat'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String>{
        'user_question': text,
      }),
    );

    if (response.statusCode == 200) {
      setState(() {
        textSpeech = json.decode(response.body)["response"];
      });

      await flutterTts.setLanguage('es-ES');
      await flutterTts.setSpeechRate(0.5);
      await flutterTts.speak(textSpeech);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text('Error: ${response.statusCode}'),
        backgroundColor: Colors.red,
        behavior: SnackBarBehavior.floating,
      ));
    }
  }
}
