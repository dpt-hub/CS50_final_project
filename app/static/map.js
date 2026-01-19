
var map = L.map('map').setView([40.270, -7.489], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

let addMarker = (lat, lon) => {
    let marker = L.marker([lat, lon]).addTo(map);
}

async function loadClients() {
    let response = await fetch('fetch-clients')
    let clients = await response.json()
    for (let client of clients)
    {
        addMarker(client["latitude"], client["longitude"]);
    }
}

loadClients()
