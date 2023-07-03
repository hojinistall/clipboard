import tkinter as tk
import pyautogui
from PIL import ImageGrab, Image
import win32clipboard
from io import BytesIO
import os

# 캡쳐 영영을 만든다.


def capture_to_area(diallog):
    root = tk.Tk()
    root.attributes('-alpha', 0.5)  # 창의 투명도를 조정합니다.
    root.attributes('-topmost', True)  # 창을 항상 맨 위에 띄웁니다.
    root.attributes('-fullscreen', True)  # 창을 전체화면으로 설정합니다.

    canvas = tk.Canvas(root, bg='white')
    canvas.pack(expand=True, fill='both')

    rect_id = 0  # 이전에 그린 사각형의 ID 값을 저장할 변수입니다.

    # 마우스 이벤트를 바인딩합니다.
    def on_left_button_down(event):
        global x_start, y_start, rect_id
        rect_id = None
        x_start, y_start = pyautogui.position()
        #print("시작 윈도우 위치:", pyautogui.position())

    def on_left_button_drag(event):
        global x_start, y_start, rect_id

        if rect_id is not None:
            canvas.delete(rect_id)  # 이전에 그린 사각형을 지웁니다.

        rect_id = canvas.create_rectangle(
            x_start, y_start, pyautogui.position(), outline='red', width=5, dash=(4,))

        #print("드래그 윈도우 위치:", pyautogui.position())

    def on_left_button_up(event):
        global x_start, y_start, x_end, y_end

        try:
            x_end, y_end = pyautogui.position()
            root.withdraw()  # 화면에서 창을 숨깁니다.
        
            #print("마지막 윈도우 위치:", pyautogui.position())
            # 캡쳐할 영역을 계산합니다.

            # x_start가 x_end보다 클 때 값을 바꿔줍니다.
            if x_start > x_end:
                x_start, x_end = x_end, x_start

            # y_start가 y_end보다 클 때 값을 바꿔줍니다.
            if y_start > y_end:
                y_start, y_end = y_end, y_start

            capture_region = (x_start, y_start, x_end, y_end)

            strPosition = "캡쳐영역 ["+str(x_start) + "," + str(y_start) + "," + str(x_end) + "," + str(y_end) + " ]"
            makePositionLabel(diallog, strPosition)
            # 지정한 영역을 캡쳐합니다.
            screenshot = ImageGrab.grab(capture_region)

            #screenshot.show()
            # 캡쳐한 이미지를 파일로 저장합니다.
            # screenshot.save("./capture6.png")

            root.destroy()
        except Exception as e:
            makeAlertLabel(diallog, "영역 설정 중 에러 발생")

    canvas.bind('<Button-1>', on_left_button_down)
    canvas.bind('<B1-Motion>', on_left_button_drag)
    canvas.bind('<ButtonRelease-1>', on_left_button_up)
    root.mainloop()
#캡쳐해서 클립보드에 넣는다.


def capture_to_clipboard():
    global x_start, y_start, x_end, y_end

    try:
        # 캡쳐할 영역을 지정합니다. (x, y, width, height)
        capture_region = (x_start, y_start, x_end, y_end)

        # 지정한 영역을 캡쳐합니다.
        screenshot = ImageGrab.grab(capture_region)

        # 클립보드에 이미지를 복사합니다.
        output = BytesIO()
        screenshot.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        #print("캡쳐 스크린 성공")
        makeProcessLabel(root, "캡쳐 성공!")
    except Exception as e:
        makeAlertLabel(root, "캡쳐 에러 발생")


#문구를 만들어준다.
# 에러 AlertMessaage
def makeAlertLabel(root, msg):
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label) and (widget['fg'] == 'red' or widget['fg'] == 'blue')  :
            widget.destroy()
    lbl_text = tk.Label(root, text=msg, fg="red", font=("맑은 고딕", 12))
    root.after(300, lambda: lbl_text.place(
        relx=0.5, rely=0.9, anchor="center"))
    #lbl_text.place(relx=0.5, rely=0.9, anchor="center")

# 진행Messaage


def makeProcessLabel(root, msg):
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label) and (widget['fg'] == 'red' or widget['fg'] == 'blue'):
            widget.destroy()
    lbl_text = tk.Label(root, text=msg, fg="blue", font=("맑은 고딕", 12))
    root.after(300, lambda: lbl_text.place(
        relx=0.5, rely=0.9, anchor="center"))
    #lbl_text.place(relx=0.5, rely=0.9, anchor="center")


def makePositionLabel(root, msg):
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label) and widget['fg'] == 'green':
            widget.destroy()
    lbl_text = tk.Label(root, text=msg, fg="green", font=("맑은 고딕", 6))
    lbl_text.place(relx=0.5, rely=0.35, anchor="center")

# Tkinter 윈도우 생성
root = tk.Tk()

# DPI 설정
root.tk.call('tk', 'scaling', 2.0)  # DPI를 2.0으로 설정합니다.

# 윈도우 크기 설정
window_width = int(root.winfo_screenwidth() * 0.12)
window_height = int(root.winfo_screenheight() * 0.1)
root.geometry(f"{window_width}x{window_height}")
# 윈도우 타이틀 설정
root.title("Auto Caputure")

# 전역 변수로 x_pos와 y_pos를 초기화합니다.
x_start = 0
y_start = 0
x_end = 0
y_end = 0

lbl_text = tk.Label(root, text="© PAULTALL", fg="black", font=("", 5))
lbl_text.place(relx=1.0, rely=1.0, anchor="se")

# 배경색 설정
bg_color = "#FFFFFF"
root.configure(bg=bg_color)
# 버튼 생성
# 캡쳐 영역 생성
btn_create_capture = tk.Button(
    root, text="Area (영역지정)", command=lambda: capture_to_area(root),font=("",8))
btn_create_capture.place(relx=0.5, rely=0.15, anchor="center")

# 캡쳐 영역 생성
btn_create_capture = tk.Button(
    root, text="Clipboard (클립보드)", command=capture_to_clipboard, font=("", 13))
btn_create_capture.place(relx=0.5, rely=0.6, anchor="center")

# Tkinter 실행
root.mainloop()
