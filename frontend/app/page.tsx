import Link from "next/link";

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen gap-8">
      <h1 className="text-5xl font-bold text-sky-700">Flappy Bird</h1>
      <p className="text-lg text-gray-600">Tap to flap. Don&apos;t hit the pipes.</p>
      <div className="flex gap-4">
        <Link
          href="/game"
          className="px-8 py-3 bg-sky-500 text-white rounded-xl text-lg font-semibold hover:bg-sky-600 transition"
        >
          Play
        </Link>
        <Link
          href="/leaderboard"
          className="px-8 py-3 bg-white border border-sky-400 text-sky-600 rounded-xl text-lg font-semibold hover:bg-sky-50 transition"
        >
          Leaderboard
        </Link>
      </div>
    </main>
  );
}
