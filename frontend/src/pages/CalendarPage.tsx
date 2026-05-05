import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Calendar } from "@/components/ui/calendar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Plus, Clock, MapPin } from "lucide-react";

const events = [
  { day: "Pzt", date: 5, title: "Folik asit", time: "09:00", type: "ilac" },
  { day: "Sal", date: 6, title: "Dr. Ayşe — Kontrol", time: "14:30", type: "randevu", place: "MedPark Hastanesi" },
  { day: "Çar", date: 7, title: "Yoga sınıfı", time: "18:00", type: "etkinlik" },
  { day: "Per", date: 8, title: "Folik asit", time: "09:00", type: "ilac" },
  { day: "Cum", date: 9, title: "Şeker tarama testi", time: "10:00", type: "randevu", place: "Lab" },
  { day: "Cmt", date: 10, title: "Yürüyüş", time: "08:00", type: "etkinlik" },
  { day: "Paz", date: 11, title: "Dinlenme", time: "—", type: "etkinlik" },
];

const colorOf = (t: string) =>
  t === "randevu"
    ? "bg-accent-pink/25 border-l-accent-pink"
    : t === "ilac"
    ? "bg-accent/20 border-l-accent"
    : "bg-secondary/30 border-l-secondary";

export default function CalendarPage() {
  const [date, setDate] = useState<Date | undefined>(new Date());

  return (
    <div className="p-4 md:p-8 space-y-6 max-w-[1400px] mx-auto">
      <div className="flex items-end justify-between flex-wrap gap-3">
        <div>
          <h1 className="font-serif text-3xl">Takvim</h1>
          <p className="text-muted-foreground mt-1">Randevuların ve ilaç hatırlatıcıların.</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" /> Yeni Etkinlik
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[320px,1fr] gap-6">
        <Card className="shadow-card border-border/60">
          <CardHeader>
            <CardTitle className="font-serif text-lg">Ay Görünümü</CardTitle>
          </CardHeader>
          <CardContent>
            <Calendar
              mode="single"
              selected={date}
              onSelect={setDate}
              className="p-0 pointer-events-auto"
            />
            <div className="mt-4 space-y-2 text-sm">
              <Legend color="bg-accent-pink" label="Randevu" />
              <Legend color="bg-accent" label="İlaç" />
              <Legend color="bg-secondary" label="Etkinlik" />
            </div>
          </CardContent>
        </Card>

        <Card className="shadow-card border-border/60">
          <CardHeader>
            <CardTitle className="font-serif text-xl">Bu Hafta</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-7 gap-3">
              {events.map((e, i) => (
                <div key={i} className="space-y-2">
                  <div className="text-center pb-2 border-b border-border/60">
                    <p className="text-xs text-muted-foreground">{e.day}</p>
                    <p className="font-serif text-xl">{e.date}</p>
                  </div>
                  <div
                    className={`rounded-lg border-l-4 p-2.5 ${colorOf(e.type)} shadow-sm`}
                  >
                    <p className="text-xs font-semibold text-foreground leading-tight">{e.title}</p>
                    <div className="flex items-center gap-1 mt-1.5 text-[11px] text-muted-foreground">
                      <Clock className="h-3 w-3" />
                      {e.time}
                    </div>
                    {e.place && (
                      <div className="flex items-center gap-1 mt-0.5 text-[11px] text-muted-foreground">
                        <MapPin className="h-3 w-3" />
                        {e.place}
                      </div>
                    )}
                    <Badge variant="outline" className="mt-2 text-[10px] capitalize border-border/60">
                      {e.type}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function Legend({ color, label }: { color: string; label: string }) {
  return (
    <div className="flex items-center gap-2">
      <span className={`h-3 w-3 rounded-sm ${color}`} />
      <span className="text-foreground/80">{label}</span>
    </div>
  );
}
