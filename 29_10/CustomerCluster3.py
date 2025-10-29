from flask import Flask
from flaskext.mysql import MySQL
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
import numpy as np
app = Flask(__name__)

def getConnect(server, port, database, username, password):
    try:
        mysql = MySQL()
        # MySQL configuartion
        app.config['MYSQL_DATABASE_HOST'] = server
        app.config['MYSQL_DATABASE_PORT'] = port
        app.config['MYSQL_DATABASE_DB'] = database
        app.config['MYSQL_DATABASE_USER'] = username
        app.config['MYSQL_DATABASE_PASSWORD'] = password
        mysql.init_app(app)
        conn = mysql.connect()
        return conn
    except mysql.connector.Error as e:
        print("Error = ",e)
    return None

def closeConnection(conn):
    if conn != None:
        conn.close()

def queryDataset(conn, sql):
    cursor = conn.cursor()

    cursor.execute(sql)
    df = pd.DataFrame(cursor.fetchall())
    return df

conn = getConnect('localhost', 3306, 'salesdatabase', 'root', '@Obama123')

sql1 = "select * from customer"
df1 = queryDataset(conn, sql1)
print(df1)

sql2 = (
    "SELECT DISTINCT customer.CustomerId, Age, Annual_Income, Spending_Score "
    "FROM customer, customer_spend_score "
    "WHERE customer.CustomerId = customer_spend_score.CustomerID"
)

df2 = queryDataset(conn, sql2)
df2.columns = ['CustomerId', 'Age', 'Annual Income', 'Spending Score']

print(df2)

print(df2.head())

print(df2.describe())

def showHistogram(Df, columns):
    plt.figure(1, figsize=(7, 8))
    n = 0
    for column in columns:
        n += 1
        plt.subplot(3, 1, n)
        plt.subplots_adjust(hspace=0.5, wspace=0.5)
        sns.distplot(Df[column], bins=32)
        plt.title(f'Histogram of {column}')
    plt.show()

showHistogram(df2, df2.columns[1:])

def elbowMethod(df, columsForElbow):
    X = df.loc[:, columsForElbow].values
    inertia = []
    for n in range(1, 11):
        model = KMeans(n_clusters=n, init='k-means++', max_iter=500, random_state=42)
        model.fit(X)
        inertia.append(model.inertia_)

    plt.figure(1, figsize = (15, 6))
    plt.plot(np.arange(1, 11), inertia, 'o')
    plt.plot(np.arange(1, 11), inertia, '-', alpha = 0.5)
    plt.xlabel('Number of Clusters'), plt.ylabel('Cluster sum of squared distances')
    plt.show()
columns = ['Age', 'Annual Income', 'Spending Score']
elbowMethod(df2, columns)

def runKmeans(X,cluster):
    model = KMeans(n_clusters=cluster,
                   init='k-means++',
                   max_iter=500,
                   random_state=42)
    model.fit(X)
    labels = model.labels_
    centroids = model.cluster_centers_
    y_kmeans = model.fit_predict(X)
    return y_kmeans, centroids, labels
X = df2.loc[:, columns].values
cluster = 6
colors = ["red", "green", "blue", "purple", "black", "pink","orange" ]

y_kmeans, centroids, labels = runKmeans(X,cluster)
print(y_kmeans)
print(centroids)
print(labels)
df2["cluster"] = labels
print(df2)

def visualize3DKMeans(df, columns, hover_data, cluster):
    fig = px.scatter_3d(df,
                        x = columns[0],
                        y = columns[1],
                        z = columns[2],
                        color = 'cluster',
                        hover_data = hover_data,
                        category_orders={"cluster": range(0, cluster)},
                        )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    fig.show()
hover_data=df2.columns
visualize3DKMeans(df2, columns, hover_data, cluster)
