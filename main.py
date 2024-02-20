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
        self.root.geometry("600x1000")
        self.label = tk.Label(self.root, text="Hand Scroll", font=('San Francisco', 27), foreground='white', background='black')
        self.label.pack(padx=10, pady=10)
        self.label = tk.Label(self.root, text="Show an open hand to camera to scroll down\n Make a fist and hide a thumb to scroll down", font=('San Francisco', 20), foreground='white', background='black')
        self.label.pack(padx=5, pady=5)
        self.label = tk.Label(self.root, text="by matela", font=('San Francisco', 15), foreground='white', background='black')
        self.label.place(relx=1, rely=1, anchor='se')
        self.label = tk.Label(self.root)
        self.label.pack(padx=10, pady=10)
        self.cap = cv2.VideoCapture(0)
        self.SCROLL_SPEED = 100
        self.HAND_OPEN_THRESHOLD = 0.01
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.button = tk.Button(self.root, text="Quit", foreground='white', command=self.quit, background='red', font=('San Francisco', 27))
        self.button.pack()
        self.root.after(10, self.update_frame)
        self.root.mainloop()

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index_finger = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                distance = (index_finger.x - thumb.x) + (index_finger.y - thumb.y)
                if distance >= self.HAND_OPEN_THRESHOLD:
                    pyautogui.scroll(self.SCROLL_SPEED)
                else:
                    pyautogui.scroll(-self.SCROLL_SPEED)
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