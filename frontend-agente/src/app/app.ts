import { Component, OnInit, inject } from '@angular/core';

import { ChatHeader } from './chat/chat-header/chat-header';
import { ChatInput } from './chat/chat-input/chat-input';
import { ChatMessages } from './chat/chat-messages/chat-messages';
import { ChatService } from './chat/chat.service';

@Component({
  selector: 'app-root',
  imports: [ChatHeader, ChatMessages, ChatInput],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App implements OnInit {
  protected readonly chat = inject(ChatService);

  ngOnInit(): void {
    void this.chat.refreshHealth();
  }

  protected onSend(question: string): void {
    void this.chat.send(question);
  }

  protected onNewConversation(): void {
    void this.chat.reset();
  }
}
