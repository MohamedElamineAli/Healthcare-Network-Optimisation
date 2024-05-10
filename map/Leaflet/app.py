# app.py
from flask import Flask,render_template,request,jsonify
import json
# import networkx as nx
# import osmnx as ox
import os
os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_APP'] = 'app.py'

# Rest of your Flask application code


app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Retrieve data from the request
            request_data = request.json
            file_path = "requestData.json"

            # Convert the dictionary to JSON
            json_data = json.dumps(request_data, indent=4)

            # Write the JSON data to a file
            with open(file_path, "w") as json_file:
                json_file.write(json_data)
            # Process the request data (if needed)
            # For example, you can access request_data['key'] to get values

            # Here you can fetch the data from the JSON file or any other source
            # For demonstration, let's assume you're reading from a JSON file
            with open("static/js/joe.geojson", "r") as file:
                data = json.load(file)
            return jsonify(data["features"])
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return render_template('index.html')



if __name__ == '__main__':
    app.debug = True
    app.run()
    
