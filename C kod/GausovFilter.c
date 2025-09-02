#define STB_IMAGE_IMPLEMENTATION
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image.h"
#include "stb_image_write.h"

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

#define KERNEL_SIZE 5
#define SIGMA 1.5

float kernel[KERNEL_SIZE][KERNEL_SIZE];

void generate_gaussian_kernel() {
    int offset = KERNEL_SIZE / 2;
    float sum = 0.0;

    for (int y = -offset; y < KERNEL_SIZE - offset; y++) {
        for (int x = -offset; x < KERNEL_SIZE - offset; x++) {
            float exponent = -((x * x + y * y) / (2 * SIGMA * SIGMA));
            kernel[y + offset][x + offset] = expf(exponent);
            sum += kernel[y + offset][x + offset];
        }
    }

    for (int y = 0; y < KERNEL_SIZE; y++) {
        for (int x = 0; x < KERNEL_SIZE; x++) {
            kernel[y][x] /= sum;
        }
    }
}

void apply_gaussian_rgb(unsigned char *input, unsigned char *output, int width, int height, int channels) {
    int offset = KERNEL_SIZE / 2;

    #pragma omp parallel for collapse(2)
    for (int y = offset; y < height - offset; y++) {
        for (int x = offset; x < width - offset; x++) {
            for (int c = 0; c < 3; c++) {
                float sum = 0.0f;
                for (int ky = -offset; ky < KERNEL_SIZE - offset; ky++) {
                    for (int kx = -offset; kx < KERNEL_SIZE - offset; kx++) {
                        int px = x + kx;
                        int py = y + ky;
                        int index = (py * width + px) * channels + c;
                        sum += input[index] * kernel[ky + offset][kx + offset];
                    }
                }
                int out_index = (y * width + x) * channels + c;
                if (sum > 255) sum = 255;
                if (sum < 0) sum = 0;
                output[out_index] = (unsigned char)sum;
            }
            if (channels == 4) {
                int a_index = (y * width + x) * channels + 3;
                output[a_index] = input[a_index];
            }
        }
    }
}

int main() {
    int width, height, channels;
    unsigned char *input_img = stbi_load("Gauss.jpg", &width, &height, &channels, 0);

    unsigned char *output_img = (unsigned char *)malloc(width * height * channels);

    generate_gaussian_kernel();

    int thread_counts[] = {1, 2, 4, 8};
    int num_tests = sizeof(thread_counts) / sizeof(thread_counts[0]);


    for (int i = 0; i < num_tests; i++) {
        int threads = thread_counts[i];
        omp_set_num_threads(threads);

        double start = omp_get_wtime();
        apply_gaussian_rgb(input_img, output_img, width, height, channels);
        double end = omp_get_wtime();

        printf("broj niti: %d Vrijeme: %f\n", threads, end - start);
    }

    stbi_write_jpg("output.jpg", width, height, channels, output_img, 100);

    printf("Zamucivanje gotovo. Spremio output.jpg\n");

    stbi_image_free(input_img);
    free(output_img);

    return 0;
}
//gcc -fopenmp -Wall -o GausovFilter.exe GausovFilter.c
//./GausovFilter