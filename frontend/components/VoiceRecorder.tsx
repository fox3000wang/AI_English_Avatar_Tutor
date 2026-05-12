"use client";

import { useRef, useState } from "react";
import { getAudioUrl, sendVoiceChat, type VoiceChatResponse } from "@/services/voiceChat";

type VoiceRecorderProps = {
  onResult: (result: VoiceChatResponse) => void;
};

export function VoiceRecorder({ onResult }: VoiceRecorderProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  async function startRecording() {
    setError(null);
    setAudioUrl(null);

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      chunksRef.current = [];

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      recorder.onstop = async () => {
        stream.getTracks().forEach((track) => track.stop());
        const audioBlob = new Blob(chunksRef.current, { type: recorder.mimeType });

        setIsUploading(true);
        try {
          const result = await sendVoiceChat(audioBlob, 1);
          onResult(result);
          setAudioUrl(getAudioUrl(result.audio_url));
        } catch {
          setError("Unable to send the recording. Please try again.");
        } finally {
          setIsUploading(false);
        }
      };

      mediaRecorderRef.current = recorder;
      recorder.start();
      setIsRecording(true);
    } catch {
      setError("Microphone permission is required.");
    }
  }

  function stopRecording() {
    mediaRecorderRef.current?.stop();
    mediaRecorderRef.current = null;
    setIsRecording(false);
  }

  function handleClick() {
    if (isRecording) {
      stopRecording();
      return;
    }

    void startRecording();
  }

  return (
    <div className="space-y-4">
      <button
        type="button"
        onClick={handleClick}
        disabled={isUploading}
        className="w-full rounded-lg bg-ink px-5 py-4 text-base font-semibold text-paper shadow-lg shadow-ink/10 transition hover:bg-ink/90 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {isUploading ? "Uploading..." : isRecording ? "Stop Recording" : "Start Recording"}
      </button>

      {error ? <p className="text-sm font-medium text-coral">{error}</p> : null}

      {audioUrl ? (
        <audio className="w-full" controls src={audioUrl}>
          <track kind="captions" />
        </audio>
      ) : null}
    </div>
  );
}
