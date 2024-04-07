import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:google_fonts/google_fonts.dart';
import '../components/button_intro.dart';

class IntroPage extends StatelessWidget {
  const IntroPage({Key? key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromARGB(255, 252, 252, 242),
      body: SingleChildScrollView( //RESPONSIVE
        child: Padding(
          padding: const EdgeInsets.all(40.0),
          child: FutureBuilder<Map<String, dynamic>>(
            future: fetchCustomization(),
            builder: (context, snapshot) {
              if (snapshot.hasData) {
                return Column(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    SizedBox(height: 70.0),
                    Image.network(
                      'http://10.0.2.2:5000/app_customization/file/${snapshot.data?['logoSecundario'] ?? ''}',
                      width: 70.0,
                      height: 60.0,
                      fit: BoxFit.contain,
                    ),
                    SizedBox(height: 20.0),
                    Text(
                      "Bienvenido a ${snapshot.data?['nombreRestaurante'] ?? 'Nombre desconocido'}",                      style: GoogleFonts.kanit(
                        fontSize: 30,
                        fontWeight: FontWeight.bold,
                        color: Colors.black,
                      ),
                      textAlign: TextAlign.center,
                    ),
                    SizedBox(height: 20.0),
                    Text(
                      "Aplicación para ordenar tu comida y pedir información rápidamente hablando con nuestro asistente virtual sin la necesidad de hacer cola.",
                      style: GoogleFonts.kanit(
                        color: Colors.grey,
                        fontSize: 16,
                      ),
                      textAlign: TextAlign.center,
                    ),
                    SizedBox(height: 60.0),
                    Image.network(
                      'http://10.0.2.2:5000/app_customization/file/${snapshot.data?['logoPrincipal'] ?? ''}',
                      width: MediaQuery.of(context).size.width * 0.6, //PARA VOLVERLO RESPONSIVE
                      height: MediaQuery.of(context).size.height * 0.3,
                      fit: BoxFit.contain,
                    ),
                    SizedBox(height:120.0),
                    Center(
                      child: MyButton(text: "EMPEZAR"),
                    ),
                  ],
                );
              } else if (snapshot.hasError) {
                return Text('${snapshot.error}');
              }
              return CircularProgressIndicator();
            },
          ),
        ),
      ),
    );
  }
}

Future<Map<String, dynamic>> fetchCustomization() async {
  final response = await http.get(Uri.parse('http://10.0.2.2:5000/app_customization')); //Flask api (react)

  if (response.statusCode == 200) {
    String jsonString = response.body;
    dynamic decodedJson = jsonDecode('[' + jsonString + ']'); //Lo metemos en una lista y abajo sacamos solo el elemento 0
    jsonString = decodedJson[0];  //Lo hacemos asi ya que el formato json contiene "" al principio y al final y esta es una buena solucion para quitarlos
 
    Map<String, dynamic> responseObject = jsonDecode(jsonString);
    String nombreRestaurante = responseObject['nombre_restaurante'];
    String logoPrincipal = responseObject['logo_principal'];
    String logoSecundario = responseObject['logo_secundario'];

    return {
      'nombreRestaurante': nombreRestaurante,
      'logoPrincipal': logoPrincipal,
      'logoSecundario': logoSecundario,
    };
  } else {
    throw Exception('Failed to load customization data');
  }
}