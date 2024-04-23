// import 'package:flutter/material.dart';
// import 'package:http/http.dart' as http;
// import 'package:file_picker/file_picker.dart';
// import 'result_display_screen.dart'; // Import the result display screen
// import 'loading_screen.dart'; // Import the loading screen

// class UploadScreen extends StatefulWidget {
//   @override
//   _UploadScreenState createState() => _UploadScreenState();
// }

// class _UploadScreenState extends State<UploadScreen> {
//   bool _loading = false;

//   Future<void> _uploadVideo(BuildContext context) async {
//     setState(() {
//       _loading = true;
//     });

//     try {
//       var url = Uri.parse('http://172.16.132.165:8000/classify'); // Update with your backend URL

//       // Pick the video file
//       FilePickerResult? result = await FilePicker.platform.pickFiles(
//         type: FileType.video,
//         allowCompression: true,
//       );

//       if (result != null) {
//         // Get the file bytes
//         List<int> fileBytes = result.files.single.bytes!;

//         // Create a multipart request
//         var request = http.MultipartRequest('POST', url);

//         // Attach the video file to the request
//         request.files.add(http.MultipartFile.fromBytes('video', fileBytes, filename: 'video.mp4'));

//         // Send the request and wait for the response
//         var streamedResponse = await request.send();

//         // Read and decode the response
//         var response = await http.Response.fromStream(streamedResponse);

//         if (response.statusCode == 200) {
//           // Navigate to result display screen with the classification result
//           Navigator.push(
//             context,
//             MaterialPageRoute(builder: (context) => ResultDisplayScreen(result: response.body)),
//           );
//         } else {
//           ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Failed to upload video: ${response.reasonPhrase}')));
//         }
//       } else {
//         ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('No video file selected')));
//       }
//     } catch (e) {
//       ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error uploading video: $e')));
//     } finally {
//       setState(() {
//         _loading = false;
//       });
//     }
//   }

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       appBar: AppBar(title: Text('SSBD -- APP')),
//       body: _loading
//           ? LoadingScreen() // Show loading screen while uploading
//           : Center(
//               child: Column(
//                 mainAxisAlignment: MainAxisAlignment.center,
//                 children: [
//                   Text(
//                     'To classify the video into self-stimulator actions, please upload your video here',
//                     textAlign: TextAlign.center,
//                     style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
//                   ),
//                   SizedBox(height: 20),
//                   ElevatedButton(
//                     onPressed: () async {
//                       await _uploadVideo(context);
//                     },
//                     child: Text(
//                       'Upload Video',
//                       style: TextStyle(fontSize: 24),
//                     ),
//                   ),
//                 ],
//               ),
//             ),
//     );
//   }
// }
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:file_picker/file_picker.dart';
import 'result_display_screen.dart'; // Import the result display screen
import 'loading_screen.dart'; // Import the loading screen

class UploadScreen extends StatefulWidget {
  @override
  _UploadScreenState createState() => _UploadScreenState();
}

class _UploadScreenState extends State<UploadScreen> {
  bool _loading = false;

  Future<void> _uploadVideo(BuildContext context) async {
    setState(() {
      _loading = true;
    });

    try {
      var url = Uri.parse('http://172.16.132.165:8000/classify'); // Update with your backend URL

      

      // Pick the video file
      FilePickerResult? result = await FilePicker.platform.pickFiles(
        type: FileType.video,
        allowCompression: true,
        withData: true,
      );
      


      if (result != null) {
        // Check if file bytes are empty
        if (result.files.isNotEmpty && result.files.first.bytes != null && result.files.first.bytes!.isNotEmpty) {
          // Get the file bytes
          List<int> fileBytes = result.files.single.bytes!;

          // Create a multipart request
          var request = http.MultipartRequest('POST', url);

          // Attach the video file to the request
          request.files.add(http.MultipartFile.fromBytes('video', fileBytes, filename: 'video.mp4'));

          // Send the request and wait for the response
          var streamedResponse = await request.send();

          // Read and decode the response
          var response = await http.Response.fromStream(streamedResponse);

          if (response.statusCode == 200) {
            // Navigate to result display screen with the classification result
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => ResultDisplayScreen(result: response.body)),
            );
          } else {
            ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Failed to upload video: ${response.reasonPhrase}')));
          }
        } else {
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('File bytes are empty')));
        }
      } else {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('No video file selected')));
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error uploading video: $e')));
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('SSBD -- APP')),
      body: _loading
          ? LoadingScreen() // Show loading screen while uploading
          : Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    'To classify the video into self-stimulator actions, please upload your video here',
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                  SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: () async {
                      await _uploadVideo(context);
                    },
                    child: Text(
                      'Upload Video',
                      style: TextStyle(fontSize: 24),
                    ),
                  ),
                ],
              ),
            ),
    );
  }
}
