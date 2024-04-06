<script lang="ts">
  import { onMount } from 'svelte';
  import { useLocation, useNavigate } from 'svelte-navigator';
  import { isAuthenticated, user } from '../../stores/auth';
  import { trpc } from '../../lib/trpc';
  import { toastStore } from '@skeletonlabs/skeleton';
  import type { RoleT } from '../../lib/prismaEnums';

  const navigate = useNavigate();
  const location = useLocation();

  onMount(async () => {
    console.log($isAuthenticated, $user);
    if ($isAuthenticated === null) {
      const { isAuthenticated: isAuth, user: usr } =
        await trpc.auth.checkSession.query();
      $isAuthenticated = isAuth;
      if (usr?.role && usr?.username) {
        $user = {
          username: usr.username,
          role: usr.role as RoleT,
        };
      }
    }
  });

  $: {
    if ($isAuthenticated === false) {
      toastStore.trigger({
        message: 'Page forbidden, redirected to sign in page.',
        background: 'variant-filled-warning',
      });
      navigate('/sign-in', {
        state: { from: $location.pathname },
        replace: true,
      });
    }
  }
</script>

{#if $isAuthenticated}
  <slot />
{/if}
