import time
import ctypes
from ctypes import wintypes


def main():
    print("Mova o mouse para o local desejado.")
    print("Pressione Ctrl+C para parar.")
    print()

    point = wintypes.POINT()

    try:
        while True:
            ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
            print(f"Posicao real do mouse: x={point.x}, y={point.y}", end="\r")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\nFinalizado.")


if __name__ == "__main__":
    main()
