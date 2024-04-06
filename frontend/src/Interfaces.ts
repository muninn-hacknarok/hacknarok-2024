export interface IQuestion {
    title: string
    answers: IAnswer[]
}

export interface IAnswer {
    username: string
    isCorrect: boolean
}

export interface IAPINewAnswerResponse {
    questionId: string,
    answerId: number,
    username: string
}

export interface IAPIQuestion {
    questionId: string
    answers: string[]
    correctAnswerId: number
}