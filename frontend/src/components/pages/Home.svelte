<script lang="ts">
  import { clipboard } from '@skeletonlabs/skeleton';
  import Icon from '@iconify/svelte';
  import { LightSwitch } from '@skeletonlabs/skeleton';

  const link = 'https://muninn.com/5GHI83';
</script>

<div class="absolute top-4 right-4">
  <LightSwitch />
</div>

<div class="flex space-x-3 items-center justify-center mt-6 mb-3">
  <h1 class="text-[40px]">Muninn</h1>
  <img class="w-10 h-10" src="assets/white_raven.png" alt="" />
</div>
<h4 class="text-center mb-6">
  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
</h4>

<div class="flex">
  <!-- How to use the app -->
  <div class="flex-1">
    <div class="card">
      <h4>How to use Muninn?</h4>
      <ol>
        <li>1. Click "start recording"</li>
        <li>2. Allow access to microphone</li>
        <li>3. Send generated link to respondents</li>
      </ol>
    </div>
  </div>
  <!-- Functionality -->
  <div class="flex-1">
    <div class="stage-start">
      <button type="button" class="btn variant-filled-primary m-2">
        <div class="bg-red-500 w-3 h-3 rounded-full"></div>
        <span>Start recording</span>
      </button>
    </div>
    <div class="stage-stop">
      <button type="button" class="btn variant-filled-primary m-2">
        <div class="bg-white w-3 h-3"></div>
        <span>Stop recording</span>
      </button>
    </div>
    <div class="stage-link">
      <div
        class="card flex items-center justify-between variant-filled-primary px-4 max-w-sm"
      >
        <p>{link}</p>
        <button use:clipboard={link} type="button" class="btn-icon"
          ><Icon icon="ph:copy" /></button
        >
      </div>
    </div>
  </div>
</div>
