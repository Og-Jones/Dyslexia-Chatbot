export interface Source {
    source: string;
    title: string;
    sections: string[];
    url: string;
}

export interface AskResponse {
    answer: string;
    sources: Source[];
}