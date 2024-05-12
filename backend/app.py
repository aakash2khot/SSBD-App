import os
from flask import Flask, request, jsonify
from flask_cors import CORS 
from pipeline import detect_actions

app = Flask(__name__)
CORS(app)

def save_uploaded_file(file):
    file_path = os.path.join(os.getcwd(), file.filename)
    file.save(file_path)
    return file_path

@app.route('/classify', methods=['POST'])
def classify_video():
    try:
        print("Received request")
        
        # Receive video file from Flutter app
        if 'video' not in request.files:
            print("No video file provided")
            return jsonify({'message': 'No video file provided'}), 400

        video_file = request.files['video']
        if video_file.filename == '':
            print("Empty video file name")
            return jsonify({'message': 'Empty video file name'}), 400

        # Save the video file
        video_path = save_uploaded_file(video_file)
        print(f"Video saved at: {video_path}")

        # Call the function from pipeline.py to detect actions
        result = detect_actions(video_path)

        print("Actions detected")

        return result, 200
    except Exception as e:
        print(f"Error processing video: {str(e)}")
        return jsonify({'message': f'Error processing video: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
