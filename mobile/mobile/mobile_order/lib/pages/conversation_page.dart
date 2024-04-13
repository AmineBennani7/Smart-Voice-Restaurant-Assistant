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
  bool showMicrophoneButton = true;

  @override
  Widget build(BuildContext context) {
    if (textSpeech.isEmpty) {
      textSpeech =
          "Bienvenido a nuestro restaurante, empiece a hablar vocalmente conmigo pulsando en el botón de grabar.";
      flutterTts.setLanguage('es-ES');
      flutterTts.setSpeechRate(0.5);
      flutterTts.speak(textSpeech);
    }

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
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: () {
              resetConversation(); // Llamar a la función para reiniciar la conversación
            },
          ),
        ],
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      floatingActionButton: Visibility(
        visible: showMicrophoneButton,
        child: GestureDetector(
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
                  width: 80.0,
                  height: 80.0,
                ),
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
              Align(
                alignment: Alignment.center,
                child: Padding(
                  padding: const EdgeInsets.only(right: 15.0),
                  child: FutureBuilder<Map<String, dynamic>>(
                    future: fetchCustomization(),
                    builder: (context, snapshot) {
                      if (snapshot.hasData) {
                        return Image.network(
                          'http://10.0.2.2:5000/app_customization/file/${snapshot.data?['logoSecundario'] ?? ''}',
                          width: 70.0,
                          height: 60.0,
                          fit: BoxFit.contain,
                        );
                      } else if (snapshot.hasError) {
                        return Text('${snapshot.error}');
                      }
                      return CircularProgressIndicator();
                    },
                  ),
                ),
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
      await flutterTts.stop();
    }

    if (isRecording) {
      bool isServiceAvailable = await SpeechToTextGoogleDialog.getInstance()
          .showGoogleDialog(
        onTextReceived: (data) async {
          await sendTextToAPI(data.toString());
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
    }
  }

  Future<void> sendTextToAPI(String text) async {
    final response = await http.post(
      Uri.parse('http://10.0.2.2:8000/chat'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String>{
        'user_question': text,
      }),
    );

    if (response.statusCode == 200) {
      final responseData = json.decode(response.body);
      final botResponse = responseData["response"];
      setState(() {
        textSpeech = botResponse;
        showMicrophoneButton = !botResponse.toLowerCase().contains("número de pedido");
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

  Future<Map<String, dynamic>> fetchCustomization() async {
    final response = await http.get(Uri.parse('http://10.0.2.2:5000/app_customization'));

    if (response.statusCode == 200) {
      String jsonString = response.body;
      dynamic decodedJson = jsonDecode('[' + jsonString + ']'); 
      jsonString = decodedJson[0];
 
      Map<String, dynamic> responseObject = jsonDecode(jsonString);
  
      String logoSecundario = responseObject['logo_secundario'];

      return {
        'logoSecundario': logoSecundario,
      };
    } else {
      throw Exception('Failed to load customization data');
    }
  }

  Future<void> resetConversation() async {
    final response = await http.post(
      Uri.parse('http://10.0.2.2:8000/reset'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
    );

    if (response.statusCode == 200) {
      setState(() {
        textSpeech = "Bienvenido a nuestro restaurante, empiece a hablar vocalmente conmigo pulsando en el botón de grabar.";
        flutterTts.speak(textSpeech);
        showMicrophoneButton = true; // Restaurar el botón del micrófono
      });
    } else {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text('Error al reiniciar la conversación'),
        backgroundColor: Colors.red,
        behavior: SnackBarBehavior.floating,
      ));
    }
  }
}
