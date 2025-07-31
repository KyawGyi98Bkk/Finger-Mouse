# Finger-Mouse

This project provides a simple implementation to control your mouse using finger gestures detected via your webcam.

## Features

- **Move Cursor**: the index finger tip position controls the mouse cursor.
- **Left Click**: touching the thumb and index finger tips performs a left click.
- **Right Click**: making a fist triggers a right click.

## Requirements

- Python 3.8+
- `opencv-python`
- `mediapipe`
- `pyautogui`

Install dependencies using:

```bash
pip install opencv-python mediapipe pyautogui
```

## Usage

Run the script:

```bash
python finger_mouse.py
```

Press `Esc` to exit the program.

## Notes

The script captures video from your default webcam and requires accessibility permissions to control the mouse. Ensure these permissions are granted on your operating system.
