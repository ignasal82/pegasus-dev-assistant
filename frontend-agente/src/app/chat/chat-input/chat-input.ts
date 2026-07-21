import { ChangeDetectionStrategy, Component, input, output, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-chat-input',
  imports: [FormsModule],
  templateUrl: './chat-input.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ChatInput {
  readonly disabled = input(false);
  readonly send = output<string>();

  protected readonly draft = signal('');

  protected submit(): void {
    const question = this.draft().trim();
    if (!question || this.disabled()) {
      return;
    }
    this.send.emit(question);
    this.draft.set('');
  }

  protected onKeydown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.submit();
    }
  }
}
