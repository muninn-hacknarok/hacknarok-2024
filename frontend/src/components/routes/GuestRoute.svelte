<script lang="ts">
  import { Route } from 'svelte-navigator';
  import GuestRouteGuard from './GuestRouteGuard.svelte';
  export let path = '';
</script>

<Route {path} let:params let:location let:navigate>
  <GuestRouteGuard>
    <slot {params} {location} {navigate} />
  </GuestRouteGuard>
</Route>
