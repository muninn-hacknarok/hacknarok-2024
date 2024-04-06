<script lang="ts">
  import { clipboard } from '@skeletonlabs/skeleton';
  import Icon from '@iconify/svelte';
  import { stage } from '../../stores/presenterStore';
  import { StreamingAPIConnection, Symbl } from '@symblai/symbl-web-sdk';
  import { ProgressRadial } from '@skeletonlabs/skeleton';

  const link = 'https://muninn.com/5GHI83';
  let connection: StreamingAPIConnection;
  let timer = null;
  let transcriptBatch = '';

  async function startTranscript() {
    $stage = 'loading';
    transcriptBatch = '';
    try {
      // Symbl recommends replacing the App ID and App Secret with an Access Token for authentication in production applications.
      // For more information about authentication see https://docs.symbl.ai/docs/developer-tools/authentication/.
      const symbl = new Symbl({
        appId:
          '654f676f6c7a644945517967653158564b69744f67784676357937556b314f46',
        appSecret:
          '44414a356e4e485f6d4c56704e3141732d6439526a5375576a4f4472766663487043305f3249655557544f726c6f6637496f37425458534539664e4c30385764',
        // accessToken: '<your Access Token>' // for production use
      });

      // Open a Streaming API WebSocket Connection and start processing audio from your input device.
      connection = await symbl.createAndStartNewConnection();

      // Retrieve real-time transcription from the conversation.
      connection.on('speech_recognition', (speechData) => {
        const name = speechData.user ? speechData.user.name : 'User';
        const transcript = speechData.punctuated.transcript;
        // console.log(`${name}: `, speechData);
        if (speechData.isFinal) {
          console.log(transcript);
          transcriptBatch += transcript + ' ';
        }
      });

      const questionInterval = 1000 * 60;
      timer = setInterval(() => {}, questionInterval);

      $stage = 'recording';
    } catch (e) {
      console.error('Transcript api error: ', e);
      $stage = 'idle';
    }
  }

  async function stopTranscript() {
    await connection?.stopProcessing();
    connection?.disconnect();
    $stage = 'idle';
  }
</script>

<div class="flex-1">
  {#if $stage === 'idle'}
    <div class="stage-start mt-16 flex justify-center">
      <button
        type="button"
        class="btn variant-filled-primary m-2"
        on:click={startTranscript}
      >
        <div class="bg-red-500 w-3 h-3 rounded-full"></div>
        <span>Start recording</span>
      </button>
    </div>
  {/if}
  {#if $stage === 'loading'}
    <div class="stage-loading mt-16 flex justify-center">
      <ProgressRadial
        stroke={50}
        meter="stroke-primary-500"
        track="stroke-primary-500/30"
      />
    </div>
  {/if}
  {#if $stage === 'recording'}
    <div class="stage-stop mt-16 flex justify-center">
      <button
        type="button"
        class="btn variant-filled-primary m-2"
        on:click={stopTranscript}
      >
        <div class="bg-white w-3 h-3"></div>
        <span>Stop recording</span>
      </button>
    </div>
    <div class="stage-link flex justify-center mt-14">
      <div class="w-[400px]">
        <h3 class="text-lg mb-4">Share this link with responders:</h3>
        <div
          class="card flex items-center justify-between variant-soft-primary px-4"
        >
          <p>{link}</p>
          <button use:clipboard={link} type="button" class="btn-icon"
            ><Icon icon="ph:copy" /></button
          >
        </div>
      </div>
    </div>
  {/if}
</div>
