import { CheckCircle2, XCircle } from 'lucide-react';
import { VERDICT_LABELS } from '../../utils/formatters';

// Renders one test case's input/expected/actual output (plus stderr or
// compiler output, whichever applies) for both the "Run" sample results and
// a submission's failing hidden test case.
export default function TestCaseResult({ result, label }) {
  const { passed, verdict, input, expected_output, actual_output, stderr, compile_output } = result;

  const toneClass = passed
    ? 'border-success/30 bg-success-soft'
    : 'border-error/30 bg-error-soft';

  return (
    <div className={`rounded-lg border p-3 text-xs ${toneClass}`}>
      <div className="mb-2 flex items-center gap-2 font-medium">
        {passed ? (
          <CheckCircle2 size={14} className="shrink-0 text-success" />
        ) : (
          <XCircle size={14} className="shrink-0 text-error" />
        )}
        <span className={passed ? 'text-success' : 'text-error'}>
          {label ? `${label} — ` : ''}
          {VERDICT_LABELS[verdict] || verdict}
        </span>
      </div>
      <div className="grid gap-2 sm:grid-cols-2">
        <Field label="Input" value={input} />
        <Field label="Expected Output" value={expected_output} />
        {!passed && <Field label="Your Output" value={actual_output} />}
        {verdict === 'compilation_error' && (
          <Field label="Compiler Output" value={compile_output} span />
        )}
        {verdict === 'runtime_error' && <Field label="Error Output" value={stderr} span />}
      </div>
    </div>
  );
}

function Field({ label, value, span = false }) {
  if (value === null || value === undefined || value === '') return null;

  return (
    <div className={span ? 'sm:col-span-2' : ''}>
      <p className="mb-1 text-[10px] font-semibold uppercase tracking-wide text-ink-faint">{label}</p>
      <pre className="overflow-x-auto whitespace-pre-wrap rounded-md border border-border bg-surface-2 p-2 font-mono text-ink">
        {value}
      </pre>
    </div>
  );
}
