import { useCallback, useEffect, useState } from "react";
import { Outlet, useNavigate } from "react-router-dom";
import { useTheme } from "next-themes";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/AppSidebar";
import { NotificationDropdown } from "@/components/NotificationDropdown";
import { LogOut } from "lucide-react";
import { apiClient } from "@/lib/api";
import { clearAuth, getUserName, setUserName } from "@/lib/authStorage";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

type CurrentUser = {
  name?: string;
  email?: string;
};

/** Ad soyadın ilk kelimesinin (ad) ilk harfi — rozet / avatar kısaltması. */
function avatarInitial(name: string): string {
  const t = name.trim();
  if (!t) return "?";
  const word = t.split(/\s+/).find(Boolean) ?? t;
  const ch = word[0] ?? "?";
  return ch.toLocaleUpperCase("tr-TR");
}

/** Üst çubukta gösterim: veritabanında kullanıcının girdiği gibi kalır, sadece ekranda Türkçe büyük harf. */
function nameForHeader(name: string): string {
  const t = name.trim();
  if (!t) return "";
  return t.toLocaleUpperCase("tr-TR");
}

export default function AppLayout() {
  const navigate = useNavigate();
  const { resolvedTheme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  const [displayName, setDisplayName] = useState(
    () => getUserName()?.trim() ?? ""
  );
  const [userEmail, setUserEmail] = useState("");

  const handleLogout = useCallback(async () => {
    try {
      await apiClient.logout();
    } catch {
      // Ağ veya sunucu hatası: istemci oturumunu yine de kapat
    }
    clearAuth();
    navigate("/giris", { replace: true });
  }, [navigate]);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const me = (await apiClient.getCurrentUser()) as CurrentUser;
        if (cancelled) return;
        if (me?.name?.trim()) {
          const n = me.name.trim();
          setDisplayName(n);
          setUserName(n);
        }
        if (me?.email?.trim()) {
          setUserEmail(me.email.trim());
        }
      } catch {
        // Oturum yoksa veya ağ hatası: mevcut oturum adı / boş kalır
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const isDark = mounted && resolvedTheme === "dark";
  const initial = avatarInitial(displayName);

  const toggleTheme = () => {
    setTheme(isDark ? "light" : "dark");
  };

  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full bg-background">
        <AppSidebar />
        <div className="flex-1 flex flex-col min-w-0">
          <header className="h-16 flex items-center gap-3 border-b border-border bg-card px-4 md:px-6">
            <SidebarTrigger className="text-foreground shrink-0" />
            <div className="flex-1 min-w-0 ml-1 md:ml-2">
              <p className="font-serif text-lg md:text-xl text-foreground truncate tracking-wide">
                {nameForHeader(displayName) || "—"}
              </p>
            </div>
            <div className="ml-auto flex items-center gap-3 shrink-0">
              <NotificationDropdown />
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <button
                    type="button"
                    className="h-9 w-9 rounded-full bg-gradient-primary grid place-items-center text-primary-foreground font-serif text-sm outline-none ring-offset-background hover:opacity-95 focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    aria-label="Hesap menüsü"
                  >
                    {initial}
                  </button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-56">
                  <DropdownMenuLabel className="font-normal">
                    <div className="flex flex-col gap-1 py-0.5">
                      <p className="font-serif text-sm font-medium leading-none text-foreground">
                        {displayName || "Kullanıcı"}
                      </p>
                      {userEmail && (
                        <p className="text-xs text-muted-foreground truncate">
                          {userEmail}
                        </p>
                      )}
                    </div>
                  </DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem
                    className="cursor-pointer"
                    onSelect={(e) => {
                      e.preventDefault();
                      toggleTheme();
                    }}
                  >
                    {mounted && isDark ? "☀️ Açık Moda Geç" : "🌙 Koyu Moda Geç"}
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem
                    className="cursor-pointer"
                    onSelect={() => {
                      void handleLogout();
                    }}
                  >
                    <LogOut className="mr-2 h-4 w-4" />
                    Çıkış Yap
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </header>
          <main className="flex-1 min-h-0 overflow-y-auto overflow-x-hidden">
            <Outlet />
          </main>
        </div>
      </div>
    </SidebarProvider>
  );
}
