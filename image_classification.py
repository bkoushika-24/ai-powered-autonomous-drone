import tensorflow as tf
from tensorflow.keras import datasets, models, layers
import numpy as np
import matplotlib.pyplot as plt

# Load CIFAR-10 dataset
(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()
train_images, test_images = train_images / 255.0, test_images / 255.0

# Correct class names for CIFAR-10
class_names = ["airplane", "automobile", "bird", "cat", "deer", 
               "dog", "frog", "horse", "ship", "truck"]

# Model definition
model = models.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(32,32,3)),
    layers.MaxPooling2D((2,2)),  # Downsamples image

    layers.Conv2D(64, (3,3), activation="relu"),
    layers.MaxPooling2D((2,2)),

    layers.Conv2D(64, (3,3), activation="relu"),
    layers.Flatten(),

    layers.Dense(64, activation="relu"),
    layers.Dense(10)  # 10 classes in CIFAR-10
])

# Compile the model (Fixed 'optimize' → 'optimizer')
model.compile(optimizer="adam", 
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), 
              metrics=["accuracy"])

# Train the model (Fixed validation labels)
history = model.fit(train_images, train_labels, epochs=10, validation_data=(test_images, test_labels))

# Convert model to a probability model
probability_model = tf.keras.Sequential([model, layers.Softmax()])

# Make a prediction on a test image
image = test_images[0]  # Select a test image
image = np.expand_dims(image, axis=0)  # Add batch dimension
predictions = probability_model.predict(image)

# Fix class label retrieval
predicted_class_index = np.argmax(predictions[0])
class_label = class_names[predicted_class_index]

# Display the image with predicted label
plt.figure(figsize=(3,3))  # Fixed figure size
plt.imshow(test_images[0])  # Show test image instead of train image
plt.xlabel(f"Predicted: {class_label}", color="blue")
plt.show()
