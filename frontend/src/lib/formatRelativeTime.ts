import { useEffect, useState } from "react";

function formatClock(date: Date): string {
  const hh = String(date.getHours()).padStart(2, "0");
  const mm = String(date.getMinutes()).padStart(2, "0");
  return hh + ":" + mm;
}

/** Bugun / dun / tam tarih-saat. */
export function formatRelativeTimeTr(
  input: string | Date | null | undefined,
  now = new Date(),
): string {
  if (!input) return "—";

  const date = typeof input === "string" ? new Date(input) : input;
  if (Number.isNaN(date.getTime())) return "—";

  const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const startOfYesterday = new Date(startOfToday);
  startOfYesterday.setDate(startOfYesterday.getDate() - 1);

  if (date >= startOfToday) {
    return "Bugün saat " + formatClock(date);
  }

  if (date >= startOfYesterday && date < startOfToday) {
    return "Dün saat " + formatClock(date);
  }

  const day = String(date.getDate()).padStart(2, "0");
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const year = date.getFullYear();
  return day + "." + month + "." + year + " " + formatClock(date);
}

/** Gece yarisinda etiketlerin guncellenmesi icin. */
export function useRelativeNow(intervalMs = 60_000): Date {
  const [now, setNow] = useState(() => new Date());

  useEffect(() => {
    const id = window.setInterval(() => setNow(new Date()), intervalMs);
    return () => window.clearInterval(id);
  }, [intervalMs]);

  return now;
}
