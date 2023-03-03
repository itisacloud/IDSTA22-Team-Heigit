<script>
    import Plotly from 'plotly.js-dist';
    import {onMount, onDestroy} from 'svelte';
    import {timeInterval, selectedRegions, selectedLayers} from "/src/components/Map.svelte";
    import axios from "axios";
    import {timeIntervall} from "./Map.svelte";

    let graphData = null;
    let graphDiv;
    let graph = null;

    async function loadGraphData() {
        let request_data = {"interval": timeIntervall, "layer": selectedLayers, "name": selectedRegions}
        try {
            let {data, status} = await axios.post('http://localhost:2999/plot', request_data);
            if (status != 200) {
                alert('Error fetching search results!');
                return;
            }
            graphData = data;
            graph = 1;
            if (graph !== null) {
                Plotly.newPlot(graphDiv, graphData.data, graphData.layout);
            }
        }
        catch
            (error)
            {
                alert('Error fetching search results! Probably the API is not ready yet.');
                return;
            }

        }


    onMount(() => {
        loadGraphData();
    });


</script>

<button on:click={loadGraphData}>Reload Graph</button>


<div bind:this={graphDiv}></div>
