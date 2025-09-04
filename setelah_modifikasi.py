import cv2
import numpy as np

# Inisialisasi kamera
cap = cv2.VideoCapture(0)

# Periksa apakah kamera berhasil dibuka
if not cap.isOpened():
    print("Gagal membuka kamera.")
    exit()

while True:
    # Membaca frame dari kamera
    ret, frame = cap.read()
    if not ret:
        print("Gagal membaca frame.")
        break

    # Konversi frame ke HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # ====== Rentang Warna dalam HSV ======
    # Warna merah
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Warna hijau
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])

    # Warna biru
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])

    # ====== Masking ======
    mask_red = cv2.inRange(hsv, lower_red1, upper_red1) | cv2.inRange(hsv, lower_red2, upper_red2)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # ====== Fungsi untuk Deteksi dan Gambar Bounding Box ======
    def detect_and_draw(mask, color_name, color_bgr):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 800:  # Hanya deteksi objek dengan luas signifikan
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color_bgr, 2)
                cv2.putText(frame, color_name, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_bgr, 2)

    # Deteksi masing-masing warna
    detect_and_draw(mask_red, "Merah", (0, 0, 255))
    detect_and_draw(mask_green, "Hijau", (0, 255, 0))
    detect_and_draw(mask_blue, "Biru", (255, 0, 0))

    # Gabungkan hasil masking untuk ditampilkan
    combined_mask = cv2.bitwise_or(mask_red, cv2.bitwise_or(mask_green, mask_blue))
    result = cv2.bitwise_and(frame, frame, mask=combined_mask)

    # ====== Tampilkan Hasil ======
    cv2.imshow("Frame", frame)         # Frame asli dengan bounding box
    cv2.imshow("Mask", combined_mask)  # Masking gabungan
    cv2.imshow("Result", result)       # Hasil deteksi warna

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Lepaskan kamera dan tutup semua jendela
cap.release()
cv2.destroyAllWindows()
