import { writable } from 'svelte/store';

type StageT = 'idle' | 'loading' | 'recording';

export const stage = writable<StageT>('idle');

export interface StoredQuestionResponse {
  userName: string;
}

export interface StoredQuestion {
  questionId: string;
  question: string;
  correctAnswerIndex: number;
  goodAnswers: StoredQuestionResponse[];
  wrongAnswers: StoredQuestionResponse[];
  timestamp: Date;
}

export const storedQuestions = writable<Record<string, StoredQuestion>>({});

export const connectedUsers = writable<string[]>([]);

export const timer = writable<number>(0);
