<script lang="ts">
  import { LightSwitch } from '@skeletonlabs/skeleton';
  import Header from '../presenter/Header.svelte';
  import JoinForm from '../responder/JoinForm.svelte';
  import Question from '../responder/Question.svelte';
  import { respondentStage } from '../../stores/respondentStore';
  import WaitingForQuestion from '../responder/WaitingForQuestion.svelte';

  export let code: string | null = null;
</script>

<div class="absolute top-4 right-4">
  <LightSwitch />
</div>

<Header />

{#if $respondentStage === 'joining'}
  <JoinForm roomId={code} />
{/if}
{#if $respondentStage === 'answering'}
  <Question />
{/if}
{#if $respondentStage === 'waiting'}
  <WaitingForQuestion />
{/if}
