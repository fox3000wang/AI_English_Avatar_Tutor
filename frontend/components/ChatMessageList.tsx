import type { VoiceChatResponse } from "@/services/voiceChat";

type ChatMessageListProps = {
  result: VoiceChatResponse | null;
};

export function ChatMessageList({ result }: ChatMessageListProps) {
  if (!result) {
    return (
      <div className="rounded-lg border border-ink/10 bg-white/70 p-5 text-sm text-ink/60 shadow-sm">
        Your conversation will appear here after recording.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <article className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
        <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-ink/50">
          You said
        </p>
        <p className="text-base leading-7 text-ink">{result.user_text}</p>
      </article>

      <article className="rounded-lg border border-coral/20 bg-mint/70 p-5 shadow-sm">
        <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-ink/50">
          Teacher
        </p>
        <p className="text-base leading-7 text-ink">{result.ai_text}</p>
      </article>
    </div>
  );
}
