import cv2
import numpy as np
import os

def stop_sign(img_path, output_path):
    img = cv2.imread(img_path)
    if img is None:
        print(f"[HATA] Resim okunamadı veya dosya yolu hatalı: {img_path}")
        return None, None
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red1 = np.array([0, 50, 50])   
    upper_red1 = np.array([15, 255, 255])
    lower_red2 = np.array([170, 70, 50]) 
    upper_red2 = np.array([180, 255, 255])
    turn1 = cv2.inRange(hsv, lower_red1, upper_red1)
    turn2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(turn1, turn2)
    kernel = np.ones((3, 3), np.uint8)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel, iterations=2)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print(f"[UYARI] {os.path.basename(img_path)}: Kırmızı öğe bulunamadı.")
        return None, None 
    img_h, img_w = img.shape[:2]
    candidates = [] 
    for cnt in contours: 
        area = cv2.contourArea(cnt) 
        if area < 1000:
            continue
        peri = cv2.arcLength(cnt, True) 
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        n_corners = len(approx) 
        if not (6 <= n_corners <= 10):
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h)
        if not (0.8 <= aspect_ratio <= 1.2): 
            continue
        M = cv2.moments(cnt) 
       
        cX = int(M["m10"] / M["m00"]) 
        cY = int(M["m01"] / M["m00"]) 
        dist_center = abs(cX - img_w // 2)
        candidates.append({
            "contour": cnt,
            "area": area,
            "n_corners": n_corners,
            "aspect_ratio": aspect_ratio,
            "centroid": (cX, cY),
            "dist_center": dist_center,
            "bbox": (x, y, w, h)
        })

    if not candidates:
        print(f"[UYARI] {os.path.basename(img_path)}: Filtrelerden geçebilecek bir kontur bulunamadı.")
        return None, None 

    candidates = sorted(candidates, key=lambda x: (x["area"], -x["dist_center"]), reverse=True)
    best = candidates[0] 

    x, y, w, h = best["bbox"] 
    cX, cY = best["centroid"] 

    result_img = img.copy()
    cv2.rectangle(result_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.circle(result_img, (cX, cY), 5, (255, 0, 0), -1)

    print(f"[BİLGİ] {os.path.basename(img_path)}: STOP levhası bulundu. Merkez = ({cX}, {cY}), Alan = {best['area']:.1f}, Köşe sayısı = {best['n_corners']}, En/Boy = {best['aspect_ratio']:.2f}")
    cv2.imwrite(output_path, result_img)
    print(f"[KAYDEDİLDİ] {output_path}")

    return result_img, (cX, cY) 

if __name__ == "__main__":
    dataset_path = "stop_sign_dataset"
    output_dir = "output_images"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"[BİLGİ] Çıktı klasörü oluşturuldu: '{output_dir}'")
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')

    print(f"\n'{dataset_path}' klasöründeki resimler işleniyor...\n")
    for filename in os.listdir(dataset_path):
        if filename.lower().endswith(image_extensions):
            input_image_path = os.path.join(dataset_path, filename)
            output_image_path = os.path.join(output_dir, f"detected_{filename}")

            print(f"-> İşleniyor: {filename}")
            detected_img, centroid_coords = stop_sign(input_image_path, output_image_path)
            print("-" * 50) 

    print("\nTüm uygun resimler başarıyla işlendi.")
    print(f"İşlenmiş çıktılar '{output_dir}' klasöründe bulunmaktadır.")