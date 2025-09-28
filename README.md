
# Smart Home Control Panel

This project is a **Smart Home Control Panel** GUI built with **PyQt5**. It provides a foundation for managing home security components such as alarms, sensors, and cameras.

## Overview

The GUI is designed with a modern, dark-themed, full-screen interface. It is modular, object-oriented, and ready to integrate additional features such as live camera preview, sensor input, and home layout visualization.

### Current Features

- **Full-Screen Interface**  
  Modern gradient background with clean layouts.

- **Top Bar**  
  - Digital clock.
  - Panel title.
  - Status icons for Wi-Fi, Battery, and User.

- **Middle Grid Layout (2x2)**  
  - **Camera Card (top-left)**: Placeholder black box for future camera preview.  
  - **Alarm Card (top-right)**:
    - Displays alarm status (Active/Inactive).
    - Toggle button to activate/deactivate the alarm.
    - Alarm deactivation requires PIN entry.
    - Flashing effect when alarm is active.
  - **Map / Home Layout Card (bottom-left)**: Placeholder for home plan / sensor positions.
  - **System Info Card (bottom-right)**: Displays panel status (Alarm active / inactive).

- **Interactive NumPad Dialog**  
  For PIN entry when disabling the alarm. Supports backspace and maximum 8 digits.

- **Alarm Logic**  
  - Alarm can be turned **ON without a PIN**.  
  - Alarm can be turned **OFF only with correct PIN**.  
  - Visual feedback (color and border changes) when alarm is active.

### Project Structure



mainscreen.py # Main GUI application


### Technologies Used

- **Python 3**
- **PyQt5** for GUI
- Object-oriented programming for modularity and maintainability.

### Future Plans

- Integrate **live camera feed** in the Camera card.
- Connect with **sensors** and YOLO-based human detection.  
  - Display alerts when movement is detected in specific rooms.
- Implement dynamic **home layout visualization** in the Map card.
- Extend alarm system to handle multiple input sources and notifications.

### How to Run

1. Install required packages:

```bash
pip install pyqt5
```

