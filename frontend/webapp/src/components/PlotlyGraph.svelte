<script>
  import Plotly from 'plotly.js-dist';
  import { onMount, onDestroy } from 'svelte';

  let graphData = null;
  let graphDiv;
  let graph = null;

  function loadGraphData() {
    fetch('/src/components/test2.json')
      .then(response => response.json())
      .then(data => {
        graphData = data;
        graph = 1;
        if (graph !== null) {
          Plotly.newPlot(graphDiv, graphData.data, graphData.layout);
        }
      });
  }

  onMount(() => {
    loadGraphData();
  });


</script>

<button on:click={loadGraphData}>Reload Graph</button>


  <div bind:this={graphDiv}></div>
