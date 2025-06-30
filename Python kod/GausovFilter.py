import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import time

def apply_gaussian_to_row(row_index, image, ksize, sigma):
    row = image[row_index:row_index + 1, :]
    blurred_row = cv2.GaussianBlur(row, ksize, sigma)
    return row_index, blurred_row

def parallel_gaussian_blur(image, ksize=(11,11), sigma=5.5, max_workers=4):
    output = np.zeros_like(image)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(apply_gaussian_to_row, i, image, ksize, sigma) for i in range(image.shape[0])]
        for f in futures:
            i, blurred = f.result()
            output[i] = blurred
    return output

img = cv2.imread("Gauss.jpg")

thread_counts = [1, 2, 4, 8]
blurred_img = None

for threads in thread_counts:
    start_time = time.time()
    blurred_img = parallel_gaussian_blur(img, max_workers=threads)
    end_time = time.time()

    print(f"Broj niti: {threads}, Vrijeme izvođenja: {end_time - start_time:.4f} sekundi")

cv2.imwrite("output.jpg", blurred_img)
print("Slika spremljena kao: output.jpg")

cv2.imshow("Output", blurred_img)
cv2.waitKey(0)
cv2.destroyAllWindows()


