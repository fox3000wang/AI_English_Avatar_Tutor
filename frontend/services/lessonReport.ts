export interface LessonReportMistake {
  original: string;
  corrected: string;
  explanation: string;
}

export interface LessonReportResponse {
  session_id: number | string;
  summary: string;
  strengths: string[];
  mistakes: LessonReportMistake[];
  new_words: string[];
  next_practice: string[];
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function createLessonReport(sessionId: number): Promise<LessonReportResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/lesson-report`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ session_id: sessionId }),
  });

  if (!response.ok) {
    throw new Error("Lesson report request failed");
  }

  return response.json() as Promise<LessonReportResponse>;
}
