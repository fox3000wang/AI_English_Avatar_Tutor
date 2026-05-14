type LoadingStateProps = {
  message: string;
};

export function LoadingState({ message }: LoadingStateProps) {
  return (
    <div className="rounded-lg border border-ink/10 bg-white/70 p-5 text-sm font-medium text-ink/60 shadow-sm">
      {message}
    </div>
  );
}
