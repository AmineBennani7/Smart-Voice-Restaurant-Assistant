import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:mobile_order/components/button_intro.dart';

class IntroPage extends StatelessWidget {
  const IntroPage({super.key});

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

        //TITULO PRINCIPAL

            Padding(
              padding: const EdgeInsets.only(top: 20.0), // Reduce el espacio arriba del texto
              child: Center(
                child: Text(
                  "Te damos la bienvenida a PizzaUs",
                  style: GoogleFonts.kanit(
                    fontSize: 30, // Ajusta el tamaño de fuente según necesites
                    fontWeight: FontWeight.bold,
                    color: Colors.black,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
            ),

    //SUBTITULO
            Padding(
              padding: const EdgeInsets.only(top: 20.0), // Espacio después del texto de bienvenida
              child: Center(
                child: Text(
                  "Aplicación para ordenar tu comida  y pedir información rápidamente hablando con nuestro asistente virtual sin la necesidad de hacer cola. ", // Aquí va tu texto secundario
                  style: GoogleFonts.kanit(
                    color: Colors.grey, // Color gris para el texto
                    fontSize: 16, // Ajusta el tamaño de fuente según tus necesidades
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
            ),

     //IMAGEN     
     // Padding(
            Padding(
               padding: const EdgeInsets.only(top: 60.0), 
               child: Center(
              child: Image.asset(
                'lib/images/caja-de-pizza.png',
                width: 220.0,
                height: 299.0,
                fit: BoxFit.contain,
              ),
            ),
        ),


        //Boton 
         const Padding(
           padding:  EdgeInsets.only(top: 120.0), 
            child: Center(
              child: MyButton(text: "EMPEZAR"),
            ),
          
          ),

          ]
        ) , 
        
        
  ),

    );


      
           
    
  }
}
