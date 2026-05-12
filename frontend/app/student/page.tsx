"use client";

import { useState } from "react";
import { ChatMessageList } from "@/components/ChatMessageList";
import { VoiceRecorder } from "@/components/VoiceRecorder";
import type { VoiceChatResponse } from "@/services/voiceChat";

export default function StudentPage() {
  const [result, setResult] = useState<VoiceChatResponse | null>(null);

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-3xl flex-col justify-center px-5 py-10">
      <section className="space-y-8">
        <div className="space-y-3">
          <p className="text-sm font-semibold uppercase tracking-[0.18em] text-coral">
            Student Practice
          </p>
          <h1 className="text-4xl font-black tracking-normal text-ink sm:text-5xl">
            AI English Tutor
          </h1>
        </div>

        <div className="grid gap-5">
          <VoiceRecorder onResult={setResult} />
          <ChatMessageList result={result} />
        </div>
      </section>
    </main>
  );
}
