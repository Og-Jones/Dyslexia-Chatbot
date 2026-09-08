import {
    Component,
    ElementRef,
    EventEmitter,
    Input,
    Output,
    ViewChild
} from '@angular/core';

import { FormsModule } from '@angular/forms';

@Component({
    selector: 'app-question-input',
    standalone: true,
    imports: [FormsModule],
    templateUrl: './question-input.component.html',
    styleUrl: './question-input.component.css'
})

export class QuestionInputComponent {
  @Input()
  disabled = false;


  @Output()
  readonly questionSubmitted = new EventEmitter<string>();


  @ViewChild('questionTextarea')
  private questionTextarea?: ElementRef<HTMLTextAreaElement>;

  question = '';

  // emits the question to parent component and resets input field
  submitQuestion(): void {
        const trimmedQuestion = this.question.trim();

        if (!trimmedQuestion || this.disabled) {return;}

        this.questionSubmitted.emit(trimmedQuestion);

        this.question = '';
        this.resetTextareaHeight();
    }

  // when enter is pressed question is submitted, unless shift key is held
  handleEnter(event: Event): void {
      const keyboardEvent = event as KeyboardEvent;

      if (keyboardEvent.shiftKey) {return;}

      keyboardEvent.preventDefault();
      this.submitQuestion();
  }

  // resizes the text area via scroll
  resizeTextarea(event: Event): void {
        const textarea = event.target as HTMLTextAreaElement;

        textarea.style.height = 'auto';
        textarea.style.height = `${Math.min(textarea.scrollHeight, 180)}px`;
    }

  // resets the text area after question submission
  private resetTextareaHeight(): void {
        setTimeout(() => {
            const textarea = this.questionTextarea?.nativeElement;

            if (textarea) {textarea.style.height = 'auto';}
        });
    }
}