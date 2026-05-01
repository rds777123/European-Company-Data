import type { APIResponse, UserOut, ScoreOut, LeaderboardEntry } from "@/types";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<APIResponse<T>> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  return res.json() as Promise<APIResponse<T>>;
}

export const api = {
  users: {
    register: (username: string, password: string) =>
      request<UserOut>("/users/register", {
        method: "POST",
        body: JSON.stringify({ username, password }),
      }),
    get: (userId: number) => request<UserOut>(`/users/${userId}`),
  },
  scores: {
    submit: (userId: number, value: number) =>
      request<ScoreOut>(`/scores/${userId}`, {
        method: "POST",
        body: JSON.stringify({ value }),
      }),
    leaderboard: () => request<LeaderboardEntry[]>("/scores/leaderboard"),
    forUser: (userId: number) => request<ScoreOut[]>(`/scores/${userId}`),
  },
};
