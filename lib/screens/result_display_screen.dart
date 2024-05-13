import 'package:flutter/material.dart';

class ResultDisplayScreen extends StatelessWidget {
  final String result;

  ResultDisplayScreen({required this.result});

  @override
  Widget build(BuildContext context) {
    Widget imageWidget = Container(); // Default empty container
    if (result == 'Armflapping') {
      imageWidget = Image.asset(
        'images/armflipping.png',
        width: 500, // Adjust width as needed
        height: 500, // Adjust height as needed
      );
    } else if (result == 'Headbanging') {
      imageWidget = Image.asset(
        'images/headbanging.png',
        width: 500, // Adjust width as needed
        height: 500, // Adjust height as needed
      );
    } else if (result == 'Spinning') {
      imageWidget = Image.asset(
        'images/Spinning.png',
        width: 500, // Adjust width as needed
        height: 500, // Adjust height as needed
      );
    }

    return Scaffold(
      appBar: AppBar(title: Text('Result')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Classification Result:',
              style: TextStyle(fontSize: 30, fontWeight: FontWeight.bold), // Increased font size
            ),
            // SizedBox(height: 20),
            // Text(
            //   result,
            //   style: TextStyle(fontSize: 24), // Increased font size
            // ),
            SizedBox(height: 25),
            imageWidget, // Display the image based on the result
          ],
        ),
      ),
    );
  }
}
