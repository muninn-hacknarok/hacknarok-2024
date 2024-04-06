<script lang="ts">
  import { LightSwitch } from '@skeletonlabs/skeleton';
  import Instructions from '../presenter/Instructions.svelte';
  import StageControl from '../presenter/StageControl.svelte';
  import Header from '../presenter/Header.svelte';
  import { isDarkTheme } from '../../stores/globalStore';
</script>

<div class="absolute top-4 right-4">
  <LightSwitch on:click={() => ($isDarkTheme = !$isDarkTheme)} />
</div>

<Header />

<div class="flex">
  <Instructions />
  <StageControl />
  <!-- <QuestionOverview /> -->
</div>
