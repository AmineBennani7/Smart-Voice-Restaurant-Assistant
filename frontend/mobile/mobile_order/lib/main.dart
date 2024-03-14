import 'package:flutter/material.dart';
import 'package:mobile_order/pages/conversation_page.dart';
import 'package:mobile_order/pages/info_page.dart';
import 'package:mobile_order/pages/intro_page.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});



  @override 
  Widget build(BuildContext context){
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: const IntroPage(),
      routes: {
        '/intropage': (context) => const IntroPage(),
        '/infopage': (context) => const InfoPage(),
        '/conversationpage': (context) => const ConversationPage(),
      
    },
  );
}
}
