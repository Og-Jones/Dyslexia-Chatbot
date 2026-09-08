import {
    ChangeDetectionStrategy,
    Component,
    ElementRef,
    Input,
    ViewChild
} from '@angular/core';

import { AskResponse } from '../../../../models/interfaces';

@Component({
    selector: 'app-answer-card',
    standalone: true,
    imports: [],
    templateUrl: './answer-card.component.html',
    styleUrl: './answer-card.component.css',
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class AnswerCardComponent {
    @Input({ required: true })
    response!: AskResponse;

    @Input()
    audioUrl: string | null = null;

    @Input()
    isLoadingAudio = false;

    @ViewChild('audioPlayer')
    private audioPlayer?:
        ElementRef<HTMLAudioElement>;

    audioErrorMessage = '';

    playAudio(): void {
        const player = this.audioPlayer?.nativeElement;

        if (!player || !this.audioUrl) {return;}

        this.audioErrorMessage = '';

        player.load();

        void player.play().catch((error) => {
            console.error('Audio playback failed:', error);

            this.audioErrorMessage = 'Your browser could not play the audio.';
        });
    }
}