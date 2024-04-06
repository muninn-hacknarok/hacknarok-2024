<script lang="ts">
  import { LightSwitch } from '@skeletonlabs/skeleton';
  import Instructions from '../presenter/Instructions.svelte';
  import StageControl from '../presenter/StageControl.svelte';
  import Header from '../presenter/Header.svelte';
</script>

<div class="absolute top-4 right-4">
  <LightSwitch />
</div>

<Header />

<div class="flex">
  <Instructions />
  <StageControl />
  <QuestionOverview />
</div>
