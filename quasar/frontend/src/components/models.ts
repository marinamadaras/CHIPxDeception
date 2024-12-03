export interface Todo {
  id: number;
  content: string;
}

export interface Meta {
  totalCount: number;
}

export interface ChatMessage {
  message: string;
  user: User | undefined;
}

export interface User {
  name: string;
  human: boolean;
}
