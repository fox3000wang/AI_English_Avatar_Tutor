export type ChatHistoryMessage = {
  id: number;
  role: string;
  text: string;
  audio_url: string | null;
  correction: string | null;
  created_at: string;
};

export type ChatHistoryResponse = {
  session_id: number;
  messages: ChatHistoryMessage[];
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function fetchChatHistory(sessionId: number): Promise<ChatHistoryResponse> {
  const params = new URLSearchParams({ session_id: String(sessionId) });
  const response = await fetch(`${API_BASE_URL}/api/v1/chat-history?${params.toString()}`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Chat history request failed");
  }

  return response.json() as Promise<ChatHistoryResponse>;
}
