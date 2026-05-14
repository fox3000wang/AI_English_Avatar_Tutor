type ErrorMessageProps = {
  message: string;
};

export function ErrorMessage({ message }: ErrorMessageProps) {
  return (
    <div className="rounded-lg border border-coral/25 bg-white/80 p-5 text-sm font-semibold text-coral shadow-sm">
      {message}
    </div>
  );
}
