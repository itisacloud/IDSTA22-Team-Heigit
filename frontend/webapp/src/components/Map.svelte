<script>
    import axios from 'axios';
    import L from 'leaflet';
    import {setContext, getContext, onMount, onDestroy} from "svelte";
    import {searchResultsStore} from "/src/stores/searchResultsStore.js";
    import testData from '/src/components/test.json';
    import testData2 from '/src/components/test2.json';

    export let timeIntervall = "";
    export let selectedRegions = [];
    export let selectedLayers = [];
    let geojson;
    let geojson2;
    let geojson3;

    let map;
    let osm;
    var myStyle = {
        fillColor: "#EEF200",
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };

    function highlightFeature(e) {
        const layer = e.target;
        layer.setStyle({
            weight: 5,
            color: '#666',
            dashArray: '',
            fillOpacity: 0.7
        });
        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
            layer.bringToFront();
        }
    }

    function resetHighlight(e) {
        if (map.hasLayer(geojson)) {
            geojson.resetStyle(e.target);
        }
        if (map.hasLayer(geojson2)) {
            geojson2.resetStyle(e.target);
        }
        if (map.hasLayer(geojson3)) {
            geojson3.resetStyle(e.target);
        }
    }

    async function selectStyle(e) {
        // change value of mapCheck in html to signalize intern area was selected
        //update_url("id", e.target.feature.id)
        //const s = document.getElementById("mapCheck");
        //s.innerHTML = "selected";
        // TODO style selected id
        // alert("I will be red");
        const layer = e.target;
        const regionName = e.target.feature.properties.NUTS_NAME;
        let selectedFeature = e.target.feature;
        let selectedFeatureLayer = L.geoJSON(selectedFeature, {
            style: function (feature) {
                return {
                    color: 'red',
                    fillColor: '#f03',
                    fillOpacity: 0.5
                };
            }
        }).addTo(map);
        selectedRegions.push(regionName);
        let lvl = document.getElementById("cardtype").value;
        if (lvl === "Federal States") selectedLayers.push("NAME_1")
        if (lvl === "Government Districts") selectedLayers.push("NAME_2")
        if (lvl === "County Districts") selectedLayers.push("NAME_3")
        selectedFeatureLayer.on("click", function (e) {
            for (const [key, value] of Object.entries(e.target._layers)) {
                selectedRegions = selectedRegions.filter(e => e !== value.feature.properties.NUTS_NAME);
            }
            let ind = selectedRegions.indexOf(regionName);
            map.removeLayer(selectedFeatureLayer);
            selectedRegions.splice(ind, ind + 1);
            selectedLayers.splice(ind, ind + 1);
        })

    }

    function onEachFeature(feature, layer) {
        layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight,
            click: selectStyle
        });
    }

    function chooseLevel() {
        //TODO: remove layer on level change
        selectedLayers = [];
        selectedRegions = [];
        const level = document.getElementById("cardtype");
        if (level.value === "Federal States") {
            if (map.hasLayer(geojson3)) {
                console.log("layer already added");
            } else {
                map.eachLayer(function (layer) {
                    if (layer._url === "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png ") {
                    } else {
                        map.removeLayer(layer);
                    }
                });
                map.addLayer(geojson3);
            }
        }
        if (level.value === "Government Districts") {
            if (map.hasLayer(geojson2)) {
                console.log("layer already added");
            } else {
                map.eachLayer(function (layer) {
                    if (layer._url === "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png ") {
                    } else {
                        map.removeLayer(layer);
                    }
                });
                map.addLayer(geojson2);
            }
        }
        if (level.value === "County Districts") {
            if (map.hasLayer(geojson)) {
                console.log("layer already added");
            } else {
                map.eachLayer(function (layer) {
                    if (layer._url === "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png ") {
                    } else {
                        map.removeLayer(layer);
                    }
                });
                map.addLayer(geojson);
            }
        }
    };
    onMount(() => {
        map = L.map("map", {
            center: [52, 8],
            zoom: 5
        });
        let osm = L.tileLayer("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png ", {
            attribution:
                'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
        }).addTo(map);

                fetch("http://localhost:3000/data/nuts3_germany.geojson")
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                geojson = L.geoJSON(data, {
                    style: myStyle,
                    onEachFeature: onEachFeature
                })
            });
        fetch("http://localhost:3000/data/nuts3_germany.geojson")
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                geojson = L.geoJSON(data, {
                    style: myStyle,
                    onEachFeature: onEachFeature
                })
            });
        fetch("http://localhost:3000/data/nuts2_germany.geojson")
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                geojson2 = L.geoJSON(data, {
                    style: myStyle,
                    onEachFeature: onEachFeature
                })
            });
        fetch("http://localhost:3000/data/nuts1_germany.geojson")
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                geojson3 = L.geoJSON(data, {
                    style: myStyle,
                    onEachFeature: onEachFeature
                }).addTo(map);
            });



    });
function chooseTimeIntervall() {
    timeIntervall = document.getElementById("timeIntervall");
}
            async function requestApi(array) {
            timeIntervall = document.getElementById("timeIntervall");
            console.log(timeIntervall.value, selectedRegions, selectedLayers)
                let request_data = {"interval": timeIntervall,"layer":"", "name": selectedRegions}
            try {
                let {data, status} = await axios.post('http://localhost:2999/plot', request_data);
                if (status != 200) {
                    alert('Error fetching search results!');
                    return;
                }
                searchResultsStore.set(data.results);
            } catch (error) {
                alert('Error fetching search results! Probably the API is not ready yet.');
                return;
            }
        }
</script>
<svelte:head>
    <link
            rel="stylesheet"
            href="https://unpkg.com/leaflet@1.6.0/dist/leaflet.css"
            integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ=="
            crossorigin=""/>
</svelte:head>
<style>
    .map {
        height: 30vh;
        width: 50vw;
    }
</style>
    <div class="select">
        <select class="minimal" id="cardtype" on:change={chooseLevel}>
            <option value="Federal States">Federal States</option>
            <option value="Government Districts">Government Districts</option>
            <option value="County Districts">County Districts</option>
        </select>
    </div>

    <div style="size: 2vh;" class="select">
        <select class="minimal" id="timeIntervall" on:change={chooseTimeIntervall}>
            <option value="Monthly">Monthly</option>
            <option value="Weekly">Weekly</option>
            <option value="Daily">Daily</option>
        </select>
    </div>
    <div class='map' id="map">
        <slot></slot>
    </div>
    <h3 style="font-size: 2vh;">Run analysis.</h3>
