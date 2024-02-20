import cv2
import mediapipe as mp
import pyautogui
import tkinter as tk
from PIL import Image, ImageTk
import sys


class Gui:
    def __init__(self): 
        self.root = tk.Tk()
        self.root.title("Hand Scroll app")
        self.root.configure(bg="#000000")
        self.root.geometry("700x1200")
        self.label = tk.Label(self.root, text="Hand Scroll", font=('San Francisco', 27), foreground='white', background='black')
        self.label.pack(padx=10, pady=10)
        self.label = tk.Label(self.root, text="Show an open RIGHT hand to camera to scroll down\n Make a RIGHT hand a fist and hide a thumb to scroll down", font=('San Francisco', 20), foreground='white', background='black')
        self.label.pack(padx=5, pady=5)
        self.label = tk.Label(self.root, text="Show an open LEFT hand to zoom\n Make a LEFT hand a fist and hide a thumb to zoom-", font=('San Francisco', 20), foreground='white', background='black')
        self.label.pack(padx=5, pady=5)
        self.label = tk.Label(self.root, text="by matela", font=('San Francisco', 15), foreground='white', background='black')
        self.label.place(relx=1, rely=1, anchor='se')
        self.label = tk.Label(self.root)
        self.label.pack(padx=10, pady=10)
        self.cap = cv2.VideoCapture(0)
        self.SCROLL_SPEED = 100
        self.ZOOM_SPEED = 25
        self.HAND_OPEN_THRESHOLD = 0.01
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.button = tk.Button(self.root, text="Quit", foreground='white', command=self.quit, background='red', font=('San Francisco', 27))
        self.button.pack()
        self.is_running = True
        self.button = tk.Button(self.root, text="Start", foreground='white', command=self.start_stop, background='blue', font=('San Francisco', 27))
        self.button.pack()
        self.button.pack()
        self.root.after(10, self.update_frame)
        self.root.mainloop()        
    def start_stop(self):
        if self.is_running:
            self.stop()
        else:
            self.start()

    def start(self):
        self.cap = cv2.VideoCapture(0)
        self.is_running = True
        self.button.config(text="Stop")
        self.update_frame()

    def stop(self):
        self.is_running = False
        if self.cap.isOpened():
            self.cap.release()
        self.button.config(text="Start")

    def update_frame(self):
        if not self.is_running:
            return
        ret, frame = self.cap.read()
        if not ret:
            return
        frame = cv2.flip(frame, 1) 
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                handedness = results.multi_handedness[idx].classification[0].label  # 'Left' or 'Right'
                #print(f'Handedness: {handedness}')  # prints 'Left' or 'Right'
                if handedness == 'Right':
                    index_finger = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    thumb = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                    distance = (index_finger.x - thumb.x) + (index_finger.y - thumb.y)
                    if distance >= self.HAND_OPEN_THRESHOLD:
                        pyautogui.scroll(self.SCROLL_SPEED)
                    else:
                        pyautogui.scroll(-self.SCROLL_SPEED)
                    self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                elif handedness == 'Left':
                    index_finger = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    thumb = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                    distance = (index_finger.x - thumb.x) + (index_finger.y - thumb.y)
                    if distance >= self.HAND_OPEN_THRESHOLD:
                        pyautogui.keyDown('ctrl')
                        pyautogui.scroll(-self.ZOOM_SPEED)
                        pyautogui.keyUp('ctrl')
                    else:
                        pyautogui.keyDown('ctrl')
                        pyautogui.scroll(self.ZOOM_SPEED)
                        pyautogui.keyUp('ctrl')
                    self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)
        self.root.after(10, self.update_frame)
    def quit(self):
        sys.exit()

Gui()