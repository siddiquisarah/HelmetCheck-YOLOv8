import sys, os
from ultralytics import YOLO
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QStackedWidget,QDesktopWidget
from PyQt5.QtGui import QFont, QMovie, QFontDatabase, QPixmap, QImage
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QTimer, QSize
import cv2, cvzone, math, time

class ButtonHandler(QObject):
    switchMode = pyqtSignal()

button_handler = ButtonHandler()  # Create a global instance of ButtonHandler

number1 = 0

def stop_button_clicked():
    sys.exit()

def create_left_part():
    left_part = QWidget()
    left_part.setStyleSheet(
        "background-color: #171717;"
        "border: 5px solid #09DC8F;"  # Add a 5px bright green border
    )
    left_part.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    left_layout = QVBoxLayout(left_part)
    left_layout.setContentsMargins(0, 0, 0, 0) 
    return left_part

def create_right_part():

    global number1

    right_part = QWidget()
    right_part.setStyleSheet("background-color: black;")
    right_part.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    stacked_widget = QStackedWidget(right_part)

    font_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "JosefinSans-Medium.ttf")
    font_id = QFontDatabase.addApplicationFont(font_file_path)
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

    # Panel 1
    panel1 = QWidget()
    panel1.setStyleSheet("background-color: #04161a; color: #fa893e;")
    panel1_layout = QVBoxLayout(panel1)
    panel1_layout.addStretch(1)

    alert_icon = QPixmap("../assets/alert.png").scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    alert_icon_label = QLabel()
    alert_icon_label.setPixmap(alert_icon)
    alert_icon_label.setAlignment(Qt.AlignHCenter)
    panel1_layout.addWidget(alert_icon_label)

    panel1_layout.addStretch(1)

    label_panel1 = QLabel("NO HARD HAT")
    font = QFont(font_family, 20, 400)
    font.setLetterSpacing(QFont.AbsoluteSpacing, 7)
    label_panel1.setFont(font)
    label_panel1.setAlignment(Qt.AlignHCenter)  # Align the text horizontally in the center
    panel1_layout.addWidget(label_panel1)
    
    label_panel1a = QLabel("DETECTED")
    font1a = QFont(font_family, 20, 400)
    font1a.setLetterSpacing(QFont.AbsoluteSpacing, 7)
    label_panel1a.setFont(font1a)
    label_panel1a.setAlignment(Qt.AlignHCenter)  # Align the text horizontally in the center
    panel1_layout.addWidget(label_panel1a)
    panel1_layout.addStretch(1) 

    # Create a QLabel to display the dynamic text
    dynamic_text_label = QLabel()
    dynamic_text_label.setStyleSheet("font-family: font_family; color: white; font-size: 14px; letter-spacing: 5px;")
    dynamic_text_label.setAlignment(Qt.AlignHCenter)  # Align the text horizontally in the center
    panel1_layout.addWidget(dynamic_text_label)

    panel1_layout.addStretch(1) 

    # Function to update the dynamic text
    def update_dynamic_text():
        text = f"CLEARED: <span style='color:#fa893e; font-size:19px; font-family: font_family;'>{number1}</span>"
        dynamic_text_label.setText(text)

    # # Sample values for number1 and number2 (you can replace these with your actual dynamic variables)
    # number1 = 10
    # number2 = 3
    update_dynamic_text()

    button_layout = QVBoxLayout()
    stop_button = QPushButton("TERMINATE")
    font1b = QFont(font_family, 13, 600)
    font1b.setLetterSpacing(QFont.AbsoluteSpacing, 3)
    stop_button.setFont(font1b)
    stop_button.setStyleSheet(
        "background-color: #bf6930; color: white; font-family: font_family; border: 2px solid #bf6930;"
        "border-radius: 24px;"
        "padding: 12px 20px"
    )
    stop_button.clicked.connect(stop_button_clicked)

    timer = QTimer()
    def switch_to_panel1():
        stacked_widget.setCurrentIndex(0)
        timer.stop()  # Stop the timer when switching to Panel 1
    timer.timeout.connect(switch_to_panel1)

    def on_success_button_clicked():
        global number1
        number1 += 1 
        update_dynamic_text()
        stacked_widget.setCurrentIndex(1)
        timer.start(3000)  # Start the timer when success_button is clicked
        #button_handler.switchMode.emit()  # Emit the switchMode signal

    button_handler.switchMode.connect(on_success_button_clicked)

    #stop_button.clicked.connect(on_success_button_clicked)
    stop_button.setFixedWidth(220)
    button_layout.addWidget(stop_button)  # Set the stretch factor to 2 (narrower)
    button_layout.setAlignment(Qt.AlignHCenter)
    button_layout.setContentsMargins(0, 0, 0, 0)

    panel1_layout.addLayout(button_layout)
    panel1_layout.addStretch(1) 

    # Panel 3
    panel3 = QWidget()
    panel3.setStyleSheet("background-color: #04161a; color: #09DC8F;")
    panel3_layout = QVBoxLayout(panel3)
    panel3_layout.addStretch(2) 
    tick_image = QPixmap("../assets/tick.png").scaled(130, 130, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    tick_label = QLabel()
    tick_label.setPixmap(tick_image)
    tick_label.setAlignment(Qt.AlignHCenter)
    panel3_layout.addWidget(tick_label)
    panel3_layout.addStretch(1) 
    label_panel3 = QLabel("CLEARED")
    font3 = QFont(font_family, 22, 400)
    font3.setLetterSpacing(QFont.AbsoluteSpacing, 10)
    label_panel3.setFont(font3)
    label_panel3.setAlignment(Qt.AlignHCenter)  # Align the text horizontally in the center
    panel3_layout.addWidget(label_panel3)
    panel3_layout.addStretch(1)
    clear_text_line1 = QLabel("HARD HAT DETECTED")
    custom_font3 = QFont(font_family, 13)
    custom_font3.setLetterSpacing(QFont.AbsoluteSpacing, 4) # letter spacing = 5
    clear_text_line1.setFont(custom_font3)
    clear_text_line1.setStyleSheet("color: white;")
    clear_text_line1.setAlignment(Qt.AlignHCenter)
    panel3_layout.addWidget(clear_text_line1)
    panel3_layout.addStretch(4) 

    stacked_widget.addWidget(panel1)
    stacked_widget.addWidget(panel3)
    stacked_widget.setCurrentIndex(0)   # Show Panel 1 initially

    right_layout = QVBoxLayout(right_part)
    right_layout.setContentsMargins(0, 0, 0, 0)  # Set margins to zero
    right_layout.addWidget(stacked_widget)

    return right_part

if __name__ == "__main__":
    # Create the application object
    app = QApplication(sys.argv)
    window = QWidget()

    window.setWindowTitle("Hard Hat Detection")
    window.showMaximized()

    left_part = create_left_part()
    right_part = create_right_part()

    video_label = QLabel()
    video_label.setAlignment(Qt.AlignHCenter)
    video_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
    video_label.setMinimumSize(1, 1)

    windowLayout = QHBoxLayout()
    windowLayout.setContentsMargins(0, 0, 0, 0)  # Set margins to zero for the window layout
    windowLayout.setSpacing(0)  # Set spacing between widgets to zero
    #windowLayout.addWidget(left_part, 1)  # Set the left part to take 70% of the window width
    windowLayout.addWidget(video_label, 7)
    windowLayout.addWidget(right_part, 3)  # Set the right part to take 30% of the window width
    window.setLayout(windowLayout)

    window.show()

    # cap = cv2.VideoCapture(0)  # For Webcam
    # cap.set(3, 1280)
    # cap.set(4, 720)
    cap = cv2.VideoCapture("../Videos/20230725180126_1818.mp4")  # For Video

    model = YOLO("ppe.pt")
    classNames = ['Hardhat', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest', 'Person', 'Safety Cone','Safety Vest', 'machinery', 'vehicle']
    myColor = (0, 0, 255)
    prev_frame_time = 0
    new_frame_time = 0
    object_detected = False

    while True:
        new_frame_time = time.time()
        success, img = cap.read()
        results = model(img, stream=True)
        hardhat_detected = False

        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                conf = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])
                currentClass = classNames[cls]

                if conf>0.5:
                    cls = int(box.cls[0])
                    currentClass = classNames[cls]
                
                    if currentClass == 'Hardhat':
                        #print("Hard hat detected")
                        button_handler.switchMode.emit()
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
                        cvzone.putTextRect(img, f'{currentClass} {conf}',
                                       (max(0, x1), max(35, y1)), scale=1, thickness=1, colorB=(0, 255, 0),
                                       colorT=(255, 255, 255), colorR=(0, 255, 0), offset=5)
                        
        # Convert the OpenCV video frame to QImage
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        q_img = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()

        # Set the QImage as the pixmap of the video label
        scaled_pixmap = QPixmap.fromImage(q_img).scaledToWidth(video_label.width(), Qt.SmoothTransformation)
        video_label.setPixmap(scaled_pixmap)
                        
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        #cv2.imshow("Image", img)
        cv2.waitKey(1)
          

    sys.exit(app.exec_())
