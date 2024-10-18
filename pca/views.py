# pca_app/views.py

import seaborn as sns
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA


def scatter_plot_view(request):
    return render(request, 'pca/pca_scatter.html')


def pca_view(request):
    # Load the iris dataset
    iris_data = sns.load_dataset('iris')

    # Extract features and labels
    X = iris_data[["sepal_length", "sepal_width", "petal_length", "petal_width"]].values
    y = iris_data["species"].values

    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Perform LDA to reduce dimensions to 2 components
    lda = LDA(n_components=2)
    X_lda = lda.fit_transform(X_scaled, y)  # LDA requires both X and y

    # Create a DataFrame for the LDA result
    lda_df = pd.DataFrame(data=X_lda, columns=['LD1', 'LD2'])
    lda_df['species'] = y

    # Convert DataFrame to JSON
    lda_data = lda_df.to_dict(orient='records')

    # Return LDA data as JSON
    return JsonResponse(lda_data, safe=False)


def histogram_data_view(request):
    # Load the iris dataset
    iris_data = sns.load_dataset('iris')

    # Extract features and labels
    X = iris_data[["sepal_length", "sepal_width", "petal_length", "petal_width"]].values
    y = iris_data["species"].values

    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Perform PCA to reduce dimensions to 1 component
    pca = PCA(n_components=1)
    X_pca = pca.fit_transform(X_scaled)

    # Add the reduced PCA component to the original dataset
    iris_data['PCA1'] = X_pca

    # Prepare PCA data for each species
    pca_hist_data = {
        'setosa': iris_data[iris_data['species'] == 'setosa']['PCA1'].tolist(),
        'versicolor': iris_data[iris_data['species'] == 'versicolor']['PCA1'].tolist(),
        'virginica': iris_data[iris_data['species'] == 'virginica']['PCA1'].tolist()
    }

    return JsonResponse(pca_hist_data)