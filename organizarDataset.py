import os
import shutil
import pandas as pd


def organizar_renombrar_y_actualizar_csv(carpeta, tipo):
    # Leer el archivo CSV
    csv_path = os.path.join(carpeta, "_classes.csv")
    df = pd.read_csv(csv_path)

    # Obtener las columnas de clase (excluyendo la columna 'filename')
    clases = df.columns[1:]

    # Crear subcarpetas para cada clase
    for clase in clases:
        ruta_clase = os.path.join(carpeta, clase)
        os.makedirs(ruta_clase, exist_ok=True)

    # Mover y renombrar cada imagen según su clase
    for _, row in df.iterrows():
        filename = row["filename"]
        for clase in clases:
            if row[clase] == 1:
                # Mover la imagen a la carpeta de su clase
                origen = os.path.join(carpeta, filename)
                extension = os.path.splitext(filename)[1]
                # Contar cuántas imágenes ya hay en la carpeta para nombrarlas secuencialmente
                num_imagenes = len(
                    [
                        name
                        for name in os.listdir(os.path.join(carpeta, clase))
                        if os.path.isfile(os.path.join(carpeta, clase, name))
                    ]
                )
                nuevo_nombre = f"{tipo}_imagen_{num_imagenes + 1}_{clase}{extension}"

                destino = os.path.join(carpeta, clase, nuevo_nombre)
                shutil.move(origen, destino)
                print(f"Movido y renombrado {filename} a {nuevo_nombre}")

                # Actualizar la columna filename con el nuevo nombre
                df.loc[df["filename"] == filename, "filename"] = nuevo_nombre

    # Guardar el CSV actualizado, reemplazando el filename por el nuevo nombre
    df.drop(columns=["new_filename"], inplace=True, errors="ignore")
    df.to_csv(csv_path, index=False)
    print(f"CSV actualizado guardado en {csv_path}")


carpetas = {
    "./imageWater/test": "test",
    "./imageWater/train": "train",
}

# Carpetas a procesar
for carpeta, tipo in carpetas.items():
    organizar_renombrar_y_actualizar_csv(carpeta, tipo)
