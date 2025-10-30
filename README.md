## THIS PROJECT IS STILL IN DEVELOPMENT



## Installation

To install and run this project, follow these steps:

### Steps

1.  **Install needed pip**
    ```bash
    pip install flask
    pip install opencv-python
    pip install cvzone
    pip install numpy
2. **File structure**
   ```bash
   project-root/
    ├── static/
    │   └── style.css
    ├── templates/
    │   └── index.html
    ├── carParkImg.png (your parking space img)
    ├── CarParkPos
    ├── main.py (anyname you want)
    └── ParkingSpacePicker.py
3. **How to run and make all the devices that use the same internet**
   ```bash
   in Command Prompt
   //cd to your folder EX: (cd Desktop\project-root)
   set FLASK_APP=main.py
   flask run --host=0.0.0.0
