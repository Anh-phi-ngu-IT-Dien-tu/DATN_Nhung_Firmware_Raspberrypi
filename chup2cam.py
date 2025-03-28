import cv2
import numpy as np
import urllib.request
import os
import re

# IP stream URLs của hai camera
urlL = "http://192.168.137.206/capture"      # Camera trái
urlR = "http://192.168.137.202/capture"      # Camera phải

# Tạo thư mục lưu ảnh nếu chưa tồn tại
os.makedirs('images/trai', exist_ok=True)
os.makedirs('images/phai', exist_ok=True)

# Hàm lấy số thứ tự ảnh tiếp theo
def get_next_image_num(directory, prefix):
    files = [f for f in os.listdir(directory) if re.match(rf"{prefix}_\d+\.png", f)]
    if files:
        nums = [int(re.search(rf"{prefix}_(\d+)\.png", f).group(1)) for f in files]
        return max(nums) + 1
    return 0

# Lấy số thứ tự ảnh bắt đầu
num = max(get_next_image_num('images/trai', 'Im_L'),
          get_next_image_num('images/phai', 'Im_R'))

while True:
    try:
        # Đọc ảnh từ camera trái
        img_respL = urllib.request.urlopen(urlL)
        imgnpL = np.array(bytearray(img_respL.read()), dtype=np.uint8)
        imgL = cv2.imdecode(imgnpL, cv2.IMREAD_COLOR)

        # Đọc ảnh từ camera phải
        img_respR = urllib.request.urlopen(urlR)
        imgnpR = np.array(bytearray(img_respR.read()), dtype=np.uint8)
        imgR = cv2.imdecode(imgnpR, cv2.IMREAD_COLOR)

        if imgL is None or imgR is None:
            print("Không nhận được ảnh từ một trong hai camera.")
            continue

        # Hiển thị cả hai ảnh
        cv2.imshow('Left Camera', imgL)
        cv2.imshow('Right Camera', imgR)

        k = cv2.waitKey(5)
        if k == 27:  # ESC để thoát
            break
        elif k == ord('m'):  # Nhấn 'm' để lưu ảnh
            cv2.imwrite(f'images/trai/Im_L_{num}.png', imgL)
            cv2.imwrite(f'images/phai/Im_R_{num}.png', imgR)
            print(f"Đã lưu ảnh Im_L_{num}.png và Im_R_{num}.png")
            num += 1 

    except Exception as e:
        print(f"Lỗi khi lấy ảnh: {e}")
        continue

# Giải phóng tài nguyên
cv2.destroyAllWindows()
