def generar_eda_python(df):
    with open("eda_python.txt", "w") as f:
        f.write(df.describe().to_string())
    return "eda_python.txt"
