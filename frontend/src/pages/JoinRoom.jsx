import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { LogIn } from 'lucide-react';
import { joinRoom } from '../api/rooms';
import { getApiErrorMessage } from '../api/axios';
import Card from '../components/common/Card';
import Input from '../components/common/Input';
import Button from '../components/common/Button';
import ErrorBanner from '../components/common/ErrorBanner';

export default function JoinRoom() {
  const navigate = useNavigate();

  const [roomCode, setRoomCode] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      const { data } = await joinRoom(roomCode.trim());
      navigate(`/rooms/${data.room_code}`);
    } catch (err) {
      setError(getApiErrorMessage(err, 'Could not join that room.'));
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="mx-auto max-w-sm">
      <div className="mb-6 flex items-center gap-3">
        <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary-soft text-primary">
          <LogIn size={20} />
        </span>
        <div>
          <h1 className="text-xl font-semibold text-ink">Join a Room</h1>
          <p className="text-sm text-ink-soft">Enter the room code your friend shared with you.</p>
        </div>
      </div>

      <Card>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <Input
            id="roomCode"
            label="Room Code"
            placeholder="e.g. 639c4026"
            value={roomCode}
            onChange={(event) => setRoomCode(event.target.value)}
            className="font-mono"
            required
          />
          <ErrorBanner message={error} />
          <Button type="submit" isLoading={isSubmitting} className="w-full">
            Join Room
          </Button>
        </form>
      </Card>
    </div>
  );
}
