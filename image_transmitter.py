import os
import numpy as np
import cv2


'''
Takes an image, resizes to 96*96, converts to grayscale, and then flattens it.
'''
if __name__=="__main__":
    while True:
        filename = input("Enter the image filename: ")
        
        if not os.path.exists(filename):
            print(f"File {filename} does not exist.")
            continue

        image = cv2.imread(filename)
        resized_image = cv2.resize(image, (96, 96), interpolation=cv2.INTER_LINEAR)
        grayscale_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

        cv2.imshow("Grayscale Image", grayscale_image)
        cv2.waitKey(0)  # Wait for a key press (0 means wait indefinitely)
        cv2.destroyAllWindows()  # Close the window

        cv2.imwrite("output.png", grayscale_image)

        flattened_image = grayscale_image.flatten()
        flattened_2d = flattened_image.reshape(1, -1)  # 1x9216
        cv2.imwrite("flattened.png", flattened_2d)

        # Convert the flattened array to bytes
        flattened_bytes = flattened_image.astype(np.uint8).tobytes()
        