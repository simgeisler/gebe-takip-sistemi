import { useCallback, useEffect, useState } from "react";
import { Outlet, useNavigate } from "react-router-dom";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/AppSidebar";
import { Bell, LogOut } from "lucide-react";
import { apiClient } from "@/lib/api";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

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
  const [displayName, setDisplayName] = useState(
    () => localStorage.getItem("user_name")?.trim() ?? ""
  );

  const handleLogout = useCallback(async () => {
    try {
      await apiClient.logout();
    } catch {
      // Ağ veya sunucu hatası: istemci oturumunu yine de kapat
    }
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_name");
    navigate("/giris", { replace: true });
  }, [navigate]);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const me = (await apiClient.getCurrentUser()) as { name?: string };
        if (cancelled || !me?.name?.trim()) return;
        const n = me.name.trim();
        setDisplayName(n);
        localStorage.setItem("user_name", n);
      } catch {
        // Oturum yoksa veya ağ hatası: mevcut localStorage / boş kalır
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const initial = avatarInitial(displayName);

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
              <button type="button" className="relative h-9 w-9 grid place-items-center rounded-full hover:bg-muted transition">
                <Bell className="h-[18px] w-[18px] text-foreground" />
                <span className="absolute top-2 right-2 h-2 w-2 rounded-full bg-secondary" />
              </button>
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
                <DropdownMenuContent align="end" className="w-48">
                  <DropdownMenuItem
                    className="cursor-pointer"
                    onSelect={() => {
                      void handleLogout();
                    }}
                  >
                    <LogOut className="mr-2 h-4 w-4" />
                    Çıkış yap
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
