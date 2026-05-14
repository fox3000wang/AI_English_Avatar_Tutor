import { getAudioUrl } from "@/services/voiceChat";

export type ChatMessageItem = {
  id: number | string;
  role: "user" | "assistant";
  content: string;
  audioUrl?: string | null;
};

type ChatMessageListProps = {
  messages: ChatMessageItem[];
};

export function ChatMessageList({ messages }: ChatMessageListProps) {
  if (messages.length === 0) {
    return (
      <div className="rounded-lg border border-ink/10 bg-white/75 p-6 text-base leading-7 text-ink/60 shadow-sm">
        还没有上课记录，点击麦克风开始第一句英语对话吧。
      </div>
    );
  }

  return (
    <div className="space-y-5" aria-live="polite">
      {messages.map((message) => {
        const isAssistant = message.role === "assistant";

        return (
          <article
            key={message.id}
            className={`flex ${isAssistant ? "justify-start" : "justify-end"}`}
          >
            <div
              className={
                isAssistant
                  ? "max-w-[86%] rounded-lg border border-coral/20 bg-mint/75 p-5 shadow-sm"
                  : "max-w-[86%] rounded-lg border border-ink/10 bg-white p-5 shadow-sm"
              }
            >
              <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-ink/50">
                {isAssistant ? "Teacher" : "You"}
              </p>
              <p className="whitespace-pre-wrap text-lg leading-8 text-ink">{message.content}</p>
              {message.audioUrl ? (
                <audio className="mt-4 w-full" controls src={getAudioUrl(message.audioUrl)}>
                  <track kind="captions" />
                </audio>
              ) : null}
            </div>
          </article>
        );
      })}
    </div>
  );
}
