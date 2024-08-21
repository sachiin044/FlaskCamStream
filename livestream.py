from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Initialize the camera
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

def generate_frames():
    while True:
        # Read the camera frame
        success, frame = camera.read()
        if not success:
            print("Failed to capture frame")
            break
        else:
            # Try to encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                print("Failed to encode frame")
                continue  # Skip this frame if encoding fails

            frame = buffer.tobytes()

            # Yield the frame in a format that can be displayed in the browser
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
