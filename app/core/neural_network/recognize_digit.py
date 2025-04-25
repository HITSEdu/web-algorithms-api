import tensorflow as tf
import numpy as np
from PIL import Image
from app.utils.config import config

model = tf.keras.models.load_model(r'app/core/neural_network/digit_model.keras')


def resize_canvas(canvas):
    img = Image.fromarray(np.array(canvas, dtype=np.uint8) * 255)
    img = img.resize((config.neural_network.WIDTH, config.neural_network.HEIGHT), Image.BILINEAR)
    resized_canvas = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(resized_canvas, axis=(0, -1))


def predict_digit(canvas):
    predict = model.predict(resize_canvas(canvas.pixels), verbose=0)[0]
    digit = int(np.argmax(predict))
    predict *= 100
    predict = np.round(predict, 0).astype(int)
    return digit, predict.tolist()
