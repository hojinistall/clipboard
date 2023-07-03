import tkinter as tk
import pyautogui
from PIL import ImageGrab


def capture_screen():
    root = tk.Tk()
    root.attributes('-alpha', 0.5)  # 창의 투명도를 조정합니다.
    root.attributes('-topmost', True)  # 창을 항상 맨 위에 띄웁니다.
    root.attributes('-fullscreen', True)  # 창을 전체화면으로 설정합니다.

    canvas = tk.Canvas(root, bg='white')
    canvas.pack(expand=True, fill='both')
 
    # 전역 변수로 x_pos와 y_pos를 초기화합니다.
    x_start = 0
    y_start = 0
    rect_id = 0  # 이전에 그린 사각형의 ID 값을 저장할 변수입니다.

    # 마우스 이벤트를 바인딩합니다.
    def on_left_button_down(event):
        global x_start, y_start,rect_id
        rect_id = None
        x_start, y_start = pyautogui.position()
        print("시작 윈도우 위치:", pyautogui.position())


    def on_left_button_drag(event):
        global x_start, y_start,rect_id
        
        if rect_id is not None:
             canvas.delete(rect_id)  # 이전에 그린 사각형을 지웁니다.

        rect_id = canvas.create_rectangle(
            x_start, y_start, pyautogui.position(), outline='red', width=5, dash=(4,))
        
        print("드래그 윈도우 위치:", pyautogui.position())
        


    def on_left_button_up(event):
        global x_start, y_start

        x_end,y_end = pyautogui.position()
        root.withdraw()  # 화면에서 창을 숨깁니다.
        print("마지막 윈도우 위치:", pyautogui.position())
        # 캡쳐할 영역을 계산합니다.
        capture_region = (x_start, y_start, x_end, y_end)

        # 지정한 영역을 캡쳐합니다.
        screenshot = ImageGrab.grab(capture_region)

        screenshot.show()

        # 캡쳐한 이미지를 파일로 저장합니다.
        # screenshot.save("./capture6.png")

        root.destroy()

    canvas.bind('<Button-1>', on_left_button_down)
    canvas.bind('<B1-Motion>', on_left_button_drag)
    canvas.bind('<ButtonRelease-1>', on_left_button_up)

    root.mainloop()


if __name__ == '__main__':
    capture_screen()
