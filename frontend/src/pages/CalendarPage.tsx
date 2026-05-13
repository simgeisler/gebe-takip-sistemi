import { useState, useEffect } from "react";
import { format, isSameDay, parseISO } from "date-fns";
import { tr } from "date-fns/locale";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Calendar } from "@/components/ui/calendar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Plus, Clock, MapPin, Trash2 } from "lucide-react";
import { apiClient } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";
import { toast } from "sonner";

type EventType = "ilac" | "randevu" | "etkinlik";

type CalendarEventRow = {
  id: number;
  day?: string | null;
  date?: number | null;
  event_on?: string | null;
  title: string;
  time?: string | null;
  type?: EventType | null;
  place?: string | null;
};

const colorOf = (t: string) =>
  t === "randevu"
    ? "bg-accent-pink/25 border-l-accent-pink"
    : t === "ilac"
      ? "bg-accent/20 border-l-accent"
      : "bg-secondary/30 border-l-secondary";

/** API satırından takvim günü (event_on varsa onu, yoksa mevcut ay + date). */
function eventAsDate(e: CalendarEventRow): Date {
  if (e.event_on) {
    try {
      const s = e.event_on.length > 10 ? e.event_on : `${e.event_on}T12:00:00`;
      return parseISO(s);
    } catch {
      /* ignore */
    }
  }
  const now = new Date();
  const d = typeof e.date === "number" ? e.date : 1;
  return new Date(now.getFullYear(), now.getMonth(), d);
}

export default function CalendarPage() {
  const { toast: pushToast } = useToast();
  const [date, setDate] = useState<Date | undefined>(new Date());
  const [events, setEvents] = useState<CalendarEventRow[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selectedDate, setSelectedDate] = useState<Date>(new Date());
  const [eventType, setEventType] = useState<EventType>("ilac");

  const loadEvents = async () => {
    try {
      const data = (await apiClient.getCalendarEvents()) as CalendarEventRow[];
      setEvents(Array.isArray(data) ? data : []);
    } catch {
      pushToast({
        title: "Veri yüklenemedi",
        description: "Takvim etkinlikleri alınırken bir hata oluştu",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    void loadEvents();
  }, []);

  const handleAddEvent = () => {
    setSelectedDate(date || new Date());
    setEventType("ilac");
    setIsDialogOpen(true);
  };

  const handleSubmitEvent = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const title = (formData.get("title") as string)?.trim();
    const time = (formData.get("time") as string)?.trim();
    const placeRaw = (formData.get("place") as string)?.trim();

    if (!title || !time) {
      toast.error("Başlık ve saat zorunludur.");
      return;
    }

    const eventData = {
      day: selectedDate.toLocaleDateString("tr-TR", { weekday: "long" }),
      date: selectedDate.getDate(),
      event_on: format(selectedDate, "yyyy-MM-dd"),
      title,
      time,
      type: eventType,
      place: placeRaw || undefined,
    };

    try {
      await apiClient.createCalendarEvent(eventData);
      await loadEvents();
      toast.success("Etkinlik kaydedildi");
      setIsDialogOpen(false);
      e.currentTarget.reset();
      setEventType("ilac");
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Kayıt başarısız";
      toast.error(msg);
    }
  };

  const handleDeleteEvent = async (eventId: number) => {
    try {
      await apiClient.deleteCalendarEvent(eventId);
      await loadEvents();
      toast.success("Etkinlik silindi");
    } catch {
      toast.error("Etkinlik silinemedi");
    }
  };

  return (
    <div className="p-4 md:p-8 space-y-6 max-w-[1400px] mx-auto">
      <div className="flex items-end justify-between flex-wrap gap-3">
        <div>
          <h1 className="font-serif text-3xl">Takvim</h1>
          <p className="text-muted-foreground mt-1">Randevuların ve ilaç hatırlatıcıların.</p>
        </div>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button onClick={handleAddEvent}>
              <Plus className="h-4 w-4 mr-2" /> Yeni Etkinlik
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Yeni Etkinlik</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmitEvent} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="event-date">Tarih</Label>
                <Input
                  id="event-date"
                  value={selectedDate.toLocaleDateString("tr-TR")}
                  disabled
                  className="bg-muted"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="title">Başlık</Label>
                <Input id="title" name="title" placeholder="Etkinlik başlığı" required />
              </div>
              <div className="space-y-2">
                <Label htmlFor="time">Saat</Label>
                <Input id="time" name="time" type="time" required />
              </div>
              <div className="space-y-2">
                <Label>Kategori</Label>
                <Select value={eventType} onValueChange={(v) => setEventType(v as EventType)} required>
                  <SelectTrigger>
                    <SelectValue placeholder="Kategori seç" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="ilac">İlaç</SelectItem>
                    <SelectItem value="randevu">Randevu</SelectItem>
                    <SelectItem value="etkinlik">Etkinlik</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="place">Konum (isteğe bağlı)</Label>
                <Input id="place" name="place" placeholder="Konum bilgisi" />
              </div>
              <div className="flex justify-end space-x-2">
                <Button type="button" variant="outline" onClick={() => setIsDialogOpen(false)}>
                  İptal
                </Button>
                <Button type="submit" disabled={isLoading}>
                  Kaydet
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
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
              modifiers={{
                hasEvent: (day) =>
                  events.some((ev) => isSameDay(eventAsDate(ev), day)),
              }}
              modifiersClassNames={{
                hasEvent: "relative",
              }}
              components={{
                DayContent: ({ date: day }) => {
                  const dayEvents = events.filter((ev) => isSameDay(eventAsDate(ev), day));
                  return (
                    <div className="relative w-full h-full flex flex-col items-center">
                      <span>{day.getDate()}</span>
                      {dayEvents.length > 0 && (
                        <div className="flex gap-0.5 mt-1">
                          {dayEvents.slice(0, 3).map((event, idx) => (
                            <div
                              key={event.id ?? idx}
                              className={`w-1.5 h-1.5 rounded-full ${
                                event.type === "randevu"
                                  ? "bg-accent-pink"
                                  : event.type === "ilac"
                                    ? "bg-accent"
                                    : "bg-secondary"
                              }`}
                            />
                          ))}
                        </div>
                      )}
                    </div>
                  );
                },
              }}
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
            <CardTitle className="font-serif text-xl">Tüm Etkinlikler</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {events.map((ev) => (
                <div
                  key={ev.id}
                  className={`rounded-lg border-l-4 p-3 ${colorOf(ev.type || "etkinlik")} shadow-sm relative`}
                >
                  <Button
                    size="sm"
                    variant="ghost"
                    className="absolute top-2 right-2 h-6 w-6 p-0 hover:bg-destructive/20"
                    type="button"
                    onMouseDown={(clickEv) => {
                      clickEv.preventDefault();
                      clickEv.stopPropagation();
                      void handleDeleteEvent(ev.id);
                    }}
                  >
                    <Trash2 className="h-3 w-3 text-destructive" />
                  </Button>
                  <div className="space-y-2">
                    <div className="flex items-start justify-between">
                      <div className="flex-1 pr-10">
                        <p className="text-sm font-semibold text-foreground leading-tight">{ev.title}</p>
                        <div className="flex items-center gap-3 mt-2 text-xs text-muted-foreground flex-wrap">
                          <div className="flex items-center gap-1">
                            <Clock className="h-3 w-3" />
                            {ev.time}
                          </div>
                          <div className="flex items-center gap-1">
                            <span className="font-medium">{ev.day}</span>
                            {ev.event_on ? (
                              <span>{format(eventAsDate(ev), "d MMM yyyy", { locale: tr })}</span>
                            ) : (
                              <span>{ev.date}</span>
                            )}
                          </div>
                          {ev.place && (
                            <div className="flex items-center gap-1">
                              <MapPin className="h-3 w-3" />
                              {ev.place}
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <div />
                      <Badge variant="outline" className="text-xs capitalize border-border/60">
                        {ev.type}
                      </Badge>
                    </div>
                  </div>
                </div>
              ))}
              {events.length === 0 && !isLoading && (
                <div className="text-center py-8 text-muted-foreground">Henüz etkinlik bulunmuyor</div>
              )}
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
