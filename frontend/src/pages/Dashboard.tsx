import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  HeartPulse,
  Activity,
  CalendarDays,
  Pill,
  Baby,
  Sparkles,
} from "lucide-react";
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiClient } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";

type DashboardUpcoming = {
  id: number;
  title: string;
  time: string;
  tag: string;
  type?: string | null;
};


export default function Dashboard() {
  const { toast } = useToast();
  const navigate = useNavigate();
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const data = await apiClient.getDashboard();
        setDashboardData(data);
      } catch (error) {
        toast({
          title: "Veri yüklenemedi",
          description: "Dashboard verileri alınırken bir hata oluştu",
          variant: "destructive",
        });
      } finally {
        setIsLoading(false);
      }
    };

    fetchDashboard();
  }, [toast]);

  if (isLoading || !dashboardData) {
    return (
      <div className="p-4 md:p-8 space-y-6 max-w-[1400px] mx-auto">
        <div className="animate-pulse space-y-4">
          <div className="h-32 bg-muted rounded-2xl"></div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div className="h-32 bg-muted rounded-xl"></div>
            <div className="h-32 bg-muted rounded-xl"></div>
            <div className="h-32 bg-muted rounded-xl"></div>
          </div>
        </div>
      </div>
    );
  }

  const { hero, summary_cards, weight_chart, weight_gain_label, upcoming } = dashboardData;
  const upcomingList = (Array.isArray(upcoming) ? upcoming : []) as DashboardUpcoming[];
  const { week, total_weeks, days_left, progress_percent, subtitle, headline, summary_text } = hero;

  return (
    <div className="p-4 md:p-8 space-y-6 max-w-[1400px] mx-auto">
      {/* Hero greeting */}
      <div className="rounded-2xl bg-gradient-soft px-6 pt-6 pb-6 md:px-8 md:pt-8 md:pb-0 shadow-card relative overflow-hidden">
        <div className="absolute -right-10 -top-10 h-48 w-48 rounded-full bg-secondary/30 blur-2xl" />
        <div className="relative md:pr-52 lg:pr-64 md:pb-8">
          <p className="text-sm text-muted-foreground">{subtitle}</p>
          <h1 className="font-serif text-3xl md:text-4xl mt-1">
            {headline}
          </h1>
          <p className="text-muted-foreground mt-2 max-w-xl">
            {summary_text}
          </p>
          <div className="mt-5 max-w-md">
            <div className="flex items-center justify-between text-xs text-muted-foreground mb-2">
              <span>Hafta {week}/{total_weeks}</span>
              <span>{progress_percent}%</span>
            </div>
            <Progress value={progress_percent} className="h-2" />
          </div>
        </div>
        <img
          src="/pregnant-mother.png"
          alt="Hamile anne illüstrasyonu"
          className="hidden md:block absolute bottom-0 right-0 h-40 lg:h-48 xl:h-56 w-auto object-contain object-bottom pointer-events-none select-none"
        />
      </div>

      {/* 3-column summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <SummaryCard
          icon={<Baby className="h-5 w-5" />}
          label={summary_cards.baby.label}
          value={summary_cards.baby.value}
          hint={summary_cards.baby.hint}
          accent="bg-secondary/30"
        />
        <SummaryCard
          icon={<HeartPulse className="h-5 w-5" />}
          label={summary_cards.blood_pressure.label}
          value={summary_cards.blood_pressure.value}
          hint={summary_cards.blood_pressure.hint}
          accent="bg-accent/20"
        />
        <SummaryCard
          icon={<Activity className="h-5 w-5" />}
          label={summary_cards.blood_glucose.label}
          value={summary_cards.blood_glucose.value}
          hint={summary_cards.blood_glucose.hint}
          accent="bg-accent-pink/20"
        />
      </div>

      {/* Chart + side */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        <Card className="lg:col-span-2 shadow-card border-border/60">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle className="font-serif text-xl">Kilo Takibi</CardTitle>
              <p className="text-sm text-muted-foreground mt-1">Son 7 ölçüm</p>
            </div>
            <Badge variant="secondary" className="bg-accent/15 text-foreground hover:bg-accent/20">
              {weight_gain_label}
            </Badge>
          </CardHeader>
          <CardContent>
            <div className="h-[260px]">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={weight_chart} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="kg" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="hsl(var(--accent))" stopOpacity={0.45} />
                      <stop offset="100%" stopColor="hsl(var(--accent))" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis dataKey="d" stroke="hsl(var(--muted-foreground))" fontSize={12} />
                  <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} />
                  <Tooltip
                    contentStyle={{
                      background: "hsl(var(--card))",
                      border: "1px solid hsl(var(--border))",
                      borderRadius: 12,
                      color: "hsl(var(--foreground))",
                    }}
                  />
                  <Area
                    type="monotone"
                    dataKey="kg"
                    stroke="hsl(var(--accent))"
                    strokeWidth={2.5}
                    fill="url(#kg)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card className="shadow-card border-border/60">
          <CardHeader>
            <CardTitle className="font-serif text-xl">Yaklaşan</CardTitle>
            <p className="text-sm text-muted-foreground">En yakın 2 takvim etkinliği</p>
          </CardHeader>
          <CardContent className="space-y-3">
            {upcomingList.length === 0 ? (
              <p className="text-sm text-muted-foreground py-2 px-1">
                Önümüzdeki günlerde kayıtlı etkinlik yok. Takvimden ekleyebilirsin.
              </p>
            ) : (
              upcomingList.map((u) => {
                const kind = (u.type || "").toLowerCase();
                const isIlac = kind === "ilac" || u.tag === "İlaç";
                const isRandevu = kind === "randevu" || u.tag === "Randevu";
                const iconWrap = isIlac
                  ? "bg-accent/20 text-foreground"
                  : isRandevu
                    ? "bg-accent-pink/20 text-foreground"
                    : "bg-secondary/40 text-foreground";
                return (
                  <div key={u.id} className="flex items-start gap-3 p-3 rounded-xl bg-muted/40">
                    <div className={`h-9 w-9 rounded-lg grid place-items-center ${iconWrap}`}>
                      {isIlac ? <Pill className="h-4 w-4" /> : <CalendarDays className="h-4 w-4" />}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-foreground truncate">{u.title}</p>
                      <p className="text-xs text-muted-foreground">{u.time}</p>
                    </div>
                    <Badge variant="outline" className="text-[10px] border-border/60 shrink-0">
                      {u.tag}
                    </Badge>
                  </div>
                );
              })
            )}
            <Button variant="outline" className="w-full mt-2" type="button" onClick={() => navigate("/takvim")}>
              Tüm takvimi gör
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* AI nudge */}
      <Card className="border-secondary/40 bg-gradient-warm/40 shadow-card">
        <CardContent className="flex flex-col md:flex-row items-start md:items-center gap-4 p-6">
          <div className="h-12 w-12 rounded-full bg-secondary grid place-items-center text-secondary-foreground shadow-glow">
            <Sparkles className="h-5 w-5" />
          </div>
          <div className="flex-1">
            <h3 className="font-serif text-lg">Gebelik Asistanı ile sohbet et</h3>
            <p className="text-sm text-muted-foreground">
              Gebelik sürecin, bebeğinin gelişimi veya sağlık kayıtların hakkında soru sor.
            </p>
          </div>
          <Button
            className="bg-secondary text-secondary-foreground hover:brightness-105"
            type="button"
            onClick={() => navigate("/bebegimle-konus")}
          >
            Gebelik Asistanı
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}

function SummaryCard({
  icon,
  label,
  value,
  hint,
  accent,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
  hint: string;
  accent: string;
}) {
  return (
    <Card className="shadow-card border-border/60">
      <CardContent className="p-5 flex items-center gap-4">
        <div className={`h-12 w-12 rounded-xl grid place-items-center ${accent} text-foreground`}>
          {icon}
        </div>
        <div>
          <p className="text-xs text-muted-foreground uppercase tracking-wide">{label}</p>
          <p className="font-serif text-2xl mt-0.5">{value}</p>
          <p className="text-xs text-muted-foreground">{hint}</p>
        </div>
      </CardContent>
    </Card>
  );
}
