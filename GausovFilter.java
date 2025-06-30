import java.awt.image.BufferedImage;
import java.io.File;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import javax.imageio.ImageIO;

public class GausovFilter {

    static int KERNEL_SIZE = 5;
    static double SIGMA = 1.5;
    static double[][] kernel;

    public static void generateKernel() {
        kernel = new double[KERNEL_SIZE][KERNEL_SIZE];
        int offset = KERNEL_SIZE / 2;
        double sum = 0.0;

        for (int y = -offset; y <= offset; y++) {
            for (int x = -offset; x <= offset; x++) {
                double exponent = -(x * x + y * y) / (2 * SIGMA * SIGMA);
                kernel[y + offset][x + offset] = Math.exp(exponent);
                sum += kernel[y + offset][x + offset];
            }
        }

        for (int y = 0; y < KERNEL_SIZE; y++) {
            for (int x = 0; x < KERNEL_SIZE; x++) {
                kernel[y][x] /= sum;
            }
        }
    }

    public static void izglađivanje(BufferedImage input, BufferedImage output, int numThreads) throws InterruptedException {
        int width = input.getWidth();
        int height = input.getHeight();
        int offset = KERNEL_SIZE / 2;

        ExecutorService executor = Executors.newFixedThreadPool(numThreads);

        for (int y = offset; y < height - offset; y++) {
            final int row = y;
            executor.submit(() -> {
                for (int x = offset; x < width - offset; x++) {
                    double r = 0, g = 0, b = 0;

                    for (int ky = -offset; ky <= offset; ky++) {
                        for (int kx = -offset; kx <= offset; kx++) {
                            int px = x + kx;
                            int py = row + ky;
                            int rgb = input.getRGB(px, py);

                            int red = (rgb >> 16) & 0xff;
                            int green = (rgb >> 8) & 0xff;
                            int blue = rgb & 0xff;

                            double weight = kernel[ky + offset][kx + offset];
                            r += red * weight;
                            g += green * weight;
                            b += blue * weight;
                        }
                    }

                    int newRGB = ((int) r << 16) | ((int) g << 8) | (int) b;
                    output.setRGB(x, row, newRGB);
                }
            });
        }

        executor.shutdown();
        executor.awaitTermination(1, TimeUnit.MINUTES);
    }

    public static void main(String[] args) throws Exception {
        BufferedImage input = ImageIO.read(new File("QRcode.png"));

        generateKernel();

        int[] threadCounts = {1, 2, 4, 8};
        BufferedImage output = null;

        for (int threads : threadCounts) {
            output = new BufferedImage(input.getWidth(), input.getHeight(), input.getType());

            long start = System.nanoTime();
            izglađivanje(input, output, threads);
            long end = System.nanoTime();

            double duration = (end - start) / 1e9;
            System.out.printf("Broj niti: %d, Vrijeme: %.4f sekundi%n", threads, duration);
        }

        ImageIO.write(output, "jpg", new File("output.jpg"));
        System.out.println("Slika spremljena kao output.jpg");
    }
}

