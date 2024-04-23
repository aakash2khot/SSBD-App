import 'package:flutter/material.dart';
import 'upload_screen.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Classify_Behaviour',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: UploadScreen(), // Navigate directly to UploadScreen
    );
  }
}
