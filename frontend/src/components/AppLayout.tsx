import { Outlet } from "react-router-dom";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/AppSidebar";
import { Bell, Search } from "lucide-react";
import { Input } from "@/components/ui/input";

export default function AppLayout() {
  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full bg-background">
        <AppSidebar />
        <div className="flex-1 flex flex-col min-w-0">
          <header className="h-16 flex items-center gap-3 border-b border-border bg-card px-4 md:px-6">
            <SidebarTrigger className="text-foreground" />
            <div className="hidden md:flex items-center gap-2 max-w-md flex-1 ml-2">
              <div className="relative w-full">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Ara: makale, randevu, ilaç..."
                  className="pl-9 bg-muted/50 border-transparent focus-visible:bg-background"
                />
              </div>
            </div>
            <div className="ml-auto flex items-center gap-3">
              <button className="relative h-9 w-9 grid place-items-center rounded-full hover:bg-muted transition">
                <Bell className="h-[18px] w-[18px] text-foreground" />
                <span className="absolute top-2 right-2 h-2 w-2 rounded-full bg-secondary" />
              </button>
              <div className="h-9 w-9 rounded-full bg-gradient-primary grid place-items-center text-primary-foreground font-serif">
                E
              </div>
            </div>
          </header>
          <main className="flex-1 overflow-x-hidden">
            <Outlet />
          </main>
        </div>
      </div>
    </SidebarProvider>
  );
}
