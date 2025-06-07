const map = L.map("map", {
    center: [-19.92, -43.94],
    crs: L.CRS.EPSG3857,
    zoom: 13,
    zoomControl: true,
    preferCanvas: false
});

const baseTileLayer = L.tileLayer(
    "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
        minZoom: 0,
        maxZoom: 18,
        maxNativeZoom: 20,
        noWrap: false,
        attribution: "&copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors &copy; <a href=\"https://carto.com/attributions\">CARTO</a>",
        subdomains: "abcd",
        detectRetina: false,
        tms: false,
        opacity: 1,
    }
);
baseTileLayer.addTo(map);

function distritosStyle(feature) {
    return { color: "green", fillOpacity: 0.1, weight: 1 };
}

function onEachDistrito(feature, layer) {
    // Nada ainda
}

const distritosLayer = L.geoJson(null, {
    style: distritosStyle,
    onEachFeature: onEachDistrito
});

function adicionarDistritos(data) {
    distritosLayer.addData(data);
}

distritosLayer.addTo(map);

fetch("regiao_bh.geojson")
    .then(response => response.json())
    .then(data => adicionarDistritos(data));

const layersControl = L.control.layers(
    { "CartoDB Positron": baseTileLayer },
    { "Distritos": distritosLayer },
    {
        position: "topright",
        collapsed: true,
        autoZIndex: true,
    }
).addTo(map);

function plotarEstabelecimentos(bounds) {
    const sw = bounds.getSouthWest();
    const ne = bounds.getNorthEast();

    const apenasComidaDiButeco = document.getElementById("comidaCheckbox").checked;

    fetch("http://127.0.0.1:5000/filtrar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            sw: { lat: sw.lat, lng: sw.lng },
            ne: { lat: ne.lat, lng: ne.lng },
            comida_di_buteco: apenasComidaDiButeco
        })
    })
    .then(response => response.json())
    .then(estabelecimentos => {
        if (window.restaurantesGroup) map.removeLayer(window.restaurantesGroup);
        if (window.baresGroup) map.removeLayer(window.baresGroup);

        const restauranteIcon = L.icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        });

        const barIcon = L.icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        });

        const goldenBarIcon = L.icon({
            iconUrl: './imagens/marker-icon-2x-gold-bar.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        });
        const goldenRestIcon = L.icon({
            iconUrl: './imagens/marker-icon-2x-gold-rest.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        });


        // Usa marker cluster groups
        window.restaurantesGroup = L.markerClusterGroup({
            chunkedLoading: true,
            maxClusterRadius: 30
        });
        window.baresGroup = L.markerClusterGroup({
            chunkedLoading: true,
            maxClusterRadius: 30
        });

        estabelecimentos.forEach(estab => {
            console.log("Estab:", estab);
            const isButeco = estab.comida_di_buteco;
            console.log(isButeco? "1" : "0")
            const lat = parseFloat(estab.LATITUDE);
            const lon = parseFloat(estab.LONGITUDE);
            const nome = estab.NOME_FANTASIA || estab.NOME || "Sem nome";
            const endereco = `${estab.DESC_LOGRADOURO || ''} ${estab.NOME_LOGRADOURO || ''}, ${estab.NUMERO_IMOVEL || ''}, ${estab.NOME_BAIRRO || ''}`;
            const inicio = estab.DATA_INICIO_ATIVIDADE || "Desconhecida";
            const alvara = estab.IND_POSSUI_ALVARA || "Não especificado";

            let popup = `<div class="text-center">`;
            popup += `<strong>${nome}</strong><br>${endereco}<br>Início: ${inicio}<br>Alvará: ${alvara}<br><br>`;
            if (isButeco){
                popup += `
                    <img src="imagens/${estab["ID_ATIV_ECON_ESTABELECIMENTO"]}.jpg" class="img-fluid rounded mb-2" alt="Petisco"><br>
                    <strong>${estab["Nome Petisco"]}</strong><br>
                    <button class="btn btn-sm btn-outline-info mt-2" onclick="mostrarDescricao('${estab["Descricao"].replace(/'/g, "\\'")}')">ℹ️ Ver Descrição</button>
                `;
            }
            popup += `</div>`;
            const isBar = estab.DESCRICAO_CNAE_PRINCIPAL && estab.DESCRICAO_CNAE_PRINCIPAL.includes("BARES");
            
            let marker;
            if(isButeco){
                marker = L.marker([lat, lon], {
                    icon: isBar ? goldenBarIcon : goldenRestIcon
                }).bindPopup(popup);
            }else{
                marker = L.marker([lat, lon], {
                    icon: isBar ? barIcon : restauranteIcon
                }).bindPopup(popup);
            }

            if (isBar) {
                window.baresGroup.addLayer(marker);
            } else {
                window.restaurantesGroup.addLayer(marker);
            }
        });

        window.restaurantesGroup.addTo(map);
        window.baresGroup.addTo(map);

        if (window.layerControl) map.removeControl(window.layerControl);

        window.layerControl = L.control.layers(null, {
            "Restaurantes": window.restaurantesGroup,
            "Bares": window.baresGroup
        }).addTo(map);
    })
    .catch(error => {
        console.error("Erro ao buscar estabelecimentos:", error);
    });
}

const drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

const drawControl = new L.Control.Draw({
    edit: { featureGroup: drawnItems, remove: true },
    draw: {
        polygon: false,
        polyline: false,
        circle: false,
        circlemarker: false,
        marker: false,
        rectangle: {
            shapeOptions: {
                color: '#007bff',
                weight: 3,
                fillOpacity: 0.1
            }
        }
    }
});

map.addControl(drawControl);

map.on(L.Draw.Event.CREATED, function (e) {
    const layer = e.layer;
    drawnItems.clearLayers();
    drawnItems.addLayer(layer);
    plotarEstabelecimentos(layer.getBounds());
});

map.on(L.Draw.Event.EDITED, function (event) {
    event.layers.eachLayer(layer => {
        if (layer instanceof L.Rectangle) {
            plotarEstabelecimentos(layer.getBounds());
        }
    });
});

map.on(L.Draw.Event.DELETED, function () {
    if (window.restaurantesGroup) map.removeLayer(window.restaurantesGroup);
    if (window.baresGroup) map.removeLayer(window.baresGroup);
    if (window.layerControl) map.removeControl(window.layerControl);
});

//Inserir o conteúdo no modal
function mostrarDescricao(texto) {
    const modalBody = document.getElementById("descricaoModalBody");
    modalBody.textContent = texto;
    const modal = new bootstrap.Modal(document.getElementById("descricaoModal"));
    modal.show();
}

// Chamar novamente a função para quando marcar ou desmarcar o checkbox
function atualizarFiltroComida(){
    if(drawnItems.getLayers().length > 0){
        const bounds = drawnItems.getLayers()[0].getBounds();
        plotarEstabelecimentos(bounds);
    }
}