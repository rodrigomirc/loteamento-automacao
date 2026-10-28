import pyautogui
import time

print("Mova o mouse para cada botão/campo e anote as coordenadas.")
print("Pressione Ctrl+C para parar.")

try:
    while True:
        x, y = pyautogui.position()
        print(f"x={x}, y={y}", end="\r")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nFinalizado.")
