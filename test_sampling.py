import cv2

from sampling import BrightnessSampler

image = cv2.imread("input.jpg", cv2.IMREAD_GRAYSCALE)

sampler = BrightnessSampler(image)

print(sampler.sample(100, 100))
print(sampler.sample(200, 200))
print(sampler.sample(300, 300))