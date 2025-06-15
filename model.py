import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import io
import base64


def build_linear_regression_model(df):
    required_columns = {"MEDV"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Отсутствуют обязательные столбцы: {', '.join(missing)}")

    columns_to_drop = {"RAD", "TAX", "DIS", "AGE", "MEDV"}
    available_to_drop = columns_to_drop & set(df.columns)

    X = df.drop(list(available_to_drop), axis=1)
    y = df["MEDV"].values
    feature_names = X.columns.tolist()

    X = X.values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    # генерируем график
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.6)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    plt.xlabel("Настоящие значения")
    plt.ylabel("Предсказанные значения")
    plt.title("Настоящие vs Предсказанные MEDV")
    plt.grid(True)
    plt.tight_layout()

    # конвертация графика в base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    return model, r2, rmse, plot_base64, feature_names
