import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  HeartPulse,
  Apple,
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

const weightData = [
  { w: "H8", kg: 62 },
  { w: "H12", kg: 63.2 },
  { w: "H16", kg: 64.5 },
  { w: "H20", kg: 66 },
  { w: "H24", kg: 68 },
  { w: "H28", kg: 69.4 },
  { w: "H32", kg: 71 },
];

const upcoming = [
  { title: "Doktor kontrolü — Dr. Ayşe", time: "Salı, 14:30", tag: "Randevu", color: "bg-accent-pink/20 text-foreground" },
  { title: "Folik asit", time: "Her sabah 09:00", tag: "İlaç", color: "bg-accent/20 text-foreground" },
  { title: "Şeker tarama testi", time: "Önümüzdeki hafta", tag: "Test", color: "bg-secondary/40 text-foreground" },
];

export default function Dashboard() {
  const week = 28;
  const totalWeeks = 40;
  const daysLeft = (totalWeeks - week) * 7 - 2;
  const progress = (week / totalWeeks) * 100;

  return (
    <div className="p-4 md:p-8 space-y-6 max-w-[1400px] mx-auto">
      {/* Hero greeting */}
      <div className="rounded-2xl bg-gradient-soft p-6 md:p-8 shadow-card relative overflow-hidden">
        <div className="absolute -right-10 -top-10 h-48 w-48 rounded-full bg-secondary/30 blur-2xl" />
        <div className="relative">
          <p className="text-sm text-muted-foreground">Merhaba Elif 🌸</p>
          <h1 className="font-serif text-3xl md:text-4xl mt-1">
            Bebeğine kavuşmana <span className="text-primary">{daysLeft} gün</span> kaldı
          </h1>
          <p className="text-muted-foreground mt-2 max-w-xl">
            Şu an <strong className="text-foreground">{week}. haftadasın</strong>. Bebeğin bir patlıcan büyüklüğünde
            ve seni duyabiliyor 💛
          </p>
          <div className="mt-5 max-w-md">
            <div className="flex items-center justify-between text-xs text-muted-foreground mb-2">
              <span>Hafta {week}/{totalWeeks}</span>
              <span>{Math.round(progress)}%</span>
            </div>
            <Progress value={progress} className="h-2" />
          </div>
        </div>
      </div>

      {/* 3-column summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <SummaryCard
          icon={<Baby className="h-5 w-5" />}
          label="Bebek Durumu"
          value="~ 1 kg"
          hint="Boy: 38 cm"
          accent="bg-secondary/30"
        />
        <SummaryCard
          icon={<HeartPulse className="h-5 w-5" />}
          label="Son Tansiyon"
          value="118 / 76"
          hint="3 gün önce ölçüldü"
          accent="bg-accent/20"
        />
        <SummaryCard
          icon={<Apple className="h-5 w-5" />}
          label="Bugünkü Su"
          value="1.8 L"
          hint="Hedef: 2.5 L"
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
              +9 kg toplam
            </Badge>
          </CardHeader>
          <CardContent>
            <div className="h-[260px]">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={weightData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="kg" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="hsl(var(--accent))" stopOpacity={0.45} />
                      <stop offset="100%" stopColor="hsl(var(--accent))" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis dataKey="w" stroke="hsl(var(--muted-foreground))" fontSize={12} />
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
            <p className="text-sm text-muted-foreground">Randevu ve hatırlatıcılar</p>
          </CardHeader>
          <CardContent className="space-y-3">
            {upcoming.map((u, i) => (
              <div key={i} className="flex items-start gap-3 p-3 rounded-xl bg-muted/40">
                <div className={`h-9 w-9 rounded-lg grid place-items-center ${u.color}`}>
                  {u.tag === "İlaç" ? (
                    <Pill className="h-4 w-4" />
                  ) : (
                    <CalendarDays className="h-4 w-4" />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-foreground truncate">{u.title}</p>
                  <p className="text-xs text-muted-foreground">{u.time}</p>
                </div>
                <Badge variant="outline" className="text-[10px] border-border/60">
                  {u.tag}
                </Badge>
              </div>
            ))}
            <Button variant="outline" className="w-full mt-2">
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
            <h3 className="font-serif text-lg">Bebeğinle bir sohbet başlat</h3>
            <p className="text-sm text-muted-foreground">
              Bugün nasıl hissettiğini yaz, bebeğin sana cevap versin.
            </p>
          </div>
          <Button className="bg-secondary text-secondary-foreground hover:brightness-105">
            Bebeğimle Konuş
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
