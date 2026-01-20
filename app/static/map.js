
var map = L.map('map').setView([40.270, -7.489], 13);

var customMarker;
var tempMarker;
async function loadCustomMarkers() {
    let url = "fetch/logo"
    const options = {
        method: "GET"
    }
    let response = await fetch(url, options)
    let imageBlob = await response.blob();
    let imageObjectURL = URL.createObjectURL(imageBlob);

    customMarker = L.icon({
    iconUrl: imageObjectURL,
    iconSize: [40, 40],
    iconAnchor: [20, 40],
    popupAnchor: [0, -35],
    });

    url = 'fetch/tempmarker'
    response = await fetch(url, options)
    imageBlob = await response.blob()
    imageObjectURL = URL.createObjectURL(imageBlob);

    tempMarker = L.icon({
    iconUrl: imageObjectURL,
    iconSize: [40, 40],
    iconAnchor: [20, 40],
    popupAnchor: [0, -35],
    });
}

loadCustomMarkers()

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

let addMarker = (lat, lon) => {
    let marker = L.marker([lat, lon], {icon: customMarker}).addTo(map);
    return marker
}

async function loadClients() {
    let response = await fetch('fetch/clients')
    let clients = await response.json()
    for (let client of clients)
    {
        let marker = addMarker(client["latitude"], client["longitude"]);
        marker.bindPopup(`<b>Name:</b> ${client["name"]}<br><b>Type:</b> ${client["type"]}`)
    }
}

loadClients()

let isMarkerAdded = false;
let addedMarker;
let onMapClick = (e) => {
    if (!isMarkerAdded)
    {
        addedMarker = L.marker(e.latlng, {icon: tempMarker}).addTo(map);
        isMarkerAdded = true;
    }
    else
    {
        addedMarker.remove();
        addedMarker = L.marker(e.latlng, {icon: tempMarker}).addTo(map);
    }
}

map.on("click", onMapClick)

let addClientButton = document.querySelector('#addclient')
addClientButton.addEventListener("click", () => {
    if(!isMarkerAdded)
    {
        alert('Select a point on the map.')
    }
    else
    {
        addedMarker.bindPopup('<form method="post"><h6 class="fs-5 fw-bold">Add New Client:</h6><div class="form-group mb-2"><label for="name">Name:</label><input id="name" name="name" class="form-control" type="text" required></div><div class="form-group mb-2"><label for="type">Type:</label><input id="type" name="type" class="form-control" type="text" required></div><input type="hidden" name="latitude" value="" id="latitude"><input type="hidden" name="longitude" value="" id="longitude"><div class="d-grid col-2 mx-auto justify-content-center"><button class="btn btn-primary" type="submit">Submit</button></div></form>')
        .openPopup()
        let latInput = document.getElementById('latitude')
        let lonInput = document.getElementById('longitude')
        latInput.value = addedMarker.getLatLng()["lat"]
        lonInput.value = addedMarker.getLatLng()["lng"]
    }
})