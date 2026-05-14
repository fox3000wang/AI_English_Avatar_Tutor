import type { ChatHistoryMessage } from "@/services/chatHistory";
import { getAudioUrl } from "@/services/voiceChat";

type ChatMessageListProps = {
  messages: ChatHistoryMessage[];
};

export function ChatMessageList({ messages }: ChatMessageListProps) {
  if (messages.length === 0) {
    return (
      <div className="rounded-lg border border-ink/10 bg-white/70 p-5 text-sm text-ink/60 shadow-sm">
        No conversation yet. Start recording when you are ready.
      </div>
    );
  }

  return (
    <div className="space-y-4" aria-live="polite">
      {messages.map((message) => {
        const isTeacher = message.role === "ai";

        return (
          <article
            key={message.id}
            className={
              isTeacher
                ? "rounded-lg border border-coral/20 bg-mint/70 p-5 shadow-sm"
                : "rounded-lg border border-ink/10 bg-white p-5 shadow-sm"
            }
          >
            <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-ink/50">
              {isTeacher ? "Teacher" : "You said"}
            </p>
            <p className="text-base leading-7 text-ink">{message.text}</p>
            {message.audio_url ? (
              <audio className="mt-4 w-full" controls src={getAudioUrl(message.audio_url)}>
                <track kind="captions" />
              </audio>
            ) : null}
          </article>
        );
      })}
    </div>
  );
}
