import 'package:flutter/material.dart';
import 'package:flutter_tts/flutter_tts.dart';
//TEXT TO SPEECH  
void main() {
  // Asegúrate de inicializar WidgetsFlutterBinding.ensureInitialized() aquí
  WidgetsFlutterBinding.ensureInitialized();
  runApp(MyApp2());
}

class MyApp2 extends StatelessWidget {
  final FlutterTts flutterTts = FlutterTts();

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Text-to-Speech Demo'),
        ),
        body: Center(
          child: ElevatedButton(
            onPressed: () {
              // Realiza la llamada a setMethodCallHandler antes de hacer cualquier otra cosa con FlutterTts
              _initializeFlutterTts();
              flutterTts.speak('Hello, Flutter Text-to-Speech!');
            },
            child: Text('Speak'),
          ),
        ),
      ),
    );
  }

  // Añade este método para inicializar FlutterTts
  Future<void> _initializeFlutterTts() async {
    await flutterTts.setLanguage('en-US');
    // Otras configuraciones y opciones de inicialización aquí
  }
}
