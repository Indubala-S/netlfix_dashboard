from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

data_df = pd.read_csv('netflix (1).csv')

@app.route('/')
def home():
    # Get filter from query parameters
    selected_type = request.args.get('type', 'All')
    df = data_df.copy()
    df['type'] = df['type'].fillna('Unknown')
    df['director'] = df['director'].fillna('Unknown')
    df['country'] = df['country'].fillna('Unknown')
    
    # Get unique types for dropdown
    content_types = ['All'] + sorted(df['type'].unique())
    
    # Filter by type if not "All"
    if selected_type != 'All':
        df = df[df['type'] == selected_type]

    # Aggregations
    top_directors = df['director'].value_counts().head(10).to_dict()
    top_countries = df['country'].value_counts().head(10).to_dict()

    return render_template(
        'index.html',
        top_directors=top_directors,
        top_countries=top_countries,
        content_types=content_types,
        selected_type=selected_type
    )

if __name__ == "__main__":
    app.run(debug=True)