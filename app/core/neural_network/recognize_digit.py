import tensorflow as tf
import numpy as np
from PIL import Image

IMG_HEIGHT = 28
IMG_WIDTH = 28

model = tf.keras.models.load_model(r'app/core/neural_network/digit_model.keras')


def resize_canvas(canvas):
    img = Image.fromarray(np.array(canvas, dtype=np.uint8) * 255)
    img = img.resize((IMG_WIDTH, IMG_HEIGHT), Image.BILINEAR)

    resized_canvas = np.array(img, dtype=np.float32) / 255.0

    return np.expand_dims(resized_canvas, axis=(0, -1))


def predict_digit(canvas):
    prediction = model.predict(resize_canvas(canvas))
    return int(np.argmax(prediction))
