<script lang="ts">
  import { clipboard } from '@skeletonlabs/skeleton';
  import Icon from '@iconify/svelte';
  import { stage } from '../../stores/presenterStore';
  import { StreamingAPIConnection, Symbl } from '@symblai/symbl-web-sdk';
  import { ProgressRadial } from '@skeletonlabs/skeleton';
  import { Socket, io } from 'socket.io-client';
  import type { DefaultEventsMap } from '@socket.io/component-emitter';
  import { SOCKET_URL } from '../../const';

  let link = 'http://localhost:3500/';
  let roomId = '';
  let connection: StreamingAPIConnection;
  let timer: number;
  export let transcriptBatch = '';
  let socket: Socket<DefaultEventsMap, DefaultEventsMap>;

  async function startTranscript() {
    $stage = 'loading';
    transcriptBatch = '';

    socket = io(SOCKET_URL);
    socket.on('room_opened', (data) => {
      console.log('room opened', data);
      handleRoomOpened(data.room);
    });
    socket.on('connect', function () {
      socket?.emit('open_room');
    });

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
      timer = setInterval(() => {
        sendBatch();
        transcriptBatch = '';
      }, questionInterval);
    } catch (e) {
      console.error('Transcript api error: ', e);
      $stage = 'idle';
    }
  }

  async function handleRoomOpened(_roomId: string) {
    roomId = _roomId;
    $stage = 'recording';
  }

  async function sendBatch() {
    console.log('sending batch', transcriptBatch);
    socket?.emit('send_question', {
      room: roomId,
      transcription: [transcriptBatch],
    });
  }

  async function stopTranscript() {
    await connection?.stopProcessing();
    connection?.disconnect();
    if (timer) {
      clearInterval(timer);
    }
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
          <p>{link}{roomId}</p>
          <button use:clipboard={link + roomId} type="button" class="btn-icon"
            ><Icon icon="ph:copy" /></button
          >
        </div>
      </div>
    </div>
  {/if}
</div>
