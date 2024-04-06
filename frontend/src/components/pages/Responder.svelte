<script lang="ts">
  import { LightSwitch } from '@skeletonlabs/skeleton';
  import Header from '../presenter/Header.svelte';
  import JoinForm from '../responder/JoinForm.svelte';
  import Question from '../responder/Question.svelte';

  export let code: string | null = null;
</script>

<div class="absolute top-4 right-4">
  <LightSwitch />
</div>

<Header />

<!-- <JoinForm /> -->
<Question />
