let Old_start_marker;
var map = L.map("map").setView([36.7538, 3.0588], 12);
var Osm = L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

// Style for the GeoJSON layer
var geojsonStyle = {
  color: "#10008d", // Border color
  weight: 2, // Border width
  fillOpacity: 0, // No fill
};

const geojsonStyle2 = {
  color: "#FF5733", // Orange color for the path
  weight: 5, // Increase the weight of the line
  opacity: 0.9, // Set opacity to 80%
  lineCap: "round", // Set line cap to round for smoother appearance
};

// Create GeoJSON layer with the specified style
var geojsonLayer = L.geoJSON(myData, {
  style: geojsonStyle,
}).addTo(map);

// Fit the map view to the boundaries of the GeoJSON data
map.fitBounds(geojsonLayer.getBounds());

// Create an empty GeoJSON object to hold the hospital data
var hospitalsGeoJSON = {
  type: "FeatureCollection",
  features: [],
};

// Populate the GeoJSON object with hospital data
for (let hospital of hospitals["hospitals"]) {
  var servicesString = hospital.services.slice(0, 3).join(", ") + (hospital.services.length > 3 ? "..." : "");
  var feature = {
    type: "Feature",
    geometry: {
      type: "Point",
      coordinates: [hospital.x, hospital.y],
    },
    properties: {
      name: hospital.name,
      services: servicesString,
    },
  };
  hospitalsGeoJSON.features.push(feature);
}

// Define the hospital icon
var hospitalIcon = L.icon({
  iconUrl: "../static/images/hospital.png", // URL to your hospital icon image
  iconSize: [32, 32], // Size of the icon
  iconAnchor: [16, 32], // Anchor point of the icon
});

// Create a Leaflet layer from the GeoJSON object
var hospitalLayer = L.geoJSON(hospitalsGeoJSON, {
  pointToLayer: function (feature, latlng) {
    return L.marker(latlng, { icon: hospitalIcon });
  },
});

// Bind popups to markers with hospital information
hospitalLayer.bindPopup(function (layer) {
  var props = layer.feature.properties;
  return "<b>" + props.name + "</b><br>Services: " + props.services;
});

// Add the hospital layer to the map
hospitalLayer.addTo(map);

let startMarker, endMarker;
let currentPathLayer; // Variable to hold the current path layer

function addFeatureWithDelay(feature, delay) {
  return new Promise((resolve) => {
    setTimeout(() => {
      const newPathLayer = L.geoJSON(feature, {
        style: geojsonStyle2,
      }).addTo(map);
      resolve(newPathLayer); 
    }, delay);
  });
}

async function addFeatures() {
  if (currentPathLayer || Old_start_marker) {
    map.removeLayer(currentPathLayer); 
    map.removeLayer(Old_start_marker);
  }
  if (myLine.o_path == null) {
    alert("No path exist inside this area");
    map.removeLayer(marker);
    return;
  }
  let newPathLayerGroup = L.layerGroup(); // for the new path

  if (myLine.paths == null) {
    geojsonStyle2["color"] = "#5c00ff";
    for (let line of myLine.o_path["features"]) {
      let newPathLayer = await addFeatureWithDelay(line.geometry, 0);
      newPathLayerGroup.addLayer(newPathLayer);
    }
    addStartMarker();
  } else {
    if (myLine.vis_type == "local search") {
      let i = 0;
      const arr_cols = ["#FF5733", "#E85644", "#D24E55", "#BB4666", "#A53D77", "#8E3488", "#782B99", "#6122AA", "#4B19BB", "#3410CC", "#5c00ff"];
      for (let path of myLine.paths) {
        if (i < 10) {
          geojsonStyle2["color"] = arr_cols[i];
        }
        let newPathLayer = await addFeatureWithDelay(path, 2000);
        newPathLayerGroup.addLayer(newPathLayer);
        i++;
      }
    } else if (myLine.vis_type == "graph search") {
      geojsonStyle2["color"] = "#FF5733";
      for (let path of myLine.paths) {
        for (let line of path["features"]) {
          let newPathLayer = await addFeatureWithDelay(line.geometry, 0);
          newPathLayerGroup.addLayer(newPathLayer);
        }
      }
    }

    geojsonStyle2["color"] = "#5c00ff";
    for (let line of myLine.o_path["features"]) {
      let newPathLayer = await addFeatureWithDelay(line.geometry, 0);
      newPathLayerGroup.addLayer(newPathLayer);
    }
    addStartMarker();
  }

  currentPathLayer = newPathLayerGroup; // Update the reference to the current path layer
  currentPathLayer.addTo(map); 
}

function addStartMarker() {
  const startPoint = myLine.start;
  startMarker = L.marker([startPoint[0], startPoint[1]]).addTo(map);
  Old_start_marker = startMarker;
  startMarker.bindPopup("This is your location").openPopup();
}

var marker = null; // Variable to hold the marker
let latitude_1 = 0;
let longitude_1 = 0;

map.on("click", async function (e) {
  latitude_1 = e.latlng.lat;
  longitude_1 = e.latlng.lng;
  if (marker !== null) {
    map.removeLayer(marker);
  }
  const requestData = {
    latitude: latitude_1,
    longitude: longitude_1
  };

  let config = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestData),
  };

  try {
    const res = await fetch("/bound_checking", config);
    const data = await res.json();
    if (data.is_inside_algiers) {
      marker = L.marker(e.latlng).addTo(map);
    } else {
      alert("Please select a location inside Algiers");
    }
  } catch (error) {
    console.error("Error fetching data:", error);
  }
});

let myLine;
document.querySelector(".button").addEventListener("click", function () {
  let speciality_1 = document.querySelector(".current").textContent;
  let special_general = document.querySelector("#switch").checked;
  let search_type = document.querySelector("#search-algo").value;
  let optimal = getCheckedRadioButton();

  if (!speciality_1 || speciality_1 == "choose") {
    alert("Enter a speciality");
    return;
  }
  if (latitude_1 == 0 || longitude_1 == 0) {
    alert("Enter a starting place");
    return;
  }

  const requestData = {
    latitude: latitude_1,
    longitude: longitude_1,
    speciality: speciality_1,
    special_general: special_general,
    search_strat: search_type,
    search_tpe: optimal
  };

  document.querySelector(".overlay").classList.remove("is-on");
  document.querySelector(".container").classList.add("active");
  document.querySelector(".buttons").classList.add("hide");
  document.querySelector(".overlay").classList.add("hide");
  document.querySelector("#map").classList.add("hide");
  document.querySelector("body").style.display = "block";

  fetch("/main", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestData),
  })
    .then((response) => response.json())
    .then((data) => {
      myLine = data;
      if (myLine) {
        document.querySelector(".container").classList.remove("active");
        document.querySelector(".buttons").classList.remove("hide");
        document.querySelector(".overlay").classList.remove("hide");
        document.querySelector("#map").classList.remove("hide");
        document.querySelector("body").style.display = "flex";
        addFeatures();
      } else {
        console.log("No data");
      }
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
});

function getCheckedRadioButton() {
  const radios = document.getElementsByName('visualization');
  for (let radio of radios) {
    if (radio.checked) {
      return radio.value;
    }
  }
  return null;
}

document.querySelector('form').addEventListener("submit",(e)=>{
  e.preventDefault()
})
