import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:mobile_order/components/button_intro.dart';

class IntroPage extends StatelessWidget {
  const IntroPage({Key? key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromARGB(255, 252, 252, 242),
      body: SingleChildScrollView( //RESPONSIVE
        child: Padding(
          padding: const EdgeInsets.all(40.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              SizedBox(height: 70.0),
              Image.asset(
                'lib/images/pizza.png',
                width: 70.0,
                height: 60.0,
                fit: BoxFit.contain,
              ),
              SizedBox(height: 20.0),
              Text(
                "Te damos la bienvenida a PizzaUs",
                style: GoogleFonts.kanit(
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
              Image.asset(
                'lib/images/caja-de-pizza.png',
                width: MediaQuery.of(context).size.width * 0.6, //PARA VOLVERLO RESPONSIVE
                height: MediaQuery.of(context).size.height * 0.3,
                fit: BoxFit.contain,
              ),
              SizedBox(height: 120.0),
              Center(
                child: MyButton(text: "EMPEZAR"),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
