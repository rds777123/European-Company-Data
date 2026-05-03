import Link from "next/link";

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen gap-8">
      <h1 className="text-5xl font-bold text-sky-700">Flappy Bird</h1>
      <p className="text-lg text-gray-600">Tap to flap. Don&apos;t hit the pipes.</p>
      <Link
        href="/game"
        className="px-10 py-4 bg-sky-500 text-white rounded-xl text-xl font-semibold hover:bg-sky-600 transition"
      >
        Play
      </Link>
    </main>
  );
}
