"use client";

import { useEffect, useRef, useState } from "react";
import { ChatMessageList, type ChatMessageItem } from "@/components/ChatMessageList";
import { ErrorMessage } from "@/components/ErrorMessage";
import { LoadingState } from "@/components/LoadingState";
import { VoiceRecorder } from "@/components/VoiceRecorder";
import { fetchChatHistory, type ChatHistoryMessage } from "@/services/chatHistory";
import type { VoiceChatResponse } from "@/services/voiceChat";

const SESSION_ID = 1;

function mapRole(role: string | undefined): "user" | "assistant" {
  return role === "ai" || role === "assistant" ? "assistant" : "user";
}

function normalizeHistoryMessages(messages: ChatHistoryMessage[]): ChatMessageItem[] {
  const normalizedMessages: ChatMessageItem[] = [];

  messages.forEach((message, index) => {
    if (message.user_text || message.ai_text) {
      if (message.user_text) {
        normalizedMessages.push({
          id: `${message.id ?? index}-user`,
          role: "user",
          content: message.user_text,
        });
      }

      if (message.ai_text) {
        normalizedMessages.push({
          id: `${message.id ?? index}-assistant`,
          role: "assistant",
          content: message.ai_text,
          audioUrl: message.audio_url,
        });
      }

      return;
    }

    const content = message.content ?? message.text ?? "";
    if (content.length > 0) {
      normalizedMessages.push({
        id: message.id ?? `history-${index}`,
        role: mapRole(message.role),
        content,
        audioUrl: message.audio_url,
      });
    }
  });

  return normalizedMessages;
}

function createLocalMessage(role: "user" | "assistant", content: string, audioUrl?: string) {
  return {
    id: `${Date.now()}-${role}`,
    role,
    content,
    audioUrl,
  };
}

export default function StudentPage() {
  const [messages, setMessages] = useState<ChatMessageItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    let isMounted = true;

    async function loadHistory() {
      try {
        const history = await fetchChatHistory(SESSION_ID);
        if (isMounted) {
          setMessages(normalizeHistoryMessages(history.messages));
        }
      } catch {
        if (isMounted) {
          setError("聊天历史加载失败，请稍后重试。");
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    void loadHistory();

    return () => {
      isMounted = false;
    };
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages.length]);

  function handleVoiceResult(result: VoiceChatResponse) {
    setMessages((currentMessages) => [
      ...currentMessages,
      createLocalMessage("user", result.user_text),
      createLocalMessage("assistant", result.ai_text, result.audio_url),
    ]);
  }

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-3xl flex-col px-5 py-10">
      <section className="space-y-8">
        <div className="space-y-3">
          <p className="text-sm font-semibold uppercase tracking-[0.18em] text-coral">
            Student Practice
          </p>
          <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
            <h1 className="text-4xl font-black tracking-normal text-ink sm:text-5xl">
              AI English Tutor
            </h1>
            <p className="rounded-lg border border-ink/10 bg-white/70 px-3 py-2 text-sm font-semibold text-ink/60 shadow-sm">
              当前 Session：{SESSION_ID}
            </p>
          </div>
        </div>

        <div className="grid gap-5">
          <VoiceRecorder sessionId={SESSION_ID} onResult={handleVoiceResult} />
          {isLoading ? <LoadingState message="正在加载聊天历史..." /> : null}
          {error ? <ErrorMessage message={error} /> : null}
          {!isLoading ? (
            <div className="max-h-[62vh] overflow-y-auto pr-1">
              <ChatMessageList messages={messages} />
              <div ref={bottomRef} />
            </div>
          ) : null}
        </div>
      </section>
    </main>
  );
}
