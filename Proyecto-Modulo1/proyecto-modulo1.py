import gradio as gr
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

from eda_python import generar_eda_python
from eda_r import generar_eda_r  # cuando esté listo

df_global = pd.DataFrame()  # almacena el df subido


def cargar_csv(file):
    global df_global
    df_global = pd.read_csv(file.name)
    return df_global.head()


def mostrar_info(df):
    buffer = io.StringIO()
    df.info(buf=buffer)
    return buffer.getvalue()


def mostrar_describe(df):
    return df.describe().T


def mostrar_pairplot(df):
    sns.pairplot(df.select_dtypes(include='number'))
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf


def graficar(df, tipo):
    plt.figure()
    if tipo == "Histograma":
        df.select_dtypes(include="number").hist()
    elif tipo == "Gráfico de barras":
        df.iloc[:, 0].value_counts().plot(kind="bar")
    elif tipo == "Gráfico de pie":
        df.iloc[:, 0].value_counts().plot(kind="pie", autopct='%1.1f%%')
    elif tipo == "Dispersión":
        if df.select_dtypes(include="number").shape[1] >= 2:
            df.plot.scatter(x=df.columns[0], y=df.columns[1])
        else:
            return "Se necesitan al menos 2 columnas numéricas."
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf


def generar_reportes():
    path_python = generar_eda_python(df_global)
    path_r = generar_eda_r(df_global)  # cuando esté lista
    return path_python, path_r
    

with gr.Blocks() as demo:
    gr.Markdown("## Web App de EDA - Ciencia de Datos con Python y R")

    file_input = gr.File(label="Sube tu archivo CSV", file_types=[".csv"])
    df_output = gr.Dataframe(label="Vista previa del DataFrame")

    file_input.change(fn=cargar_csv, inputs=file_input, outputs=df_output)

    with gr.Row():
        check_info = gr.Checkbox(label="Mostrar df.info()")
        check_desc = gr.Checkbox(label="Mostrar df.describe()")
        check_pair = gr.Checkbox(label="Mostrar Pairplot")

    info_output = gr.Textbox(label="df.info()")
    desc_output = gr.Dataframe(label="df.describe().T")
    pair_output = gr.Image(label="Pairplot")

    check_info.change(fn=lambda: mostrar_info(df_global), inputs=[], outputs=info_output)
    check_desc.change(fn=lambda: mostrar_describe(df_global), inputs=[], outputs=desc_output)
    check_pair.change(fn=lambda: mostrar_pairplot(df_global), inputs=[], outputs=pair_output)

    gr.Markdown("### Elegir tipo de gráfico")
    tipo_grafico = gr.Radio(["Histograma", "Gráfico de barras", "Gráfico de pie", "Dispersión"], label="Tipo de gráfico")
    grafico_output = gr.Image(label="Gráfico")

    tipo_grafico.change(fn=lambda tipo: graficar(df_global, tipo), inputs=tipo_grafico, outputs=grafico_output)

    gr.Markdown("### Generar Reportes EDA")
    btn_reportes = gr.Button("Generar Reportes en Python y R")
    eda_python_file = gr.File(label="Reporte EDA - Python")
    eda_r_file = gr.File(label="Reporte EDA - R")

    btn_reportes.click(fn=generar_reportes, outputs=[eda_python_file, eda_r_file])

demo.launch(share=True)
