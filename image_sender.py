import os
import numpy as np
import cv2
from sender_class import CommandTransmission


'''
Takes an image, resizes to 96*96, converts to grayscale, and then flattens it.
'''
if __name__=="__main__":
    sender_obj = CommandTransmission()
    debug = False

    while True:
        filename = input("Enter the image filename (or 'q'): ")

        if filename.lower() == 'q':
            break
        
        if not os.path.exists(filename):
            print(f"File {filename} does not exist.")
            continue

        image = cv2.imread(filename)
        resized_image = cv2.resize(image, (96, 96), interpolation=cv2.INTER_LINEAR)
        grayscale_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

        flattened_image = grayscale_image.flatten()
        flattened_2d = flattened_image.reshape(1, -1)  # 1x9216

        if debug:
            cv2.imshow("Grayscale Image", grayscale_image)
            cv2.waitKey(0)  # Wait for a key press (0 means wait indefinitely)
            cv2.destroyAllWindows()  # Close the window
            cv2.imwrite("output.png", grayscale_image)
            cv2.imwrite("flattened.png", flattened_2d)

        # Convert the flattened array to bytes
        flattened_bytes = flattened_image.astype(np.uint8).tobytes()

        sender_obj.send_data(1, flattened_bytes)

    sender_obj.close()
