from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Read and process the CSV data
def load_data():
    # Read the CSV with proper encoding
    df = pd.read_csv('data.csv')
    
    # Get unique values for each column for dropdowns
    unique_values = {
        '縣市': sorted(df['縣市'].unique().tolist()),
        '醫療院所': sorted(df['醫療院所'].dropna().unique().tolist()),
        '科別': sorted(df['科別'].dropna().unique().tolist()),
        '學歷': sorted(df['學歷'].dropna().unique().tolist())
    }
    
    return df, unique_values

# Routes
@app.route('/')
def index():
    df, unique_values = load_data()
    return render_template('index.html', unique_values=unique_values)

@app.route('/search', methods=['POST'])
def search():
    df, _ = load_data()
    
    # Get filter values from request
    filters = {
        '縣市': request.form.get('city'),
        '醫療院所': request.form.get('hospital'),
        '科別': request.form.get('department'),
        '學歷': request.form.get('education')
    }
    
    # Apply filters only if not "all"
    for column, value in filters.items():
        if value and value != 'all':
            # Handle NaN values when filtering
            if pd.isna(value):
                df = df[df[column].isna()]
            else:
                df = df[df[column] == value]
    
    # Convert to dict for JSON response
    results = df.to_dict('records')
    return jsonify({'data': results})

if __name__ == '__main__':
    app.run(debug=True)