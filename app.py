from flask import Flask, render_template, request, jsonify
import pandas as pd

# Import JobRecommendation class
from models.job_recommendation import JobRecommendation

# Initialize Flask app
app = Flask(__name__)

# Initialize JobRecommendation instance
job_rec = JobRecommendation()

# Define routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    job_title = request.args.get('job_title', '')
    
    if job_title:
        try:
            # Search for job titles containing the input string
            filtered_jobs = job_rec.data[job_rec.data['Job Title'].str.contains(job_title.lower().strip())]
            
            if filtered_jobs.empty:
                return jsonify({'error': f"No job titles found containing '{job_title}'."})
            
            # Convert filtered jobs to dictionary format
            jobs = filtered_jobs.to_dict(orient='records')
            return jsonify({'jobs': jobs})
        
        except Exception as e:
            return jsonify({'error': f"Error processing job title '{job_title}': {str(e)}"})
    
    else:
        return jsonify({'error': "Please provide a job title."})

@app.route('/recommend', methods=['GET'])
def recommend():
    job_title = request.args.get('job_title', '')
    
    if job_title:
        try:
            # Get recommendations based on job title
            recommendations = job_rec.recommend_jobs(job_title, n_recommendations=10)
            
            if recommendations.empty:
                return jsonify({'error': f"Job title '{job_title}' not found in the data."})
            
            # Convert recommendations to JSON format
            recommendations_json = recommendations.to_dict(orient='records')
            
            return jsonify({'recommendations': recommendations_json})
        
        except Exception as e:
            return jsonify({'error': f"Error processing job title '{job_title}': {str(e)}"})
    
    else:
        return jsonify({'error': "Please provide a job title."})
    
@app.route('/job/<title>')
def job_details(title):
    try:
        # Find the job details based on the provided title
        job_details = job_rec.data[job_rec.data['Job Title'] == title.lower().strip()].iloc[0]
        recommendations = job_rec.recommend_jobs(title, n_recommendations=10)
        
        # Convert recommendations to a list, ensuring it's not ambiguous
        recommendations_list = recommendations.to_dict('records') if not recommendations.empty else []
        return render_template('job_details.html', job=job_details, others=recommendations_list)
    except IndexError:
        return jsonify({'error': f"Job with title '{title}' not found."})

if __name__ == '__main__':
    
    app.run(host='0.0.0.0',port=5000,debug=True)
