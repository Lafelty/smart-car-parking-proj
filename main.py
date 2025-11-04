from flask import Flask, render_template, Response, jsonify
import cv2, pickle, cvzone, numpy as np

app = Flask(__name__)

# Load parking positions
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 107, 48
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)  # second camera if available


def checkParkingSpace(imgPro, img):
    spaceCounter = 0
    for pos in posList:
        x, y = pos
        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)
        color = (0, 255, 0) if count < 900 else (0, 0, 255)
        thickness = 5 if count < 900 else 2
        if count < 900:
            spaceCounter += 1
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3),
                           scale=1, thickness=2, offset=0, colorR=color)
    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50),
                       scale=3, thickness=5, offset=20, colorR=(0, 200, 0))
    return img, spaceCounter


def generate_frames(cam):
    while True:
        success, img = cam.read()
        if not success:
            break
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
        imgThreshold = cv2.adaptiveThreshold(
            imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 25, 16
        )
        imgMedian = cv2.medianBlur(imgThreshold, 5)
        kernel = np.ones((3, 3), np.uint8)
        imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

        imgProcessed, _ = checkParkingSpace(imgDilate, img)
        ret, buffer = cv2.imencode('.jpg', imgProcessed)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def home():
    return render_template('index.html', title="Smart Parking System")


@app.route('/camera2')
def camera2():
    return render_template('camera2.html', title="Camera 2 View")


@app.route('/about')
def about():
    return render_template('about.html', title="About System")


@app.route('/video')
def video():
    return Response(generate_frames(cap1),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video2')
def video2():
    return Response(generate_frames(cap2),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/status')
def status():
    return jsonify({"message": "Hello, T.Felix!"})


if __name__ == "__main__":
    app.run(debug=True)
