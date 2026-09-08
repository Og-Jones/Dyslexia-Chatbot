import {
    ChangeDetectorRef,
    Component,
    ElementRef,
    OnDestroy,
    ViewChild,
    inject
} from '@angular/core';

import { FormsModule } from '@angular/forms';
import { ChatbotApiService } from '../../core/chatbot-api.service';
import { AskResponse } from '../../models/interfaces';
import { QuestionInputComponent } from './components/question-input/question-input.component';
import { AnswerCardComponent } from './components/answer-card/answer-card.component';

@Component({
    selector: 'app-chatbot',
    standalone: true,
    imports: [FormsModule, QuestionInputComponent, AnswerCardComponent],
    templateUrl: './chatbot.component.html',
    styleUrl: './chatbot.component.css'
})

export class ChatbotComponent implements OnDestroy {
    private readonly chatbotApi = inject(ChatbotApiService);

    private readonly changeDetector =
        inject(ChangeDetectorRef);

    @ViewChild('audioPlayer')
    private audioPlayer?: ElementRef<HTMLAudioElement>;

    response: AskResponse | null = null;
    errorMessage = '';

    isLoadingAnswer = false;
    isLoadingAudio = false;

    audioUrl: string | null = null;

    askQuestion(question: string): void {
        const trimmedQuestion = question.trim();

        if (!trimmedQuestion || this.isLoadingAnswer) {return;}

        this.resetAudio();

        this.response = null;
        this.errorMessage = '';
        this.isLoadingAnswer = true;

        this.chatbotApi
            .askQuestion(trimmedQuestion)
            .subscribe({
                next: (response) => {
                    console.log('API response:', response);

                    this.response = response;
                    this.isLoadingAnswer = false;

                    this.changeDetector.markForCheck();

                    this.prepareAudio(response.answer);
                },

                error: (error) => {
                    console.error('Question request failed:', error);

                    this.errorMessage =
                        'Something went wrong. Please try again.';

                    this.isLoadingAnswer = false;

                    this.changeDetector.markForCheck();
                }
            });
    }

    private prepareAudio(answerText: string): void {
        this.isLoadingAudio = true;
        this.changeDetector.markForCheck();

        this.chatbotApi
            .generateSpeech(answerText)
            .subscribe({
                next: (audioBlob) => {
                    if (audioBlob.size === 0) {
                        this.isLoadingAudio = false;

                        console.error(
                            'The speech endpoint returned an empty file.'
                        );

                        this.changeDetector.markForCheck();
                        return;
                    }

                    this.audioUrl =
                        URL.createObjectURL(audioBlob);

                    this.isLoadingAudio = false;
                    this.changeDetector.markForCheck();
                },

                error: (error) => {
                    console.error(
                        'Speech generation failed:',
                        error
                    );

                    this.errorMessage =
                        'The written answer is available, but its audio could not be generated.';

                    this.isLoadingAudio = false;
                    this.changeDetector.markForCheck();
                }
            });
    }


    listenToAnswer(): void {
        const player = this.audioPlayer?.nativeElement;

        if (!player || !this.audioUrl) {
            return;
        }

        player.load();

        void player.play().catch((error) => {
            console.error(
                'Audio playback failed:',
                error
            );

            this.errorMessage =
                'Your browser could not play the audio.';

            this.changeDetector.markForCheck();
        });
    }

    ngOnDestroy(): void {
        this.resetAudio();
    }

    private resetAudio(): void {
        const player = this.audioPlayer?.nativeElement;

        if (player) {
            player.pause();
            player.removeAttribute('src');
            player.load();
        }

        if (this.audioUrl) {
            URL.revokeObjectURL(this.audioUrl);
            this.audioUrl = null;
        }
    }
}