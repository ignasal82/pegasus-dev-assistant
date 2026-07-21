import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';

import { HealthResponse } from '../chat.models';

@Component({
  selector: 'app-chat-header',
  templateUrl: './chat-header.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ChatHeader {
  readonly health = input<HealthResponse | null>(null);
  readonly hasConversation = input(false);
  readonly newConversation = output<void>();
}
