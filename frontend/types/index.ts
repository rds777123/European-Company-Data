// Mirrors backend Pydantic schemas — keep in sync with backend/schemas/

export interface APIResponse<T> {
  data: T | null;
  error: string | null;
}

export interface UserOut {
  id: number;
  username: string;
  created_at: string; // ISO 8601
}

export interface ScoreOut {
  id: number;
  user_id: number;
  value: number;
  recorded_at: string; // ISO 8601
}

export interface LeaderboardEntry {
  rank: number;
  username: string;
  best_score: number;
}
