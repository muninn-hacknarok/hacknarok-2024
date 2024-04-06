<script lang="ts">
  import { onMount } from 'svelte';
  import { useLocation, useNavigate } from 'svelte-navigator';
  import { isAuthenticated, user } from '../../stores/auth';
  import { trpc } from '../../lib/trpc';
  import type { Role } from '../../../../backend/src/utils/AuthUtils';
  import { toastStore } from '@skeletonlabs/skeleton';

  const navigate = useNavigate();
  const location = useLocation();

  onMount(async () => {
    if ($isAuthenticated === null) {
      const { isAuthenticated: isAuth, user: usr } =
        await trpc.auth.checkSession.query();
      $isAuthenticated = isAuth;
      if (usr?.role && usr?.username) {
        $user = {
          username: usr.username,
          role: usr.role as Role,
        };
      }
    }
  });

  $: {
    if ($isAuthenticated === true) {
      navigate('/tournaments', { replace: true });
    }
  }
</script>

{#if $isAuthenticated === false}
  <slot />
{/if}
