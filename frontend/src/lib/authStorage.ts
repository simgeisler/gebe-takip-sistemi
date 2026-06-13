const TOKEN_KEY = "access_token";
const USER_NAME_KEY = "user_name";

/** Eski localStorage oturumunu yalnızca bu sekmeye taşır (sekmeler arası paylaşım yok). */
function migrateLegacyLocalStorageOnce(): void {
  if (sessionStorage.getItem(TOKEN_KEY)) return;
  const legacyToken = localStorage.getItem(TOKEN_KEY);
  if (!legacyToken) return;
  sessionStorage.setItem(TOKEN_KEY, legacyToken);
  const legacyName = localStorage.getItem(USER_NAME_KEY);
  if (legacyName) sessionStorage.setItem(USER_NAME_KEY, legacyName);
}

export function getAccessToken(): string | null {
  migrateLegacyLocalStorageOnce();
  return sessionStorage.getItem(TOKEN_KEY);
}

export function setAccessToken(token: string): void {
  sessionStorage.setItem(TOKEN_KEY, token);
}

export function getUserName(): string | null {
  migrateLegacyLocalStorageOnce();
  return sessionStorage.getItem(USER_NAME_KEY);
}

export function setUserName(name: string): void {
  sessionStorage.setItem(USER_NAME_KEY, name);
}

export function clearAuth(): void {
  sessionStorage.removeItem(TOKEN_KEY);
  sessionStorage.removeItem(USER_NAME_KEY);
}

export function hasAuth(): boolean {
  return Boolean(getAccessToken());
}
