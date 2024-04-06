<script lang="ts">
  import { io } from 'socket.io-client';
  import {
    respondentStage,
    state,
    type QuestionEventData,
  } from '../../stores/respondentStore';
  import { SOCKET_URL } from '../../const';
  import {
    currentQuestion,
    respondentName,
  } from '../../stores/respondentStore';

  export let roomId: string | null;

  function joinRoom() {
    if ($respondentName === '') return;

    state.respondentSocket = io(SOCKET_URL);

    state.respondentSocket?.on('joined_room', () => {
      $respondentStage = 'waiting';
    });

    state.respondentSocket?.on('question', (data: QuestionEventData) => {
      $currentQuestion = data;
      $respondentStage = 'answering';
    });

    state.respondentSocket?.on('connect', () => {
      state.respondentSocket?.emit('join_room', {
        room: roomId,
        name: $respondentName,
      });
    });
  }
</script>

<div class="flex flex-col items-center mt-10">
  <label class="label mb-3">
    <span>Your name</span>
    {$respondentName}
    <input
      class="input"
      type="text"
      placeholder="Your name"
      bind:value={$respondentName}
    />
  </label>
  <button class="btn variant-filled-primary px-12" on:click={joinRoom}
    >Join</button
  >
</div>
