
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Fetch Data Example'),
        ),
        body: Center(
          child: FutureBuilder<Map<String, dynamic>>(
            future: fetchCustomization(),
            builder: (context, snapshot) {
              if (snapshot.hasData) {
                return Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: <Widget>[
                    Text("Restaurant's name: ${snapshot.data == null ? 'Unknown' : snapshot.data?['nombreRestaurante']}"),
                   Image.network('http://10.0.2.2:5000/app_customization/file/${snapshot.data?['logoPrincipal'] ?? ''}'),
                   Image.network('http://10.0.2.2:5000/app_customization/file/${snapshot.data?['logoSecundario'] ?? ''}')
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
  final response = await http.get(Uri.parse('http://10.0.2.2:5000/app_customization'));

  if (response.statusCode == 200) {
    String jsonString = response.body;
    dynamic decodedJson = jsonDecode('[' + jsonString + ']'); 
    jsonString = decodedJson[0];
 
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