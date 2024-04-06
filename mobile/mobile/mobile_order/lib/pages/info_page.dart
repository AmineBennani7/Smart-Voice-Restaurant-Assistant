import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:mobile_order/components/button_info.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';


class InfoPage extends StatelessWidget {
  const InfoPage({Key? key});

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
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(40.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
          Center(
            child: Padding(
              padding: const EdgeInsets.only(top: 0.0, bottom: 0.0),
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
              Padding(
                padding: const EdgeInsets.only(top: 20.0),
                child: Center(
                  child: Text(
                    "Instrucciones : ",
                    style: GoogleFonts.kanit(
                      fontSize: 30,
                      fontWeight: FontWeight.bold,
                      color: Colors.black,
                    ),
                    textAlign: TextAlign.center,
                  ),
                ),
              ),
              SizedBox(height: 40.0),
              _buildInstructionRow(
                'lib/images/chatbot2.png',
                "Interactúa de forma natural con nuestro chatbot, utilizando tu voz para solicitar información sobre nuestros platos y hacer tus pedidos cómodamente.",
              ),
              SizedBox(height: 40.0),
              _buildInstructionRow(
                'lib/images/tarjeta_credito.png',
                "Después de realizar tu pedido, recibirás una notificación para proceder al pago en caja. Por el momento, no ofrecemos la opción de pago móvil.",
              ),
              SizedBox(height: 40.0),
              _buildInstructionRow(
                'lib/images/spaguetti.png',
                "Finalmente espera mientras preparamos y servimos tus deliciosos platos que has pedido.",
              ),
              SizedBox(height: 120.0),
              Center(
                child: myButtonInfo(text: "EMPEZAR A PEDIR"),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildInstructionRow(String imagePath, String text) {
    return Row(
      children: [
        Image.asset(
          imagePath,
          width: 80.0,
          height: 80.0,
        ),
        SizedBox(width: 10),
        Expanded(
          child: Text(
            text,
            style: GoogleFonts.kanit(
              fontSize: 16,
              color: const Color.fromARGB(255, 44, 44, 44),
            ),
          ),
        ),
      ],
    );
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





