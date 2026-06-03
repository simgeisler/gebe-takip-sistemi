import { NavLink, useLocation } from "react-router-dom";
import {
  LayoutDashboard,
  HeartPulse,
  CalendarDays,
  BookOpen,
  MessagesSquare,
  Sparkles,
  Baby,
} from "lucide-react";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@/components/ui/sidebar";

const items = [
  { title: "Dashboard", url: "/dashboard", icon: LayoutDashboard },
  { title: "Sağlık Takibi", url: "/saglik", icon: HeartPulse },
  { title: "Takvim", url: "/takvim", icon: CalendarDays },
  { title: "Kütüphane", url: "/kutuphane", icon: BookOpen },
  { title: "Forum", url: "/forum", icon: MessagesSquare },
];

export function AppSidebar() {
  const { state } = useSidebar();
  const collapsed = state === "collapsed";
  const { pathname } = useLocation();
  const isActive = (path: string) => pathname === path;

  return (
    <Sidebar collapsible="icon" className="border-r-0">
      <SidebarHeader className="px-4 py-5">
        <div className="flex items-center gap-2.5">
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-sidebar-primary text-sidebar-primary-foreground">
            <Baby className="h-5 w-5" />
          </div>
          {!collapsed && (
            <div>
              <p className="font-serif text-lg leading-none">Bebeğim</p>
              <p className="text-xs text-sidebar-foreground/70 mt-0.5">Gebelik Takip</p>
            </div>
          )}
        </div>
      </SidebarHeader>

      <SidebarContent className="px-2">
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu className="gap-1">
              {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton
                    asChild
                    isActive={isActive(item.url)}
                    className="data-[active=true]:bg-sidebar-accent data-[active=true]:text-sidebar-accent-foreground hover:bg-sidebar-accent/60 hover:text-sidebar-accent-foreground rounded-lg h-10"
                  >
                    <NavLink to={item.url} className="flex items-center gap-3">
                      <item.icon className="h-[18px] w-[18px]" />
                      {!collapsed && <span className="font-medium">{item.title}</span>}
                    </NavLink>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter className="p-3">
        <NavLink
          to="/bebegimle-konus"
          className="group relative flex items-center gap-2.5 rounded-xl bg-secondary px-4 py-3 text-secondary-foreground shadow-glow transition hover:brightness-105"
        >
          <Sparkles className="h-5 w-5 shrink-0" />
          {!collapsed && (
            <div className="flex-1">
              <p className="font-serif text-sm leading-tight">Gebelik Asistanı</p>
              <p className="text-[11px] opacity-80">AI destekli sohbet</p>
            </div>
          )}
        </NavLink>
      </SidebarFooter>
    </Sidebar>
  );
}
