<script lang="ts">
  import { modalStore, type ModalSettings } from '@skeletonlabs/skeleton';

  const modal: ModalSettings = {
    type: 'alert',
    title: 'Confirm question to ask',
    body: `Question: <br>
    Lorem ipsum fdfsd fsdfs llll fsdfsd fsdfs?<br>
    Answers:<br>
    a) lorem ipsum (correct)<br>
    b) lorem ipsum (correct)<br>
    c) lorem ipsum (correct)
    `,
  };
</script>

<button
  class="button"
  on:click={() => {
    modalStore.trigger(modal);
  }}>Trigger modal</button
>
