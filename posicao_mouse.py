import time

import pyautogui


def main():
    print("Mova o mouse para o local desejado.")
    print("Pressione Ctrl+C para parar.")
    print()

    try:
        while True:
            x, y = pyautogui.position()
            print(f"Posicao do mouse: x={x}, y={y}", end="\r")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\nFinalizado.")


if __name__ == "__main__":
    main()
