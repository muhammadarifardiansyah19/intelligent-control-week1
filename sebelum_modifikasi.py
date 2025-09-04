import cv2
import numpy as np

# Inisialisasi kamera
cap = cv2.VideoCapture(0)

# Periksa apakah kamera berhasil dibuka
if not cap.isOpened():
    print("Gagal membuka kamera.")
    exit()

while True:
    # Membaca frame dari kameraq
    ret, frame = cap.read()
    if not ret:
        print("Gagal membaca frame.")
        break

    # Konversi frame ke HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Rentang warna merah dalam HSV
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])

    # Masking untuk mendeteksi warna merah
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Hasil masking ditumpuk pada frame asli
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Menampilkan hasil
    cv2.imshow("Frame", frame)     # Tampilan asli
    cv2.imshow("Mask", mask)       # Masking warna merah
    cv2.imshow("Result", result)   # Hasil deteksi warna merah

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Lepaskan kamera dan tutup semua jendela
cap.release()
cv2.destroyAllWindows()
