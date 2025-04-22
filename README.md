# Controlling_video_using_eye_gestures
# Hand and Blink Gesture Control for YouTube (Chrome)

This project uses **MediaPipe**, **OpenCV**, and **PyAutoGUI** to control YouTube video playback on Chrome using **hand gestures** and **blink detection**.

## Features

- **Blink Detection**
  - Blink once to toggle **play/pause** on a YouTube video.
  
- **Hand Gesture Control**
  - Raise 1 finger → **Volume Up**
  - Raise 2 fingers → **Volume Down**
  - Raise 3 fingers → **Skip Forward**
  - Raise 4 fingers → **Skip Backward**

## Tech Stack

- OpenCV
- MediaPipe
- PyAutoGUI
- Python 3.x

## Installation

```bash
pip install opencv-python mediapipe pyautogui
Usage
Open a YouTube video in Chrome.
python gesture_control.py
Blink or use hand gestures to control the video.
Ensure good lighting for better detection.

Make sure Chrome is the active window.

Gestures have a 1-second cooldown to avoid accidental triggers.
