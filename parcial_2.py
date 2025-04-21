from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Cargar datos
df = pd.read_csv('vacunacion_sarampion_panama.csv')
data = df.to_dict(orient='records')

@app.route('/api/v1/vacunacion', methods=['GET'])
def get_all_data():
    return jsonify(data), 200

@app.route('/api/v1/vacunacion/<int:year>', methods=['GET'])
def get_data_by_year(year):
    result = [record for record in data if record['Year'] == year]
    if result:
        return jsonify(result[0]), 200
    else:
        return jsonify({"error": "Año no encontrado"}), 404

@app.route('/api/v1/vacunacion/range/<int:start_year>/<int:end_year>', methods=['GET'])
def get_data_by_year_range(start_year, end_year):
    result = [record for record in data if start_year <= record['Year'] <= end_year]
    if result:
        return jsonify(result), 200
    else:
        return jsonify({"error": "No hay datos para el rango solicitado"}), 404

if __name__ == '__main__':
    app.run(debug=True)