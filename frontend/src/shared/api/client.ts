const apiBaseUrl = process.env.EXPO_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

interface RequestOptions extends RequestInit {
  token: string;
}

export async function requestApi<T>({ token, ...options }: RequestOptions, path: string): Promise<T> {
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  const response = await fetch(`${apiBaseUrl}${normalizedPath}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
      ...(options.headers || {}),
    },
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "API error");
  }
  return response.json() as Promise<T>;
}
