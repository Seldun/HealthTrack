import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Sequential

# Генерация синтетических данных для примера
data = {
    'age': np.random.randint(18, 80, 1000),
    'temperature': np.random.uniform(36.0, 40.0, 1000),
    'headache': np.random.choice([0, 1], 1000),
    'cough': np.random.choice([0, 1], 1000),
    'diagnosis': np.random.choice(['flu', 'cold', 'allergy'], 1000)
}

df = pd.DataFrame(data)

# Преобразование категориальных признаков
encoder = OneHotEncoder(sparse_output=False)
diagnosis_encoded = encoder.fit_transform(df[['diagnosis']])

# Нормализация числовых признаков
scaler = StandardScaler()
numerical_features = scaler.fit_transform(df[['age', 'temperature']])

# Объединение признаков
X = np.concatenate([numerical_features, df[['headache', 'cough']]], axis=1)
y = diagnosis_encoded

# Разделение данных
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Создание модели
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dense(3, activation='softmax')
])

# Компиляция модели
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Обучение модели
history = model.fit(X_train, y_train,
                    epochs=50,
                    batch_size=32,
                    validation_split=0.2)

# Оценка модели
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {accuracy:.2f}")

# Пример предсказания
new_data = np.array([[35, 38.5, 1, 1]])  # Возраст, температура, головная боль, кашель
scaled_data = scaler.transform(new_data[:, :2])
processed_data = np.concatenate([scaled_data, new_data[:, 2:]], axis=1)

prediction = model.predict(processed_data)
diagnosis = encoder.inverse_transform(prediction)

print(f"Вероятности диагнозов: {prediction}")
print(f"Предполагаемый диагноз: {diagnosis[0][0]}")
