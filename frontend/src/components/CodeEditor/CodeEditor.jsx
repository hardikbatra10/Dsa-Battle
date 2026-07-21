import Editor from '@monaco-editor/react';
import LoadingSpinner from '../LoadingSpinner/LoadingSpinner';

const MONACO_LANGUAGE = {
  cpp: 'cpp',
  java: 'java',
  python: 'python',
};

export default function CodeEditor({ language, value, onChange, readOnly = false, height = '100%' }) {
  return (
    <Editor
      height={height}
      language={MONACO_LANGUAGE[language] || 'plaintext'}
      value={value}
      onChange={(nextValue) => onChange?.(nextValue ?? '')}
      theme="vs-dark"
      loading={
        <div className="flex h-full items-center justify-center">
          <LoadingSpinner size={22} />
        </div>
      }
      options={{
        readOnly,
        minimap: { enabled: false },
        fontSize: 14,
        fontFamily: "ui-monospace, Consolas, monospace",
        scrollBeyondLastLine: false,
        automaticLayout: true,
        padding: { top: 12 },
      }}
    />
  );
}
