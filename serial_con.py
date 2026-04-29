import serial
import time

SERIAL_PORT = "COM6"
BAUD_RATE = 9600

# 打开串口
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)

# finger_state:
# "close" -> 弯曲 / 10°
# "open"  -> 伸直 / 90°
COMMAND_MAP = {
    1: {
        "close": "1",
        "open": "q"
    },
    2: {
        "close": "2",
        "open": "w"
    },
    3: {
        "close": "3",
        "open": "e"
    },
    4: {
        "close": "4",
        "open": "r"
    }
}


def control_finger(finger, finger_state):
    """
    控制不同手指的开合状态

    finger:
        1, 2, 3, 4

    finger_state:
        "open"  表示伸直
        "close" 表示弯曲
    """

    if finger not in COMMAND_MAP:
        print("Invalid finger. Use 1, 2, 3, or 4.")
        return

    if finger_state not in COMMAND_MAP[finger]:
        print('Invalid finger_state. Use "open" or "close".')
        return

    cmd = COMMAND_MAP[finger][finger_state]

    ser.write(cmd.encode())
    print(f"Sent: finger={finger}, state={finger_state}, command={cmd}")

    time.sleep(0.1)

    while ser.in_waiting:
        response = ser.readline().decode(errors="ignore").strip()
        if response:
            print("Arduino:", response)


def close_serial():
    ser.close()