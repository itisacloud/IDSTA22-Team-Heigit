<script>
    import { onMount, onDestroy } from 'svelte';
    
    export let text = "NoLogo";

    let element;

    let color = '#FFFFFF';
    let colors = [
        '#0057B8',
        '#FFD700'
    ];

    function setRandomColor(){
        let oldColor = `${color}`;
        while (color === oldColor) {
            console.log('new color');
            color = colors[Math.floor(Math.random() * colors.length)];
        }
    }

    onMount(() => {
        setRandomColor();
    });

</script>

<h2 style= "font-size: 7vh;" class="text-6xl font-bold select-none text-white text-[{color}] transition-colors duration-1000 cursor-pointer" bind:this={element} on:click={()=>
setRandomColor()}>{text}</h2>