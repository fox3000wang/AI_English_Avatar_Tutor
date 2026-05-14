"use client";

import { useEffect, useState } from "react";
import { ChatMessageList } from "@/components/ChatMessageList";
import { ErrorMessage } from "@/components/ErrorMessage";
import { LoadingState } from "@/components/LoadingState";
import { VoiceRecorder } from "@/components/VoiceRecorder";
import { fetchChatHistory, type ChatHistoryMessage } from "@/services/chatHistory";
import type { VoiceChatResponse } from "@/services/voiceChat";

const SESSION_ID = 1;

function createLocalMessage(
  role: "child" | "ai",
  text: string,
  audioUrl: string | null = null,
): ChatHistoryMessage {
  return {
    id: Date.now() + (role === "ai" ? 1 : 0),
    role,
    text,
    audio_url: audioUrl,
    correction: null,
    created_at: new Date().toISOString(),
  };
}

export default function StudentPage() {
  const [messages, setMessages] = useState<ChatHistoryMessage[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    async function loadHistory() {
      try {
        const history = await fetchChatHistory(SESSION_ID);
        if (isMounted) {
          setMessages(history.messages);
        }
      } catch {
        if (isMounted) {
          setError("Unable to load chat history.");
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

  function handleVoiceResult(result: VoiceChatResponse) {
    setMessages((currentMessages) => [
      ...currentMessages,
      createLocalMessage("child", result.user_text),
      createLocalMessage("ai", result.ai_text, result.audio_url),
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
              Session #{SESSION_ID}
            </p>
          </div>
        </div>

        <div className="grid gap-5">
          <VoiceRecorder sessionId={SESSION_ID} onResult={handleVoiceResult} />
          {isLoading ? <LoadingState message="Loading chat history..." /> : null}
          {error ? <ErrorMessage message={error} /> : null}
          {!isLoading ? <ChatMessageList messages={messages} /> : null}
        </div>
      </section>
    </main>
  );
}
