<script lang="ts">
  import { LightSwitch } from '@skeletonlabs/skeleton';
  import Instructions from '../presenter/Instructions.svelte';
  import StageControl from '../presenter/StageControl.svelte';
  import Transcript from "../presenter/Transcript.svelte";
  import QuestionOverview from "../presenter/QuestionOverview.svelte";
  import Header from '../presenter/Header.svelte';
  import { stage } from '../../stores/presenterStore';
  let transcriptBatch = ""
</script>

<div class="absolute top-4 right-4">
  <LightSwitch />
</div>

<Header />

<div class="flex flex-col">
  <div class="flex flex-row">
    {#if $stage == "recording"}
      <Transcript transcript={transcriptBatch}/>
    {:else}
      <Instructions />
    {/if}
    <StageControl bind:transcriptBatch/>
  </div>
  <QuestionOverview />
</div>
