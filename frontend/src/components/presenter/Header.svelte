<script lang="ts">
  import { isDarkTheme } from '../../stores/globalStore';
</script>

<div class="flex justify-center my-6">
  <img
    class="w-96"
    src={$isDarkTheme
      ? 'assets/logo_dark_theme.png'
      : 'assets/logo_light_theme.png'}
    alt=""
  />
</div>
