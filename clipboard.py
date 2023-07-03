from PIL import Image
import win32clipboard
from io import BytesIO
from PIL import ImageGrab, Image

# 클립보드에서 읽어오기
# img = ImageGrab.grabclipboard()
# print(img)
# print(isinstance(img, Image.Image))
# print(img.size)
# print(img.mode)
# img.save('C:\developer\hjppt\kkk.png')

# 파일을 클립보드로 보내기.
def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()


filepath = 'C:\developer\hjppt\capture.png'
image = Image.open(filepath)

output = BytesIO()
image.convert("RGB").save(output, "BMP")
data = output.getvalue()[14:]
output.close()

send_to_clipboard(win32clipboard.CF_DIB, data)
