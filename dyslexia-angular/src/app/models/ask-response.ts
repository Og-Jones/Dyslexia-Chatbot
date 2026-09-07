import { Source } from './source';

export interface AskResponse {
    answer: string;
    sources: Source[];
}