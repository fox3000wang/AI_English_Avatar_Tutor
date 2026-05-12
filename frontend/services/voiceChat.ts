export type VoiceChatResponse = {
  user_text: string;
  ai_text: string;
  audio_url: string;
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export function getAudioUrl(audioUrl: string): string {
  if (audioUrl.startsWith("http")) {
    return audioUrl;
  }

  return `${API_BASE_URL}${audioUrl}`;
}

export async function sendVoiceChat(
  file: Blob,
  sessionId: number,
): Promise<VoiceChatResponse> {
  const formData = new FormData();
  formData.append("session_id", String(sessionId));
  formData.append("file", file, "recording.wav");

  const response = await fetch(`${API_BASE_URL}/api/v1/voice-chat`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Voice chat request failed");
  }

  return response.json() as Promise<VoiceChatResponse>;
}
