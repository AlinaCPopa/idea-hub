import { Idea } from '../api/generated/types';

type Props = { idea: Idea };
export function IdeaCard({ idea }: Props) {
  return (
    <div className="border rounded p-4 shadow-sm bg-white flex flex-col gap-2">
      <h3 className="font-semibold text-lg">{idea.title}</h3>
      {idea.description && <p className="text-sm text-gray-600">{idea.description}</p>}
      <div className="text-xs text-gray-500 flex gap-4">
        <span>Likes: {idea.likes}</span>
        <span>ID: {idea.id}</span>
      </div>
    </div>
  );
}
