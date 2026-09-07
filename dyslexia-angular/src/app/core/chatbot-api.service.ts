import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { AskResponse } from '../models/ask-response';

@Injectable({
    providedIn: 'root'
})
export class ChatbotApiService {
    private readonly http = inject(HttpClient);

    private readonly apiUrl = 'https://dyslexia-chatbot.onrender.com';

    askQuestion(question: string): Observable<AskResponse> {
        return this.http.post<AskResponse>(
            `${this.apiUrl}/ask`,
            { question }
        );
    }

    generateSpeech(text: string): Observable<Blob> {
        return this.http.post(
            `${this.apiUrl}/speech`,
            { text },
            {
                responseType: 'blob'
            }
        );
    }
}