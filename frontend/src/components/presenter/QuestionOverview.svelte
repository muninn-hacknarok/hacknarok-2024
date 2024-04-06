<script lang="ts">
import { ProgressBar } from '@skeletonlabs/skeleton';
export let questions = [
    {
        "title": "What was the previous fragment about?",
        correctAnswerCount: 12,
        totalAnswers: 20
    },
    {
        "title": "Are sea lions cute?",
        correctAnswerCount: 18,
        totalAnswers: 19
    },
    {
        "title": "A lengthy question that noone has the time to read, moreso answer, even with the use of latest technology",
        correctAnswerCount: 1,
        totalAnswers: 12
    }
]

</script>
<div class="flex flex-col flex-1 justify-center mx-16">
    {#each questions as {title, correctAnswerCount, totalAnswers}}
        <div class="flex flex-row my-2 items-center">
            <span class="flex flex-1">{title}</span>
            <ProgressBar class="flex flex-1 ml-4 align-middle" value={correctAnswerCount} max={totalAnswers} track="bg-red-900" meter="bg-green-900" />

        </div>
    {/each}
</div>