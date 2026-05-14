import type { LessonReportResponse } from "@/services/lessonReport";

type LessonReportCardProps = {
  report: LessonReportResponse | null;
};

function ReportList({ items }: { items: string[] }) {
  if (items.length === 0) {
    return <p className="text-sm text-ink/50">No items yet.</p>;
  }

  return (
    <ul className="list-disc space-y-2 pl-5 text-sm leading-6 text-ink/75">
      {items.map((item) => (
        <li key={item}>{item}</li>
      ))}
    </ul>
  );
}

export function LessonReportCard({ report }: LessonReportCardProps) {
  if (!report) {
    return (
      <div className="rounded-lg border border-ink/10 bg-white/75 p-5 text-sm leading-6 text-ink/60 shadow-sm">
        课后总结会显示在这里。完成一段对话后，点击生成总结。
      </div>
    );
  }

  return (
    <section className="space-y-5 rounded-lg border border-ink/10 bg-white/85 p-5 shadow-sm">
      <div>
        <p className="text-xs font-semibold uppercase tracking-wide text-coral">Lesson Report</p>
        <h2 className="mt-2 text-2xl font-black text-ink">课后学习总结</h2>
      </div>

      <p className="text-base leading-7 text-ink">{report.summary}</p>

      <div className="grid gap-5 sm:grid-cols-2">
        <div>
          <h3 className="mb-2 text-sm font-bold text-ink">Strengths</h3>
          <ReportList items={report.strengths} />
        </div>

        <div>
          <h3 className="mb-2 text-sm font-bold text-ink">New Words</h3>
          <ReportList items={report.new_words} />
        </div>
      </div>

      <div>
        <h3 className="mb-2 text-sm font-bold text-ink">Gentle Corrections</h3>
        {report.mistakes.length === 0 ? (
          <p className="text-sm text-ink/50">No correction needed yet.</p>
        ) : (
          <div className="space-y-3">
            {report.mistakes.map((mistake) => (
              <div
                key={`${mistake.original}-${mistake.corrected}`}
                className="rounded-lg border border-coral/15 bg-paper p-4 text-sm leading-6"
              >
                <p className="text-ink/60">Original: {mistake.original}</p>
                <p className="font-semibold text-ink">Try: {mistake.corrected}</p>
                <p className="text-ink/70">{mistake.explanation}</p>
              </div>
            ))}
          </div>
        )}
      </div>

      <div>
        <h3 className="mb-2 text-sm font-bold text-ink">Next Practice</h3>
        <ReportList items={report.next_practice} />
      </div>
    </section>
  );
}
