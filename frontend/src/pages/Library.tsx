import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Search, Clock, BookOpen } from "lucide-react";

const articles = [
  { cat: "1. Trimester", title: "Erken hamilelik belirtileri", desc: "İlk haftalarda vücudunda neler olur?", time: "5 dk" },
  { cat: "Beslenme", title: "Hamilelikte demir ihtiyacı", desc: "Hangi gıdalar demir açısından zengin?", time: "7 dk" },
  { cat: "2. Trimester", title: "Bebeğin ilk hareketleri", desc: "Tekmeleri ne zaman hissedersin?", time: "4 dk" },
  { cat: "Doğum", title: "Doğum çantasında neler olmalı?", desc: "Hastane çantası için tam liste.", time: "6 dk" },
  { cat: "Ruh Sağlığı", title: "Hamilelikte kaygıyla baş etme", desc: "Stresi azaltmak için 7 yöntem.", time: "8 dk" },
  { cat: "3. Trimester", title: "Son hafta hazırlığı", desc: "Doğuma giderken nelere dikkat?", time: "5 dk" },
];

export default function Library() {
  return (
    <div className="p-4 md:p-8 space-y-6 max-w-[1400px] mx-auto">
      <div>
        <h1 className="font-serif text-3xl">Kütüphane</h1>
        <p className="text-muted-foreground mt-1">Hamilelik yolculuğun için rehber yazılar.</p>
      </div>

      <div className="relative max-w-xl">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input placeholder="Konu ara..." className="pl-9 bg-card" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {articles.map((a, i) => (
          <Card
            key={i}
            className="group cursor-pointer shadow-card border-border/60 hover:-translate-y-1 hover:shadow-soft transition overflow-hidden"
          >
            <div className="h-32 bg-gradient-soft grid place-items-center">
              <BookOpen className="h-10 w-10 text-primary/70 group-hover:scale-110 transition" />
            </div>
            <CardContent className="p-5 space-y-2">
              <Badge variant="secondary" className="bg-accent/15 text-foreground hover:bg-accent/20">
                {a.cat}
              </Badge>
              <h3 className="font-serif text-lg leading-snug">{a.title}</h3>
              <p className="text-sm text-muted-foreground line-clamp-2">{a.desc}</p>
              <div className="flex items-center gap-1 text-xs text-muted-foreground pt-2">
                <Clock className="h-3 w-3" /> {a.time} okuma
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
