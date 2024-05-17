# app.py
from flask import Flask,render_template,request,jsonify
import json
import _pickle as cPickle

# import networkx as nx
# import osmnx as ox
import os
from libs import utils
os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_APP'] = 'app.py'

# Rest of your Flask application code


print("fetching graph..")
with open(r"data/algiers_raw_simplified.pkl", "rb") as input_file:
    graph = cPickle.load(input_file)
print("fetching additional data..")
with open('data/algiers.geojson', 'r') as file:
    algiers_borders = json.load(file)
with open('data/hospitalWithID.json', 'r') as file:
    hospitals = json.load(file)
print("done fetching")


app = Flask(__name__)



@app.route('/bound_checking', methods=['GET', 'POST'])
def bound_checking():
    if request.method == 'POST':
        try:
            request_data = request.json
            long, lat = request_data["longitude"], request_data["latitude"]
            response = {
                "is_inside_algiers": utils.is_inside_algiers(long, lat, algiers_borders)
            }
            return jsonify(response)
        except Exception as e:
             return jsonify({'error': str(e)}), 500


@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')


@app.route('/main', methods=['POST'])
def f_main():
    if request.method == 'POST':
        #try:
            # Retrieve data from the request
            request_data = request.json
            data = utils.search_handler(hospitals=hospitals["hospitals"], graph=graph, request=request_data)
            return jsonify(data)
        #except Exception as e:
            #return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.debug = True
    app.run()
    
