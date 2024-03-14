import 'package:flutter/material.dart';
import 'package:avatar_glow/avatar_glow.dart';
import 'package:speech_to_text_google_dialog/speech_to_text_google_dialog.dart';

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
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      floatingActionButton: GestureDetector(
        onTap: toggleListening, // Utiliza el método toggleListening en lugar de repetir la lógica de pulsar el botón
        child: AvatarGlow(
          startDelay: const Duration(milliseconds: 1000),
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
              radius: 50.0,
            ),
          ),
        ),
      ),
      bottomNavigationBar: SizedBox(height: 50.0),
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
                  fit: BoxFit.contain,
                ),
              ),
            ),
            const SizedBox(height: 20.0),
            const Text(
              'Speech Recognition Result:',
              style: TextStyle(fontSize: 16.0, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10.0),
            Text(
              textSpeech,
              style: const TextStyle(fontSize: 18.0),
            ),
          ],
        ),
      ),
    );
  }

  void toggleListening() async {
    setState(() {
      isRecording = !isRecording; //lo devuelve true 
    });

    if (isRecording) {
      // Iniciar la escucha
      bool isServiceAvailable = await SpeechToTextGoogleDialog.getInstance()
          .showGoogleDialog(
        onTextReceived: (data) {
          setState(() {
            textSpeech = data.toString();
          });
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
      // Detener la escucha
            // Detener la escucha (no se necesita hacer nada aquí)

    }
  }
}
