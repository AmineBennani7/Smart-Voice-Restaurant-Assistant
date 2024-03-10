import 'package:flutter/material.dart';
class ConversationPage extends StatelessWidget {
  const ConversationPage({super.key});

   @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor:const Color.fromARGB(255, 252, 252, 242),
      body: 
      
      //Logo pequeño
      Padding(
        padding: const EdgeInsets.all(40.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.start, // Ajustado para alinear contenido al inicio
          children: [
            Center(
              child: Padding(
                padding: const EdgeInsets.only(top:70.0, bottom: 0.0), // Ajusta estos valores según necesites
                child: Image.asset(
                  'lib/images/pizza.png',
                  width: 70.0, // Ajusta el ancho según tus necesidades
                  height: 60.0, // Ajusta la altura según tus necesidades
                  fit: BoxFit.contain,
                ),
              ),
            ),
          ])));
          }}