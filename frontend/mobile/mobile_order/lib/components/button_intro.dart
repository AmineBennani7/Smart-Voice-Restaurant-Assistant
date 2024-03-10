import 'package:flutter/material.dart';

class MyButton extends StatelessWidget{
  final String text; 
  const MyButton({ 
    super.key, 
    required this.text
  });


 @override 
 Widget build(BuildContext context){
   return InkWell(
      onTap: () {
        Navigator.pushNamed(context, '/infopage'); // Navegar a /infopage al tocar
      },
      child: Container(
        decoration: BoxDecoration(
          color: const Color.fromARGB(255, 222, 167, 72),
          borderRadius: BorderRadius.circular(40),
        ),
        padding:const EdgeInsets.all(20),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              text,
              style: const TextStyle(
                color:  Colors.white,
              ),
            ),
            const SizedBox(width: 10),
            //icon
            const Icon (Icons.arrow_forward, color: Colors.white)
          ],
        ),
      ),
    );
  }
}