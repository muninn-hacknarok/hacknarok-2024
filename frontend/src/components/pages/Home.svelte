<script lang="ts">
  import { LightSwitch } from '@skeletonlabs/skeleton';
  import Instructions from '../presenter/Instructions.svelte';
  import StageControl from '../presenter/StageControl.svelte';
  import Transcript from '../presenter/Transcript.svelte';
  import QuestionOverview from '../presenter/QuestionOverview.svelte';
  import Header from '../presenter/Header.svelte';
  import { isDarkTheme } from '../../stores/globalStore';
  import { stage, timer } from '../../stores/presenterStore';
  let transcriptBatch = '';
  let currentPendingSentence = '';
  let customQuestionInterval = 80; // 6-7 seconds shift
</script>

<div class="absolute top-4 right-4">
  <LightSwitch on:click={() => ($isDarkTheme = !$isDarkTheme)} />
</div>

<div class="absolute top-4 left-4">
  <span>{$timer}s</span>
</div>

<Header />

<div class="flex flex-col">
  <div class="flex flex-row">
    {#if $stage == 'recording'}
      <Transcript transcript={transcriptBatch + currentPendingSentence} />
    {:else}
      <Instructions />
    {/if}
    <!-- <input bind:value={customQuestionInterval} /> -->
    <StageControl
      bind:transcriptBatch
      bind:currentPendingSentence
      bind:customQuestionInterval
    />
  </div>
  <QuestionOverview />
</div>
