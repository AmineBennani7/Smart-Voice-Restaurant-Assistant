import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:mobile_order/components/button_info.dart';



class InfoPage extends StatelessWidget {
  const InfoPage({super.key});

   @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor:const  Color.fromARGB(255, 252, 252, 242),
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
                  "Instrucciones : ",
                  style: GoogleFonts.kanit(
                    fontSize: 30, // Ajusta el tamaño de fuente según necesites
                    fontWeight: FontWeight.bold,
                    color: Colors.black,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
            ),

           // MINI LOGO Y TEXTO A SU DERECHA
            Padding(
              padding: const EdgeInsets.only(top: 40.0), // Ajusta según sea necesario
              child: Row(
                children: [
                  Image.asset(
                    'lib/images/chatbot2.png', // Asegúrate de que la ruta al mini logo es correcta
                    width: 80.0, // Ajusta según tus necesidades
                    height: 80.0, // Ajusta según tus necesidades
                  ),
                  const SizedBox(width: 10), // Espacio entre el logo y el texto
                  Expanded( // Asegura que el texto no se desborde
                    child: Text(
                      "Interactúa de forma natural con nuestro chatbot, utilizando tu voz para solicitar información sobre nuestros platos y hacer tus pedidos cómodamente.",
                      style: GoogleFonts.kanit(
                        fontSize: 16, // Ajusta el tamaño de fuente según necesites
                        color:const  Color.fromARGB(255, 44, 44, 44),
                      ),
                    ),
                  ),
                ],
              ),
            ),


            //TEXTO 2: 
             Padding(
              padding: const EdgeInsets.only(top: 50.0), // Ajusta según sea necesario
              child: Row(
                children: [
                  Image.asset(
                    'lib/images/tarjeta_credito.png', // Asegúrate de que la ruta al mini logo es correcta
                    width: 80.0, // Ajusta según tus necesidades
                    height: 80.0, // Ajusta según tus necesidades
                  ),
                  const SizedBox( width: 10), // Espacio entre el logo y el texto
                  Expanded( // Asegura que el texto no se desborde
                    child: Text(
                      "Después de realizar tu pedido, recibirás una notificación para proceder al pago en caja. Por el momento, no ofrecemos la opción de pago móvil.",
                      style: GoogleFonts.kanit(
                        fontSize: 16, // Ajusta el tamaño de fuente según necesites
                        color:const  Color.fromARGB(255, 44, 44, 44),
                      ),
                    ),
                  ),
                ],
              ),
            ),

            
              //TEXTO 3: 
             Padding(
              padding: const EdgeInsets.only(top: 50.0), // Ajusta según sea necesario
              child: Row(
                children: [
                  Image.asset(
                    'lib/images/spaguetti.png', // Asegúrate de que la ruta al mini logo es correcta
                    width: 80.0, // Ajusta según tus necesidades
                    height: 80.0, // Ajusta según tus necesidades
                  ),
                  const SizedBox(width: 10), // Espacio entre el logo y el texto
                  Expanded( // Asegura que el texto no se desborde
                    child: Text(
                      "Finalmente espera mientras preparamos y servimos tus deliciosos platos que has pedido.",
                      style: GoogleFonts.kanit(
                        fontSize: 16, // Ajusta el tamaño de fuente según necesites
                        color:const  Color.fromARGB(255, 44, 44, 44),
                      ),
                    ),
                  ),
                ],
              ),
            ),

              //Boton 
         const  Padding(
           padding:  EdgeInsets.only(top: 120.0), 
            child: Center(
              child: myButtonInfo(text: "EMPEZAR A PEDIR"),
            ),
          
          ),


          ],
        ),
      ),
    );
  }
}