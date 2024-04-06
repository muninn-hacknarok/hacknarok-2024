<script lang="ts">
  import { ProgressBar } from '@skeletonlabs/skeleton';
  import { stage, storedQuestions } from '../../stores/presenterStore';
  $: questions = Object.values($storedQuestions).sort(
    (a, b) => a.timestamp.getTime() - b.timestamp.getTime()
  );
  //   export let questions = [
  //     {
  //       title: 'What was the previous fragment about?',
  //       correctAnswerCount: 12,
  //       totalAnswers: 20,
  //     },
  //     {
  //       title: 'Are sea lions cute?',
  //       correctAnswerCount: 18,
  //       totalAnswers: 19,
  //     },
  //     {
  //       title:
  //         'A lengthy question that noone has the time to read, moreso answer, even with the use of latest technology',
  //       correctAnswerCount: 1,
  //       totalAnswers: 12,
  //     },
  //   ];
</script>

<div class="mt-14 px-8">
  {#if $stage === 'recording'}
    <h4 class="h4 mb-4">Questions:</h4>
  {/if}

  {#if questions.length > 0}
    <div class="flex flex-col flex-1 justify-center mx-16 mb-6">
      {#each questions as { question, wrongAnswers, goodAnswers }}
        <div class="flex my-2 items-center">
          <span class="flex flex-1 mr-2">{question}</span>
          <div class="flex flex-col items-end flex-1 ml-4">
            <span class="text-sm mb-1 mr-1"
              >{goodAnswers.length} / {goodAnswers.length +
                wrongAnswers.length}</span
            >
            <ProgressBar
              class="self-stretch"
              value={goodAnswers.length}
              max={goodAnswers.length + wrongAnswers.length}
              track="bg-red-500"
              meter="bg-green-500"
            />
          </div>
        </div>
      {/each}
    </div>
  {:else if $stage === 'recording'}
    <p class="text-center mt-8">There is no questions yet</p>
  {/if}
</div>
