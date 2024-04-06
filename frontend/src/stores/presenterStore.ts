import { writable } from 'svelte/store';

type StageT = 'idle' | 'loading' | 'recording';

export const stage = writable<StageT>('idle');
