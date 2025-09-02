import cv2
import numpy as np
import math
import time
from multiprocessing import Pool, cpu_count

def gaussian_kernel(size: int, sigma: float):
    kernel = [[0.0 for _ in range(size)] for _ in range(size)]
    mean = size // 2
    sum_val = 0.0

    for x in range(size):
        for y in range(size):
            exponent = -((x - mean) ** 2 + (y - mean) ** 2) / (2 * sigma ** 2)
            kernel[x][y] = math.exp(exponent) / (2 * math.pi * sigma ** 2)
            sum_val += kernel[x][y]

    for x in range(size):
        for y in range(size):
            kernel[x][y] /= sum_val

    return kernel

def process_row(args):
    row_index, image, kernel = args
    height, width, channels = len(image), len(image[0]), len(image[0][0])
    ksize = len(kernel)
    offset = ksize // 2
    new_row = [[0 for _ in range(channels)] for _ in range(width)]

    for x in range(width):
        for c in range(channels):
            val = 0.0
            for ky in range(ksize):
                for kx in range(ksize):
                    iy = min(max(row_index + ky - offset, 0), height - 1)
                    ix = min(max(x + kx - offset, 0), width - 1)
                    val += image[iy][ix][c] * kernel[ky][kx]
            new_row[x][c] = int(val)

    return row_index, new_row

def parallel_gaussian_blur(image, ksize=5, sigma=1.5, num_workers=cpu_count()):
    kernel = gaussian_kernel(ksize, sigma)
    height, width, channels = image.shape

    image_list = [[[int(image[y][x][c]) for c in range(channels)] for x in range(width)] for y in range(height)]

    args = [(row, image_list, kernel) for row in range(height)]

    output = [[[0 for _ in range(channels)] for _ in range(width)] for _ in range(height)]

    with Pool(processes=num_workers) as pool:
        for row_index, new_row in pool.map(process_row, args):
            output[row_index] = new_row

    return np.array(output, dtype=np.uint8)


if __name__ == "__main__":
    img = cv2.imread("Gauss.jpg")

    thread_counts = [1, 2, 4, 8]
    blurred_img = None

    for threads in thread_counts:
        start_time = time.time()
        blurred_img = parallel_gaussian_blur(img, ksize=5, sigma=1.5, num_workers=threads)
        end_time = time.time()

        print(f"Broj procesa: {threads}, Vrijeme izvođenja: {end_time - start_time:.4f} sekundi")

    cv2.imwrite("output.jpg", blurred_img)
    print("Slika spremljena kao: output.jpg")