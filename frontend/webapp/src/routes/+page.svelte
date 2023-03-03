<script>
  import Logo from "/src/components/Logo.svelte";
  import SearchBar from "/src/components/SearchBar.svelte";
  import SearchResults from "/src/components/SearchResults.svelte";
  import Map from "/src/components/Map.svelte";
  import ResultSection from "/src/components/ResultSection.svelte";
  import PlotlyGraph from '/src/components/PlotlyGraph.svelte';

</script>

<div class="flex flex-col items-center justify-center h-screen w-screen gap-y-4">
  <Logo text="Sentiment Analysis for Tweets on the War in Ukraine"/>
  <Map />
</div>
<div class="flex flex-col items-center w-screen ">
  <PlotlyGraph />
  </div>