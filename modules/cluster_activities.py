import sqlite3
import time
import pandas as pd
from sklearn.cluster import KMeans


def load_activity_data(days=7):
    conn = sqlite3.connect("data/productivity.db")
    query = f"SELECT * FROM activities WHERE timestamp > {time.time() - days*86400}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def cluster_activities():
    df = load_activity_data()
    
    # Feature Engineering
    df["hour"] = pd.to_datetime(df["timestamp"], unit="s").dt.hour
    app_counts = df["app"].value_counts().to_dict()
    df["app_frequency"] = df["app"].map(app_counts)
    
    # K-Means Clustering
    X = df[["hour", "app_frequency"]].values
    kmeans = KMeans(n_clusters=3).fit(X)
    df["cluster"] = kmeans.labels_
    
    return df

