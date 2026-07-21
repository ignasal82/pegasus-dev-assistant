import {
  ChangeDetectionStrategy,
  Component,
  ElementRef,
  effect,
  input,
  viewChild,
} from '@angular/core';
import { DatePipe } from '@angular/common';

import { ChatMessage } from '../chat.models';

@Component({
  selector: 'app-chat-messages',
  imports: [DatePipe],
  templateUrl: './chat-messages.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ChatMessages {
  readonly messages = input.required<ChatMessage[]>();
  readonly loading = input(false);

  private readonly scrollArea = viewChild.required<ElementRef<HTMLElement>>('scrollArea');

  constructor() {
    // Baja al último mensaje cada vez que cambia la conversación.
    effect(() => {
      this.messages();
      this.loading();
      queueMicrotask(() => {
        const el = this.scrollArea().nativeElement;
        el.scrollTop = el.scrollHeight;
      });
    });
  }
}
