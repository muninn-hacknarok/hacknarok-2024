<script lang="ts">
  // Your selected Skeleton theme:
  import '@skeletonlabs/skeleton/themes/theme-gold-nouveau.css';

  // This contains the bulk of Skeletons required styles:
  import '@skeletonlabs/skeleton/styles/skeleton.css';

  // Finally, your application's global stylesheet (sometimes labeled 'app.css')
  import './app.postcss';

  import { Router, Link, Route, useNavigate } from 'svelte-navigator';
  import { AppShell } from '@skeletonlabs/skeleton';

  import Home from './components/pages/Home.svelte';
  import { Modal, modalStore } from '@skeletonlabs/skeleton';
  import type { ModalSettings, ModalComponent } from '@skeletonlabs/skeleton';
  import Responder from './components/pages/Responder.svelte';
</script>

<Modal />
<Router>
  <AppShell>
    <svelte:fragment slot="header">
      <!-- <Header /> -->
    </svelte:fragment>

    <svelte:fragment slot="sidebarLeft">
      <!-- <SideNav /> -->
    </svelte:fragment>

    <Route path="/" component={Home} />

    <Route path="/:code" let:params>
      <Responder code={params.code} />
    </Route>
    <!-- <PrivateRoute path="/tournaments/new">
      <NewTournament />
    </PrivateRoute>

    <PrivateRoute path="/tournaments/:id/edit">
      <EditTournament />
    </PrivateRoute>

    <PrivateRoute path="/tournaments/:id">
      <Tournament />
    </PrivateRoute>

    <PrivateRoute path="/tournaments">
      <NoTournaments />
    </PrivateRoute>

    <PrivateRoute path="/policies/new">
      <PolicyForm mode="new" />
    </PrivateRoute>

    <PrivateRoute path="/policies/:id/edit">
      <PolicyForm mode="edit" />
    </PrivateRoute>

    <PrivateRoute path="/policies/:id">
      <Policy />
    </PrivateRoute>

    <PrivateRoute path="/policies">
      <NoPolicies />
    </PrivateRoute>

    <PrivateRoute path="/assets">
      <Assets />
    </PrivateRoute>

    <PrivateRoute path="/test">
      <PrivateTest />
    </PrivateRoute>

    <GuestRoute path="/sign-in">
      <SignIn />
    </GuestRoute>
    <GuestRoute path="/sign-up">
      <SignUp />
    </GuestRoute> -->

    <!-- <Route path="/*" component={NotFound} /> -->
  </AppShell>
</Router>
