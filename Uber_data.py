"""
📊 Uber Ride Analytics
------------------------
Este projeto analisa um dataset de viagens da Uber com foco em:
- Cancelamentos por tipo de veículo e hora
- Taxa de cancelamento por tipo de veículo
- Total de reservas e cancelamentos

Dataset utilizado:
https://www.kaggle.com/datasets/yashdevladdha/uber-ride-analytics-dashboard
"""

# =======================
# 1. Importação de libs
# =======================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =======================
# 2. Carregamento dos dados
# =======================
# df = pd.read_csv("/content/ncr_ride_bookings.csv")
# Exibir primeiros registros
display(df.head())

# =======================
# 3. Limpeza dos dados
# =======================
# Valores nulos
display(df.isnull().sum())
df["Driver Ratings"] = df["Driver Ratings"].fillna(df["Driver Ratings"].mean())

# Padronização de datas e horários
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Time"] = pd.to_datetime(df["Time"], format="%H:%M:%S", errors="coerce").dt.hour

# =======================
# 4. Cancelamentos
# =======================
# Filtrar viagens canceladas
cancelled_rides = df[
    (df["Booking Status"] == "Cancelled by Customer")
    | (df["Booking Status"] == "Cancelled by Driver")
].copy()

# Cancelamentos por tipo de veículo e hora
cancellation_counts = (
    cancelled_rides.groupby(["Vehicle Type", "Time"])
    .size()
    .reset_index(name="Cancellation Count")
)

# Pivot para heatmap
heatmap_data = cancellation_counts.pivot_table(
    index="Vehicle Type",
    columns="Time",
    values="Cancellation Count",
    fill_value=0
)

# =======================
# 5. Visualizações
# =======================

def plot_heatmap(data):
    """Mapa de calor de cancelamentos por tipo de veículo e hora"""
    plt.figure(figsize=(12, 8))
    sns.heatmap(data, annot=True, fmt=".0f", cmap="YlGnBu")
    plt.title("Cancelamentos por Tipo de Veículo e Hora do Dia")
    plt.xlabel("Hora do Dia")
    plt.ylabel("Tipo de Veículo")
    plt.tight_layout()
    plt.show()

def plot_pie(data):
    """Gráfico de rosca da taxa de cancelamento por tipo de veículo"""
    plt.figure(figsize=(8, 8))
    plt.pie(
        data["Cancellation Rate"],
        labels=data["Vehicle Type"],
        autopct="%1.1f%%",
        startangle=140,
        wedgeprops=dict(width=0.3)
    )
    centre_circle = plt.Circle((0, 0), 0.70, fc="white")
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.title("Taxa de Cancelamento por Tipo de Veículo")
    plt.axis("equal")
    plt.tight_layout()
    plt.show()

def plot_bar(data):
    """Gráfico de barras de cancelamentos por tipo de veículo"""
    plt.figure(figsize=(10, 6))
    sns.barplot(data=data, x="Vehicle Type", y="Cancellation Count", palette="viridis")
    plt.title("Total de Cancelamentos por Tipo de Veículo")
    plt.xlabel("Tipo de Veículo")
    plt.ylabel("Total de Cancelamentos")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

# =======================
# 6. Taxa de Cancelamento
# =======================
# Total de reservas
total_bookings = df["Vehicle Type"].value_counts().reset_index()
total_bookings.columns = ["Vehicle Type", "Total Bookings"]

# Total de cancelamentos
cancellations_by_vehicle = cancelled_rides["Vehicle Type"].value_counts().reset_index()
cancellations_by_vehicle.columns = ["Vehicle Type", "Cancellation Count"]

# Merge e taxa
cancellation_rate_df = pd.merge(total_bookings, cancellations_by_vehicle, on="Vehicle Type", how="left")
cancellation_rate_df["Cancellation Count"] = cancellation_rate_df["Cancellation Count"].fillna(0)
cancellation_rate_df["Cancellation Rate"] = (
    cancellation_rate_df["Cancellation Count"] / cancellation_rate_df["Total Bookings"]
) * 100

# =======================
# 7. Execução das visualizações
# =======================
plot_heatmap(heatmap_data)
plot_pie(cancellation_rate_df)
plot_bar(cancellations_by_vehicle)

# Mostrar tabela ordenada pela taxa de cancelamento
display(cancellation_rate_df.sort_values(by="Cancellation Rate", ascending=False))
