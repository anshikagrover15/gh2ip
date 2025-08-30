// --- THEME SETUP ---
const themeToggle = document.getElementById('theme-toggle');
const lightIcon = document.getElementById('theme-icon-light');
const darkIcon = document.getElementById('theme-icon-dark');
const docElement = document.documentElement;

const updateThemeIcons = () => {
    if (docElement.classList.contains('dark')) {
        lightIcon.classList.remove('hidden');
        darkIcon.classList.add('hidden');
    } else {
        lightIcon.classList.add('hidden');
        darkIcon.classList.remove('hidden');
    }
};

const setInitialTheme = () => {
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        docElement.classList.add('dark');
    } else {
        docElement.classList.remove('dark');
    }
    updateThemeIcons();
};

themeToggle.addEventListener('click', () => {
    docElement.classList.toggle('dark');
    localStorage.theme = docElement.classList.contains('dark') ? 'dark' : 'light';
    updateThemeIcons();
    updateMapTheme();
});

// --- MAP INITIALIZATION ---
const tileLayers = {
    light: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
    dark: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}'
};
let currentTileLayer;

// Define the geographical bounds for India
const indiaBounds = L.latLngBounds(
    L.latLng(5.0, 67.0), // Southwest corner
    L.latLng(38.0, 99.0)  // Northeast corner
);

const map = L.map('map', {
    center: [20.5937, 78.9629],
    zoom: 5,
    maxBounds: indiaBounds,
    maxBoundsViscosity: 1.0 // This makes the bounds "hard", user cannot drag outside
});

// Set a minimum zoom level to prevent zooming out too far
map.setMinZoom(5);

const updateMapTheme = () => {
    const theme = docElement.classList.contains('dark') ? 'dark' : 'light';
    if (currentTileLayer) {
        map.removeLayer(currentTileLayer);
    }
    currentTileLayer = L.tileLayer(tileLayers[theme], {
        attribution: 'Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012',
        maxZoom: 20
    }).addTo(map);
};

// --- DYNAMIC DATA FROM BACKEND ---
// The 'mapData' variable is now globally available, injected from index.html
const layerGroups = { assets: L.layerGroup(), renewables: L.layerGroup(), demand: L.layerGroup(), transport: L.layerGroup(), optimised: L.layerGroup() };

const icons = {
    plant: (status) => L.divIcon({ className: 'custom-div-icon', html: `<div style="background-color: ${status === 'Existing' ? '#22c55e' : '#f97316'};" class="h-6 w-6 rounded-full border-2 border-white shadow-md"></div>`, iconSize: [24, 24], iconAnchor: [12, 12] }),
    storage: (status) => L.divIcon({ className: 'custom-div-icon', html: `<div style="background-color: ${status === 'Existing' ? '#3b82f6' : '#a855f7'};" class="h-6 w-6 rounded-sm border-2 border-white shadow-md"></div>`, iconSize: [24, 24], iconAnchor: [12, 12] }),
    renewable: (type) => L.divIcon({ className: 'custom-div-icon', html: `<div style="background-color: ${type === 'Solar' ? '#facc15' : '#60a5fa'};" class="h-5 w-5 rounded-full"></div>`, iconSize: [20, 20], iconAnchor: [10, 10] }),
    optimised: () => L.divIcon({ className: 'custom-div-icon', html: `<div class="h-8 w-8 rounded-full bg-yellow-400 border-4 border-white flex items-center justify-center shadow-lg"><svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" /></svg></div>`, iconSize: [32, 32], iconAnchor: [16, 16] })
};

function populateLayers() {
    mapData.assets.forEach(a => L.marker([a.lat, a.lng], { icon: a.type === 'Plant' ? icons.plant(a.status) : icons.storage(a.status) }).bindPopup(`<b>${a.name}</b><br>Type: ${a.type}<br>Status: ${a.status}<br>Capacity: ${a.capacity} MW`).addTo(layerGroups.assets));
    mapData.renewables.forEach(s => L.marker([s.lat, s.lng], { icon: icons.renewable(s.type) }).bindPopup(`<b>${s.name}</b><br>Type: ${s.type}<br>Potential: ${s.potential} MW`).addTo(layerGroups.renewables));
    mapData.demand.forEach(c => L.circle([c.lat, c.lng], { color: '#ef4444', fillColor: '#ef4444', fillOpacity: 0.3, radius: c.demand === 'High' ? 100000 : 50000 }).bindPopup(`<b>${c.name}</b><br>Demand: ${c.demand}`).addTo(layerGroups.demand));
    L.geoJSON(mapData.transport, { style: { color: '#4b5563', weight: 2, dashArray: '5, 5' } }).bindPopup('Proposed Hydrogen Pipeline').addTo(layerGroups.transport);
}

const layerControlCheckboxes = { 
    existingAssets: layerGroups.assets, 
    renewableSources: layerGroups.renewables, 
    demandCenters: layerGroups.demand, 
    transportLogistics: layerGroups.transport 
};

for (const [id, group] of Object.entries(layerControlCheckboxes)) {
    const checkbox = document.getElementById(id);
    if(checkbox.checked) map.addLayer(group);
    checkbox.addEventListener('change', (e) => e.target.checked ? map.addLayer(group) : map.removeLayer(group));
}

document.getElementById('runOptimisation').addEventListener('click', () => {
    const loadingOverlay = document.getElementById('loading-overlay');
    loadingOverlay.classList.remove('hidden');
    layerGroups.optimised.clearLayers();
    setTimeout(() => {
        mapData.optimisedLocations.forEach(loc => L.marker([loc.lat, loc.lng], { icon: icons.optimised() }).bindPopup(`<b>Optimal Location</b><br>Score: ${loc.score}/100<br>Reason: ${loc.reason}`).addTo(layerGroups.optimised));
        map.addLayer(layerGroups.optimised);
        loadingOverlay.classList.add('hidden');
    }, 2000); // This timeout simulates a backend process
});

// --- INITIALIZE ---
setInitialTheme();
updateMapTheme();
populateLayers();