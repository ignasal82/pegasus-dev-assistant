import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable, computed, inject, signal } from '@angular/core';
import { firstValueFrom } from 'rxjs';

import {
  ChatMessage,
  ChatRequest,
  ChatResponse,
  HealthResponse,
} from './chat.models';

const API_BASE = '/api';

@Injectable({ providedIn: 'root' })
export class ChatService {
  private readonly http = inject(HttpClient);

  private readonly sessionId = signal<string | null>(null);

  readonly messages = signal<ChatMessage[]>([]);
  readonly loading = signal(false);
  readonly health = signal<HealthResponse | null>(null);

  readonly hasConversation = computed(() => this.messages().length > 0);

  async refreshHealth(): Promise<void> {
    try {
      const health = await firstValueFrom(
        this.http.get<HealthResponse>(`${API_BASE}/health`),
      );
      this.health.set(health);
    } catch {
      this.health.set(null);
    }
  }

  async send(question: string): Promise<void> {
    const trimmed = question.trim();
    if (!trimmed || this.loading()) {
      return;
    }

    this.append({ role: 'user', text: trimmed, sources: [], timestamp: new Date() });
    this.loading.set(true);

    const payload: ChatRequest = { question: trimmed };
    const sessionId = this.sessionId();
    if (sessionId) {
      payload.session_id = sessionId;
    }

    try {
      const response = await firstValueFrom(
        this.http.post<ChatResponse>(`${API_BASE}/chat`, payload),
      );
      this.sessionId.set(response.session_id);
      this.append({
        role: 'assistant',
        text: this.stripCitations(response.answer),
        sources: response.sources,
        timestamp: new Date(),
      });
    } catch (error) {
      this.append({
        role: 'error',
        text: this.describeError(error),
        sources: [],
        timestamp: new Date(),
      });
    } finally {
      this.loading.set(false);
    }
  }

  async reset(): Promise<void> {
    const sessionId = this.sessionId();
    this.messages.set([]);
    this.sessionId.set(null);
    if (sessionId) {
      try {
        await firstValueFrom(this.http.delete(`${API_BASE}/sessions/${sessionId}`));
      } catch {
        // La sesión remota expira sola al reiniciar la API; no bloquea al usuario.
      }
    }
  }

  private append(message: ChatMessage): void {
    this.messages.update((messages) => [...messages, message]);
  }

  /**
   * Quita del texto las citas de fragmentos/fuentes que agrega el modelo
   * (por ejemplo "Fuente: Fragmento 2 (doc/conocimiento/faq.md)").
   * El panel de fuentes de la interfaz ya muestra esa información.
   */
  private stripCitations(answer: string): string {
    return answer
      // Paréntesis que citan fuentes o fragmentos: "(Fuente: ...)", "(doc/conocimiento/....md)"
      .replace(/\s*\((?:seg[uú]n\s+)?fuentes?:[^)]*\)/gi, '')
      .replace(/\s*\([^)]*fragmento[^)]*\)/gi, '')
      .replace(/\s*\([^)]*doc\/conocimiento\/[^)]*\)/gi, '')
      // Líneas u oraciones finales del tipo "Fuente: Fragmento 1 y Fragmento 2 ..."
      .replace(/^\s*fuentes?:.*$/gim, '')
      .replace(/fuentes?:\s*[^\n]*fragmento[^\n]*/gi, '')
      // Espacios sobrantes antes de puntuación y líneas vacías repetidas
      .replace(/[ \t]+([.,;])/g, '$1')
      .replace(/\n{3,}/g, '\n\n')
      .trim();
  }

  private describeError(error: unknown): string {
    if (error instanceof HttpErrorResponse) {
      if (error.status === 0) {
        return 'No se pudo conectar con la API. Verificá que esté corriendo en el puerto 8000.';
      }
      const detail = (error.error as { detail?: string } | null)?.detail;
      if (detail) {
        return detail;
      }
      return `La API respondió con un error (HTTP ${error.status}).`;
    }
    return 'Ocurrió un error inesperado al consultar al agente.';
  }
}
