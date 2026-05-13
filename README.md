# Turismo AI Colombia

Aplicacion web en Flask para predecir saturacion turistica en pueblos patrimonio de Colombia.

## Funciones

- Landing page con estetica futurista.
- Dashboard con graficas de ocupacion y turistas.
- Mapa interactivo con Leaflet.
- Simulador de prediccion con Machine Learning.
- Modelo Random Forest para clasificacion y regresion.
- Dataset simulado con destinos reconocidos: Salento, Guatape, Villa de Leyva, Barichara, Jardin, Filandia, Mompox, Jerico, Mongui, Salamina, Honda y Santa Fe de Antioquia.

## Ejecutar en Visual Studio Code

Abre esta carpeta:

```powershell
C:\Users\karen\Desktop\UDEC\MACHINE\REPOGITHUB\Proyecto_Final
```

Crea y activa un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instala dependencias:

```powershell
pip install -r requirements.txt
```

Entrena el modelo:

```powershell
python model\entrenamiento.py
```

Inicia Flask:

```powershell
python app.py
```

Luego abre:

```text
http://127.0.0.1:5000
```
