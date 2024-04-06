import type { Socket } from 'socket.io-client';
import { writable } from 'svelte/store';
import type { DefaultEventsMap } from '@socket.io/component-emitter';

type StageT = 'joining' | 'waiting' | 'answering';

export const respondentStage = writable<StageT>('joining');

interface State {
  respondentSocket?: Socket<DefaultEventsMap, DefaultEventsMap>;
}
export const state: State = {
  respondentSocket: undefined,
};

export interface QuestionEventData {
  id: string;
  room: string;
  question: string;
  answers: string[];
}

export const currentQuestion = writable<QuestionEventData | null>(null);
export const respondentName = writable<string>('');
