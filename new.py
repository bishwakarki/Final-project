import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data (assuming you have already loaded and preprocessed your data)
data = pd.read_csv(r'C:\\Users\\bishowa\\OneDrive\\Desktop\\Final project\\data\\jobs.csv')
data = data.sample(10000).reset_index(drop=True)
data.drop("Unnamed: 0", axis=1, inplace=True)
data.dropna(subset=['Job Title', 'Key Skills'], inplace=True)

# Normalize job titles
data['Job Title'] = data['Job Title'].str.lower().str.strip()

# Text processing and TF-IDF vectorization
features = data["Key Skills"].astype(str)
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(features)

# Calculate cosine similarity matrix
similarity = cosine_similarity(tfidf_matrix)

# Function to recommend jobs based on similarity
def recommend_jobs(job_title, similarity_matrix, n_recommendations=10):
    # Find index of the job title
    index = data[data['Job Title'] == job_title.lower().strip()].index[0]
    
    # Enumerate similarities for the job title
    similarities_with_indices = list(enumerate(similarity_matrix[index]))
    
    # Sort by similarity score (excluding itself)
    sorted_similarities = sorted(similarities_with_indices, key=lambda x: x[1], reverse=True)[1:n_recommendations+1]
    
    # Extract indices of recommended jobs
    recommended_indices = [idx for idx, _ in sorted_similarities]
    
    # Return recommended jobs
    return data.iloc[recommended_indices][['Job Title', 'Job Experience Required', 'Key Skills']]

# Example usage:
target_job_title = "software developer"
recommendations = recommend_jobs(target_job_title, similarity, n_recommendations=10)
print(f"Recommendations for '{target_job_title}':")
print(recommendations)
