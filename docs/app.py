from flask import Flask, request, jsonify
from flask_cors import CORS
import csv

app = Flask(__name__)
CORS(app)


class KDNode:
    def __init__(self, point, data, left=None, right=None):
        self.point = point
        self.data = data
        self.left = left
        self.right = right

def build_kdtree(points, depth=0):
    if not points:
        return None

    k = 2
    axis = depth % k
    points.sort(key=lambda x: x[0][axis])
    median = len(points) // 2

    return KDNode(
        point=points[median][0],
        data=points[median][1],
        left=build_kdtree(points[:median], depth + 1),
        right=build_kdtree(points[median + 1:], depth + 1)
    )

def range_query_kdtree(node, bounds, depth=0, results=None):
    if results is None:
        results = []

    if node is None:
        return results

    lat, lon = node.point
    (lat_min, lon_min), (lat_max, lon_max) = bounds

    if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
        results.append(node.data) #cpa q é append

    axis = depth % 2
    coord = lat if axis == 0 else lon

    if coord >= (lat_min if axis == 0 else lon_min):
        range_query_kdtree(node.left, bounds, depth + 1, results)
    if coord <= (lat_max if axis == 0 else lon_max):
        range_query_kdtree(node.right, bounds, depth + 1, results)

    return results

def carregar_dados_csv(filepath):
    estabelecimentos = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            try:
                lat = float(row['LATITUDE'])
                lon = float(row['LONGITUDE'])
                estabelecimentos.append(((lat, lon), row))
            except:
                continue
    return estabelecimentos

def carregar_cdb_csv(filepath):
    cdb_dict = {}
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            cdb_dict[row["ID_ATIV_ECON_ESTABELECIMENTO"]] = row
    return cdb_dict

# Carrega os dados do comida di buteco para um dicionário
cdb_dados = carregar_cdb_csv("docs/comida_di_buteco.csv")

# Carrega e constrói a KD-Tree {Feito apenas ao iniciar o servidor}
dados = carregar_dados_csv("docs/bares_com_cdb.csv")
arvore = build_kdtree(dados)

@app.route("/filtrar", methods=["POST"])
def filtrar():
    payload = request.get_json()
    sw = payload["sw"]
    ne = payload["ne"]

    lat_min, lon_min = sw["lat"], sw["lng"]
    lat_max, lon_max = ne["lat"], ne["lng"]

    comida_filter = payload.get("comida_di_buteco", False)

    resultados = range_query_kdtree(arvore, ((lat_min, lon_min), (lat_max, lon_max)))


    for i in range(len(resultados)):
        id_estab = resultados[i]["ID_ATIV_ECON_ESTABELECIMENTO"]
        if id_estab in cdb_dados:
            resultados[i] = {**resultados[i], **cdb_dados[id_estab]}
            resultados[i]["comida_di_buteco"] = True
        else:
            resultados[i]["comida_di_buteco"] = False

    # Aplica o filtro (se estiver marcado)
    if comida_filter:
        resultados = [r for r in resultados if r["comida_di_buteco"]]

    return jsonify(resultados)

if __name__ == "__main__":
    app.run(debug=True)