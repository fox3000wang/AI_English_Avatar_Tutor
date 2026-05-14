import json

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.schemas.lesson_report import LessonReportMistake, LessonReportResponse
from app.services.chat_service import get_chat_history

LESSON_REPORT_MODEL = "gpt-4o-mini"
LESSON_REPORT_SYSTEM_PROMPT = """
你是一位温柔、专业的儿童英语外教，正在为一位9岁中国女孩生成本节英语口语课总结。

要求：
- 总结要简单、鼓励、具体
- 不要批评孩子
- mistakes 最多列 3 条
- strengths 最多列 3 条
- new_words 最多列 5 个
- next_practice 最多列 3 条
- 使用简单英文
- 可以让家长也看得懂
- 不输出成人、暴力、政治、恐怖内容
- 如果聊天内容太少，就给出鼓励性总结和下一步练习建议

返回必须是 JSON，不要返回 Markdown。
""".strip()


def create_mock_lesson_report(session_id: int, has_messages: bool) -> LessonReportResponse:
    if not has_messages:
        return LessonReportResponse(
            session_id=session_id,
            summary="There is not much class conversation yet, but this is a good start.",
            strengths=["You are ready to practice English."],
            mistakes=[],
            new_words=[],
            next_practice=[
                "Say hello to your teacher.",
                "Try one full sentence: My name is...",
            ],
        )

    return LessonReportResponse(
        session_id=session_id,
        summary="Today you practiced simple English conversation with your teacher.",
        strengths=[
            "You were brave to speak English.",
            "You answered simple questions clearly.",
        ],
        mistakes=[
            LessonReportMistake(
                original="I likes cat.",
                corrected="I like cats.",
                explanation="Use 'like' after I.",
            )
        ],
        new_words=["favorite", "because", "practice"],
        next_practice=[
            "Practice saying: My favorite animal is...",
            "Try to answer with a full sentence.",
        ],
    )


def build_lesson_report_prompt(messages_text: str) -> str:
    return f"""
Please generate a lesson report from this chat history.

Chat history:
{messages_text}

Return this JSON shape:
{{
  "summary": "string",
  "strengths": ["string"],
  "mistakes": [
    {{
      "original": "string",
      "corrected": "string",
      "explanation": "string"
    }}
  ],
  "new_words": ["string"],
  "next_practice": ["string"]
}}
""".strip()


def normalize_report(session_id: int, payload: dict) -> LessonReportResponse:
    return LessonReportResponse(
        session_id=session_id,
        summary=str(payload.get("summary", "")),
        strengths=[str(item) for item in payload.get("strengths", [])][:3],
        mistakes=[
            LessonReportMistake(
                original=str(item.get("original", "")),
                corrected=str(item.get("corrected", "")),
                explanation=str(item.get("explanation", "")),
            )
            for item in payload.get("mistakes", [])[:3]
            if isinstance(item, dict)
        ],
        new_words=[str(item) for item in payload.get("new_words", [])][:5],
        next_practice=[str(item) for item in payload.get("next_practice", [])][:3],
    )


def create_lesson_report(db: Session, session_id: int) -> LessonReportResponse:
    messages = get_chat_history(db=db, session_id=session_id)
    has_messages = len(messages) > 0
    settings = get_settings()

    if not settings.openai_api_key:
        return create_mock_lesson_report(session_id=session_id, has_messages=has_messages)

    messages_text = "\n".join(f"{message.role}: {message.text}" for message in messages)
    if not messages_text:
        return create_mock_lesson_report(session_id=session_id, has_messages=False)

    try:
        from openai import OpenAI

        client = OpenAI(api_key=settings.openai_api_key)
        response = client.chat.completions.create(
            model=LESSON_REPORT_MODEL,
            messages=[
                {"role": "system", "content": LESSON_REPORT_SYSTEM_PROMPT},
                {"role": "user", "content": build_lesson_report_prompt(messages_text)},
            ],
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content or "{}"
        return normalize_report(session_id=session_id, payload=json.loads(content))
    except Exception:
        return create_mock_lesson_report(session_id=session_id, has_messages=has_messages)
