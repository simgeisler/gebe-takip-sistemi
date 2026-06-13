import { useCallback, useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Bell } from "lucide-react";
import { apiClient, type NotificationItem } from "@/lib/api";
import { getAccessToken, hasAuth } from "@/lib/authStorage";
import { cn } from "@/lib/utils";

const POLL_INTERVAL_MS = 15_000;

function notificationMessage(item: NotificationItem): string {
  if (item.type === "like") {
    return `${item.actor_name} sorunu beğendi`;
  }
  return `${item.actor_name} soruna yorum yaptı`;
}

export function NotificationDropdown() {
  const navigate = useNavigate();
  const containerRef = useRef<HTMLDivElement>(null);
  const [open, setOpen] = useState(false);
  const [notifications, setNotifications] = useState<NotificationItem[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [loading, setLoading] = useState(false);

  const hasToken = hasAuth();

  const fetchUnreadCount = useCallback(async () => {
    if (!getAccessToken()) return;
    try {
      const data = await apiClient.getNotificationUnreadCount();
      setUnreadCount(data.unread_count);
    } catch {
      // Oturum yoksa veya ağ hatası
    }
  }, []);

  const fetchNotifications = useCallback(async () => {
    if (!getAccessToken()) return;
    setLoading(true);
    try {
      const data = await apiClient.getNotifications();
      setNotifications(data.notifications);
      setUnreadCount(data.unread_count);
    } catch {
      // Oturum yoksa veya ağ hatası
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!hasToken) return;
    void fetchUnreadCount();
    const interval = window.setInterval(() => {
      void fetchUnreadCount();
    }, POLL_INTERVAL_MS);
    return () => window.clearInterval(interval);
  }, [hasToken, fetchUnreadCount]);

  useEffect(() => {
    if (!open) return;
    void fetchNotifications();
  }, [open, fetchNotifications]);

  useEffect(() => {
    if (!open) return;
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [open]);

  const handleNotificationClick = async (item: NotificationItem) => {
    if (!item.is_read) {
      try {
        await apiClient.markNotificationRead(item.id);
        setNotifications((prev) =>
          prev.map((n) => (n.id === item.id ? { ...n, is_read: true } : n))
        );
        setUnreadCount((prev) => Math.max(0, prev - 1));
      } catch {
        return;
      }
    }
    setOpen(false);
    navigate(`/forum/${item.question_id}`);
  };

  const handleMarkAllRead = async () => {
    try {
      await apiClient.markAllNotificationsRead();
      setNotifications((prev) => prev.map((n) => ({ ...n, is_read: true })));
      setUnreadCount(0);
    } catch {
      // Ağ hatası
    }
  };

  if (!hasToken) {
    return (
      <button
        type="button"
        className="relative h-9 w-9 grid place-items-center rounded-full hover:bg-muted transition"
        aria-label="Bildirimler"
      >
        <Bell className="h-[18px] w-[18px] text-foreground" />
      </button>
    );
  }

  return (
    <div ref={containerRef} className="relative">
      <button
        type="button"
        onClick={() => setOpen((prev) => !prev)}
        className="relative h-9 w-9 grid place-items-center rounded-full hover:bg-muted transition"
        aria-label="Bildirimler"
        aria-expanded={open}
      >
        <Bell className="h-[18px] w-[18px] text-foreground" />
        {unreadCount > 0 && (
          <span className="absolute -top-0.5 -right-0.5 min-w-[18px] h-[18px] px-1 flex items-center justify-center rounded-full bg-destructive text-destructive-foreground text-[10px] font-semibold leading-none">
            {unreadCount > 99 ? "99+" : unreadCount}
          </span>
        )}
      </button>

      {open && (
        <div
          className="absolute right-0 top-full mt-2 z-50 w-[min(400px,calc(100vw-2rem))] rounded-[12px] bg-popover shadow-card border border-border overflow-hidden"
          style={{ width: "400px" }}
        >
          <div className="flex items-center justify-between px-4 py-3 border-b border-border/60">
            <h3 className="font-serif text-base font-semibold text-foreground">Bildirimler</h3>
            {unreadCount > 0 && (
              <button
                type="button"
                onClick={() => void handleMarkAllRead()}
                className="text-xs text-primary hover:underline font-medium"
              >
                Tümünü Okundu İşaretle
              </button>
            )}
          </div>

          <div className="max-h-[420px] overflow-y-auto">
            {loading && notifications.length === 0 ? (
              <p className="px-4 py-8 text-center text-sm text-muted-foreground">Yükleniyor…</p>
            ) : notifications.length === 0 ? (
              <p className="px-4 py-8 text-center text-sm text-muted-foreground">
                Henüz bildiriminiz yok.
              </p>
            ) : (
              notifications.map((item) => (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => void handleNotificationClick(item)}
                  className={cn(
                    "w-full text-left px-4 py-3 flex gap-3 items-start border-b border-border/30 last:border-b-0 transition-colors hover:bg-muted/40",
                    !item.is_read && "bg-primary/10"
                  )}
                >
                  <span className="text-lg shrink-0 mt-0.5" aria-hidden>
                    {item.type === "like" ? "❤️" : "💬"}
                  </span>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-foreground leading-snug">
                      {notificationMessage(item)}
                    </p>
                    <p className="text-sm text-muted-foreground mt-1 truncate">
                      &ldquo;{item.question_title}&rdquo;
                    </p>
                    <p className="text-xs text-muted-foreground/80 mt-1">{item.time_label}</p>
                  </div>
                  {!item.is_read && (
                    <span className="shrink-0 mt-2 h-2 w-2 rounded-full bg-destructive" aria-hidden />
                  )}
                </button>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}
