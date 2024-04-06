<script lang="ts">
  import { ProgressBar } from '@skeletonlabs/skeleton';

  let progress = 0;
  let progressColor = 'green';

  const seconds = 10;
  setInterval(() => {
    progress += 100 / seconds / 100;
    if (progress < 33) progressColor = 'green';
    else if (progress < 66) progressColor = 'yellow';
    else progressColor = 'red';
  }, 10);
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
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla tempor
    tristique libero, non auctor tellus aliquam eu. Maecenas accumsan, ipsum et
    ornare rhoncus, turpis felis interdum libero, sed mattis erat elit non
    mauris?
  </h2>
</div>

<div class="flex space-x-6 max-w-4xl mx-auto px-4">
  <div
    class="bg-red-600 rounded-2xl h-24 flex-1 flex items-center px-4 cursor-pointer hover:bg-red-800"
  >
    <span class="text-white">
      Lorem ipsum dolor sit amet, consectetur adipiscing elit.</span
    >
  </div>
  <div
    class="bg-blue-600 rounded-2xl h-24 flex-1 flex items-center px-4 cursor-pointer hover:bg-blue-800"
  >
    <span class="text-white">
      Lorem ipsum dolor sit amet, consectetur adipiscing elit.</span
    >
  </div>
</div>
<div class="flex space-x-6 max-w-4xl mx-auto px-4 mt-4">
  <div
    class="bg-yellow-500 rounded-2xl h-24 flex-1 flex items-center px-4 cursor-pointer hover:bg-yellow-700 text-white hover:text-gray-300"
  >
    <span> Lorem ipsum dolor sit amet, consectetur adipiscing elit.</span>
  </div>
  <div
    class="bg-green-600 rounded-2xl h-24 flex-1 flex items-center px-4 cursor-pointer hover:bg-green-800"
  >
    <span class="text-white">
      Lorem ipsum dolor sit amet, consectetur adipiscing elit.</span
    >
  </div>
</div>
