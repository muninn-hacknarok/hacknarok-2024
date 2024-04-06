<script lang="ts">
  import { ProgressBar } from '@skeletonlabs/skeleton';
  import {
    currentQuestion,
    respondentStage,
    respondentName,
    state,
  } from '../../stores/respondentStore';

  let progress = 0;
  let progressColor = 'green';

  const seconds = 10;
  let startTime = Date.now();
  let intervalId: number | null = setInterval(() => {
    // progress = Math.min(progress + 100 / seconds / 100, 100);
    progress = Math.min(
      ((Date.now() - startTime) / (seconds * 1000)) * 100,
      100
    );
    if (progress < 33) progressColor = 'green';
    else if (progress < 66) progressColor = 'yellow';
    else progressColor = 'red';

    if (intervalId !== null && progress === 100) {
      clearInterval(intervalId);
      intervalId = null;
      $respondentStage = 'waiting';
    }
  }, 10);

  function answerQuestion(answerIndex: number) {
    if (intervalId !== null) {
      clearInterval(intervalId);
      intervalId = null;
    }

    state.respondentSocket?.emit('response', {
      response: answerIndex,
      id: $currentQuestion?.id,
      name: $respondentName,
    });
    console.log('Answered with data: ', {
      response: answerIndex,
      id: $currentQuestion?.id,
      name: $respondentName,
    });

    $respondentStage = 'waiting';
    $currentQuestion = null;
  }
</script>

<div class="flex flex-col items-center bg-green mb-20">
  <ProgressBar
    rounded="0"
    value={progress}
    max={100}
    track={progressColor === 'green'
      ? 'bg-green-900'
      : progressColor === 'yellow'
        ? 'bg-yellow-900'
        : 'bg-red-900'}
    meter={progressColor === 'green'
      ? 'bg-green-500'
      : progressColor === 'yellow'
        ? 'bg-yellow-500'
        : 'bg-red-500'}
  />
  <h2 class="h4 max-w-4xl mt-4 px-4">
    {$currentQuestion?.question ?? 'Question not loaded'}
  </h2>
</div>

<div class="flex space-x-6 max-w-4xl mx-auto px-4">
  <div
    on:click={() => answerQuestion(0)}
    class="bg-red-600 rounded-2xl h-24 flex-1 flex items-center px-4 cursor-pointer hover:bg-red-800"
  >
    <span class="text-white">
      {$currentQuestion?.answers?.[0] ?? 'Answer not loaded'}
    </span>
  </div>
  <div
    on:click={() => answerQuestion(1)}
    class="bg-blue-600 rounded-2xl h-24 flex-1 flex items-center px-4 cursor-pointer hover:bg-blue-800"
  >
    <span class="text-white">
      {$currentQuestion?.answers?.[1] ?? 'Answer not loaded'}
    </span>
  </div>
</div>
<div class="flex space-x-6 max-w-4xl mx-auto px-4 mt-4">
  <div
    on:click={() => answerQuestion(2)}
    class="bg-yellow-500 rounded-2xl h-24 flex-1 flex items-center px-4 cursor-pointer hover:bg-yellow-700 text-white hover:text-gray-300"
  >
    <span>
      {$currentQuestion?.answers?.[2] ?? 'Answer not loaded'}
    </span>
  </div>
  <div
    on:click={() => answerQuestion(3)}
    class="bg-green-600 rounded-2xl h-24 flex-1 flex items-center px-4 cursor-pointer hover:bg-green-800"
  >
    <span class="text-white">
      {$currentQuestion?.answers?.[3] ?? 'Answer not loaded'}
    </span>
  </div>
</div>
