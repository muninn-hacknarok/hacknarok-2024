<script lang="ts">
  import {
    clipboard,
    modalStore,
    type ModalSettings,
  } from '@skeletonlabs/skeleton';
  import Icon from '@iconify/svelte';
  import {
    connectedUsers,
    stage,
    storedQuestions,
    timer,
  } from '../../stores/presenterStore';
  import { StreamingAPIConnection, Symbl } from '@symblai/symbl-web-sdk';
  import { ProgressRadial } from '@skeletonlabs/skeleton';
  import { Socket, io } from 'socket.io-client';
  import type { DefaultEventsMap } from '@socket.io/component-emitter';
  import { SOCKET_URL } from '../../const';
  import { SlideToggle } from '@skeletonlabs/skeleton';

  let link = import.meta.env.VITE_CURRENT_URL;
  let roomId = '';
  let connection: StreamingAPIConnection;
  let questionIntervalTimer: number;
  let timerIntervalTimer: number;
  export let customQuestionInterval: number;
  export let transcriptBatch = '';
  export let currentPendingSentence = '';
  let socket: Socket<DefaultEventsMap, DefaultEventsMap>;
  let autoConfirm = false;
  let startTime: number;

  interface Question {
    id: string;
    question: string;
    room: string;
    correct_response_index: number;
    answers: string[];
  }

  interface ResponseEventData {
    id: string;
    name: string;
    response: number;
  }

  async function startTranscript() {
    startTime = Date.now();
    timerIntervalTimer = setInterval(() => {
      $timer = Math.round((Date.now() - startTime) / 1000);
    }, 1000);
    console.log('start transcript');
    $stage = 'loading';
    transcriptBatch = '';
    currentPendingSentence = '';
    $storedQuestions = {};
    $connectedUsers = [];

    socket = io(import.meta.env.VITE_SOCKET_URL);
    socket.on('room_opened', (data) => {
      console.log('room opened', data);
      handleRoomOpened(data.room);
    });
    socket.on('new_response', (data: ResponseEventData) => {
      console.log('new response', data);
      handleNewResponse(data);
    });
    socket.on('user_joined', (data: { name: string }) => {
      console.log('user joined', data);
      onUserJoined(data.name);
    });
    socket.on('question_generated', (data: Question) => {
      handleGeneratedQuestion(data);
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
        const transcript = speechData.punctuated.transcript;
        console.log(transcript);
        if (speechData.isFinal) {
          console.log(transcript);
          transcriptBatch += transcript + ' ';
          currentPendingSentence = '';
        } else {
          currentPendingSentence = transcript;
        }
      });

      const questionInterval = 1000 * customQuestionInterval;
      questionIntervalTimer = setInterval(() => {
        if (transcriptBatch.length < 120) return;
        sendBatch();
        transcriptBatch = '';
        currentPendingSentence = '';
      }, questionInterval);
    } catch (e) {
      console.error('Transcript api error: ', e);
      $stage = 'idle';
    }
  }

  async function handleGeneratedQuestion(question: Question) {
    if (autoConfirm) {
      confirmQuestion(question);
      return;
    }
    console.log('question ');
    const modal: ModalSettings = {
      type: 'confirm',
      title: 'Confirm question to ask',
      body: `Question: <br>
    ${question.question}<br>
    Answers:<br>
    a) ${question.answers[0]} ${question.correct_response_index === 0 ? '(correct)' : ''}<br>
    b) ${question.answers[1]} ${question.correct_response_index === 1 ? '(correct)' : ''}<br>
    c) ${question.answers[2]} ${question.correct_response_index === 2 ? '(correct)' : ''}<br>
    d) ${question.answers[3]} ${question.correct_response_index === 3 ? '(correct)' : ''}
    `,
      response: (r: boolean) => {
        if (!r) return;
        confirmQuestion(question);
      },
    };

    modalStore.trigger(modal);
  }

  function onUserJoined(name: string) {
    $connectedUsers = [...$connectedUsers, name];
  }

  function confirmQuestion(question: Question) {
    socket?.emit('confirm_question', { id: question.id });
    $storedQuestions = {
      ...$storedQuestions,
      [question.id]: {
        correctAnswerIndex: question.correct_response_index,
        goodAnswers: [],
        wrongAnswers: [],
        timestamp: new Date(),
        questionId: question.id,
        question: question.question,
      },
    };
    const minute = 1000 * 60;
    setTimeout(() => findAFKUsers(question.id), minute);
  }

  function findAFKUsers(questionId: string) {
    const question = $storedQuestions[questionId];
    const usersSet = new Set();
    question.goodAnswers.forEach((a) => usersSet.add(a.userName));
    question.wrongAnswers.forEach((a) => usersSet.add(a.userName));
    const afkUsers = $connectedUsers
      .map((user) => (usersSet.has(user) ? null : user))
      .filter((i): i is string => i !== null);

    console.log('before success rate', question);
    const successRate =
      question.goodAnswers.length + question.wrongAnswers.length !== 0
        ? (question.goodAnswers.length /
            (question.goodAnswers.length + question.wrongAnswers.length)) *
          100
        : null;

    notifyMe('AFK users detected: ' + afkUsers.join(', '));
    notifyMe(
      successRate === null
        ? 'Nobody answered the question'
        : Math.round(successRate) + '% users answered the question correctly'
    );
  }

  function notifyMe(text: string) {
    if (!('Notification' in window)) {
      console.log('This browser does not support desktop notification');
    } else if (Notification.permission === 'granted') {
      const notification = new Notification(text);
    } else if (Notification.permission !== 'denied') {
      Notification.requestPermission().then((permission) => {
        if (permission === 'granted') {
          const notification = new Notification(text);
        }
      });
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
    if (questionIntervalTimer) {
      clearInterval(questionIntervalTimer);
      questionIntervalTimer = 0;
    }
    if (timerIntervalTimer) {
      clearInterval(timerIntervalTimer);
      timerIntervalTimer = 0;
    }
    $timer = 0;
    $stage = 'idle';
  }

  function handleNewResponse(response: ResponseEventData) {
    const correctAnswer = $storedQuestions[response.id].correctAnswerIndex;
    if (correctAnswer === response.response) {
      $storedQuestions[response.id].goodAnswers.push({
        userName: response.name,
      });
    } else {
      $storedQuestions[response.id].wrongAnswers.push({
        userName: response.name,
      });
    }
    $storedQuestions = structuredClone($storedQuestions);
  }
</script>

<div class="flex-1 pr-4">
  {#if $stage === 'idle'}
    <div class="stage-start mt-16 flex flex-col items-center">
      <button
        type="button"
        class="btn variant-filled-primary m-2 mb-8"
        on:click={startTranscript}
      >
        <div class="bg-red-500 w-3 h-3 rounded-full"></div>
        <span>Start recording</span>
      </button>
      <SlideToggle
        bind:checked={autoConfirm}
        size="sm"
        name="question confirmation">Questions auto confirmation</SlideToggle
      >
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
