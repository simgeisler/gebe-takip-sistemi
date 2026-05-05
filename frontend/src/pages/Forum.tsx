import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { MessageCircle, ArrowUp, Clock, Plus } from "lucide-react";

const threads = [
  { cat: "Beslenme", title: "Bulantı için ne işe yaradı?", author: "ZeynepK", time: "2 saat önce", replies: 28, votes: 142 },
  { cat: "Doğum", title: "Normal doğum deneyimimi paylaşıyorum 💛", author: "AyseninGunlugu", time: "5 saat önce", replies: 64, votes: 312 },
  { cat: "1. Trimester", title: "8. haftadayım, çok yorgunum normal mi?", author: "yeniAnneAdayi", time: "1 gün önce", replies: 19, votes: 56 },
  { cat: "Alışveriş", title: "Bebek arabası önerileri", author: "MeryemD", time: "1 gün önce", replies: 41, votes: 89 },
  { cat: "Ruh Sağlığı", title: "Doğum öncesi kaygıyla nasıl baş ediyorsunuz?", author: "elifsu", time: "2 gün önce", replies: 33, votes: 124 },
];

const categories = ["Tümü", "1. Trimester", "2. Trimester", "3. Trimester", "Beslenme", "Doğum", "Ruh Sağlığı", "Alışveriş"];

export default function Forum() {
  return (
    <div className="p-4 md:p-8 max-w-[1100px] mx-auto space-y-6">
      <div className="flex items-end justify-between flex-wrap gap-3">
        <div>
          <h1 className="font-serif text-3xl">Forum</h1>
          <p className="text-muted-foreground mt-1">Topluluğun deneyimleri ve soruları.</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" /> Yeni Başlık
        </Button>
      </div>

      <div className="flex gap-2 overflow-x-auto pb-2">
        {categories.map((c, i) => (
          <Badge
            key={c}
            variant={i === 0 ? "default" : "outline"}
            className={`cursor-pointer whitespace-nowrap py-1.5 px-3 ${
              i === 0 ? "bg-primary text-primary-foreground hover:bg-primary-hover" : "border-border/60"
            }`}
          >
            {c}
          </Badge>
        ))}
      </div>

      <div className="space-y-3">
        {threads.map((t, i) => (
          <Card key={i} className="shadow-card border-border/60 hover:border-primary/40 transition cursor-pointer">
            <CardContent className="p-5 flex gap-4">
              <div className="flex flex-col items-center justify-start pt-1">
                <button className="grid place-items-center h-8 w-8 rounded-md hover:bg-muted transition">
                  <ArrowUp className="h-4 w-4 text-muted-foreground" />
                </button>
                <span className="font-serif text-sm">{t.votes}</span>
              </div>
              <div className="flex-1 min-w-0">
                <Badge variant="secondary" className="bg-accent-pink/15 text-foreground hover:bg-accent-pink/25 mb-2">
                  {t.cat}
                </Badge>
                <h3 className="font-serif text-lg leading-snug">{t.title}</h3>
                <div className="flex items-center gap-3 text-xs text-muted-foreground mt-2">
                  <span className="flex items-center gap-1">
                    <div className="h-5 w-5 rounded-full bg-gradient-primary" />
                    {t.author}
                  </span>
                  <span className="flex items-center gap-1">
                    <Clock className="h-3 w-3" /> {t.time}
                  </span>
                  <span className="flex items-center gap-1">
                    <MessageCircle className="h-3 w-3" /> {t.replies} yanıt
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
