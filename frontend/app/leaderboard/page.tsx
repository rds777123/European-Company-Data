import { api } from "@/lib/api";
import type { LeaderboardEntry } from "@/types";
import Link from "next/link";

export const revalidate = 30;

export default async function LeaderboardPage() {
  const res = await api.scores.leaderboard();
  const entries: LeaderboardEntry[] = res.data ?? [];

  return (
    <main className="max-w-md mx-auto mt-16 px-4">
      <h1 className="text-3xl font-bold text-sky-700 mb-6">Leaderboard</h1>
      {entries.length === 0 ? (
        <p className="text-gray-500">No scores yet. Be the first!</p>
      ) : (
        <ol className="space-y-2">
          {entries.map((e) => (
            <li key={e.rank} className="flex justify-between bg-white rounded-lg px-4 py-3 shadow-sm">
              <span className="font-semibold text-sky-600">#{e.rank} {e.username}</span>
              <span className="text-gray-700 font-mono">{e.best_score}</span>
            </li>
          ))}
        </ol>
      )}
      <Link href="/" className="mt-8 inline-block text-sky-500 hover:underline">
        Back to lobby
      </Link>
    </main>
  );
}
