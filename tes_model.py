import tensorflow as tf

CLASSES = ["curly", "kinky", "straight", "wavy"]
model = tf.keras.models.load_model("backend/model/hair_EfficientNetB0.keras")

ds = tf.keras.utils.image_dataset_from_directory(
    "test",
    class_names=CLASSES,
    image_size=(224, 224),
    batch_size=32,
    shuffle=False,
)

benar, total = 0, 0
for x, y in ds:
    pred = tf.argmax(model.predict(x, verbose=0), axis=1, output_type=tf.int32)
    benar += int(tf.reduce_sum(tf.cast(pred == y, tf.int32)))
    total += len(y)

print(f"Total gambar: {total}")
print(f"Akurasi: {benar/total*100:.2f}%")