import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Dices } from 'lucide-react';
import { createRoom } from '../api/rooms';
import { getApiErrorMessage } from '../api/axios';
import { DIFFICULTY_LABELS, TOPIC_LABELS } from '../utils/formatters';
import Card from '../components/common/Card';
import Select from '../components/common/Select';
import Input from '../components/common/Input';
import Button from '../components/common/Button';
import ErrorBanner from '../components/common/ErrorBanner';

export default function CreateRoom() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    topic: 'array',
    difficulty: 'easy',
    number_of_questions: 3,
    time_limit_minutes: 60,
  });
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  function updateField(field) {
    return (event) => setForm((prev) => ({ ...prev, [field]: event.target.value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      const { data } = await createRoom({
        topic: form.topic,
        difficulty: form.difficulty,
        number_of_questions: Number(form.number_of_questions),
        time_limit_minutes: Number(form.time_limit_minutes),
      });
      navigate(`/rooms/${data.room_code}`);
    } catch (err) {
      setError(getApiErrorMessage(err, 'Could not create the room.'));
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="mx-auto max-w-lg">
      <div className="mb-6 flex items-center gap-3">
        <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary-soft text-primary">
          <Dices size={20} />
        </span>
        <div>
          <h1 className="text-xl font-semibold text-ink">Create a Room</h1>
          <p className="text-sm text-ink-soft">
            Problems are chosen automatically for your topic and difficulty.
          </p>
        </div>
      </div>

      <Card>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <Select id="topic" label="Topic" value={form.topic} onChange={updateField('topic')}>
            {Object.entries(TOPIC_LABELS).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </Select>

          <Select
            id="difficulty"
            label="Difficulty"
            value={form.difficulty}
            onChange={updateField('difficulty')}
          >
            {Object.entries(DIFFICULTY_LABELS).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </Select>

          <Input
            id="number_of_questions"
            label="Number of Questions"
            type="number"
            min={1}
            value={form.number_of_questions}
            onChange={updateField('number_of_questions')}
            required
          />

          <Input
            id="time_limit_minutes"
            label="Time Limit (minutes)"
            type="number"
            min={1}
            value={form.time_limit_minutes}
            onChange={updateField('time_limit_minutes')}
            required
          />

          <ErrorBanner message={error} />

          <Button type="submit" isLoading={isSubmitting} className="w-full">
            Create Room
          </Button>
        </form>
      </Card>
    </div>
  );
}
