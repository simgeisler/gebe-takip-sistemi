import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { MessageCircle, Clock, Plus, Heart } from "lucide-react";
import { apiClient } from "@/lib/api";
import { toast } from "sonner";

const questionCategories = [
  "1. Trimester (0-13 Hafta)",
  "2. Trimester (14-26 Hafta)",
  "3. Trimester (27-40+ Hafta)",
  "Beslenme & Takviyeler",
  "Sağlık & Şikayetler",
  "Bebek Alışverişi",
  "Doğum Hazırlığı",
  "Ruh Sağlığı",
  "İsim Önerileri",
  "Diğer",
];

/** Filtre: Tümü + uygulamada tanımlı tam kategori adları (backend ile aynı) */
const FILTER_OPTIONS: { label: string; api: string | null }[] = [
  { label: "Tümü", api: null },
  ...questionCategories.map((c) => ({ label: c, api: c })),
];

export default function Forum() {
  const navigate = useNavigate();
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [activeFilterApi, setActiveFilterApi] = useState<string | null>(null);
  const [threads, setThreads] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [formData, setFormData] = useState({
    title: "",
    category: "",
    detail: "",
  });

  useEffect(() => {
    const loadForumQuestions = async () => {
      try {
        const category = activeFilterApi ?? undefined;
        const questions = (await apiClient.getForumQuestions(category)) as any[];
        setThreads(questions);
      } catch (error) {
        console.error("Forum soruları yüklenemedi:", error);
        toast.error("Forum soruları yüklenemedi");
      } finally {
        setIsLoading(false);
      }
    };

    loadForumQuestions();
  }, [activeFilterApi]);

  const filteredThreads =
    activeFilterApi === null ? threads : threads.filter((t) => t.category === activeFilterApi);

  const handleSubmitQuestion = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!formData.category.trim()) {
      toast.error("Lütfen bir kategori seçin.");
      return;
    }

    try {
      const newQuestion = {
        title: formData.title,
        category: formData.category,
        detail: formData.detail,
      };

      await apiClient.createForumQuestion(newQuestion);
      toast.success("Soru başarıyla eklendi");

      const category = activeFilterApi ?? undefined;
      const questions = (await apiClient.getForumQuestions(category)) as any[];
      setThreads(questions);

      setIsDialogOpen(false);
      setFormData({ title: "", category: "", detail: "" });
    } catch (error) {
      console.error("Soru eklenemedi:", error);
      toast.error("Soru eklenemedi");
    }
  };

  const handleLikeQuestion = async (questionId: number, isLiked: boolean) => {
    try {
      if (isLiked) {
        await apiClient.unlikeForumQuestion(questionId);
        toast.success("Beğeni kaldırıldı");
      } else {
        await apiClient.likeForumQuestion(questionId);
        toast.success("Beğenildi");
      }

      const category = activeFilterApi ?? undefined;
      const questions = (await apiClient.getForumQuestions(category)) as any[];
      setThreads(questions);
    } catch (error) {
      console.error("Beğeni işlemi başarısız:", error);
      toast.error("Beğeni işlemi başarısız");
    }
  };

  const isQuestionLiked = (question: any) => question.likes_count > 0;

  if (isLoading) {
    return (
      <div className="p-4 md:p-8 max-w-[1400px] mx-auto">
        <p className="text-center text-muted-foreground py-16">Yükleniyor...</p>
      </div>
    );
  }

  return (
    <div className="p-4 md:p-8 space-y-6 max-w-[1400px] mx-auto pb-16">
      <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
        <div className="space-y-1 min-w-0">
          <h1 className="font-serif text-3xl md:text-4xl text-foreground tracking-tight">Forum</h1>
          <p className="text-sm md:text-base text-muted-foreground">
            Topluluğun deneyimleri ve soruları.
          </p>
        </div>

        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button className="shrink-0 rounded-full px-5 shadow-sm">
              <Plus className="h-4 w-4 mr-2" />
              Yeni Başlık
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-2xl max-h-[85vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle className="font-serif text-xl">Yeni başlık aç</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmitQuestion} className="space-y-4 pt-1">
              <div className="space-y-2">
                <Label htmlFor="title">Başlık</Label>
                <Input
                  id="title"
                  placeholder="Konu başlığı..."
                  value={formData.title}
                  onChange={(e) => setFormData((prev) => ({ ...prev, title: e.target.value }))}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="category">Kategori</Label>
                <Select
                  value={formData.category}
                  onValueChange={(value) => setFormData((prev) => ({ ...prev, category: value }))}
                >
                  <SelectTrigger id="category">
                    <SelectValue placeholder="Kategori seçin" />
                  </SelectTrigger>
                  <SelectContent>
                    {questionCategories.map((cat) => (
                      <SelectItem key={cat} value={cat}>
                        {cat}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="detail">Detay</Label>
                <Textarea
                  id="detail"
                  placeholder="Sorunu veya düşüncelerini buraya yaz..."
                  value={formData.detail}
                  onChange={(e) => setFormData((prev) => ({ ...prev, detail: e.target.value }))}
                  required
                  rows={12}
                  className="min-h-[220px] w-full resize-y text-base leading-relaxed"
                />
              </div>

              <Button type="submit" className="w-full rounded-full">
                Yayınla
              </Button>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <div className="flex flex-wrap gap-2 sm:gap-2.5">
        {FILTER_OPTIONS.map((chip) => {
          const isActive =
            chip.api === null ? activeFilterApi === null : activeFilterApi === chip.api;
          return (
            <button
              key={chip.label}
              type="button"
              title={chip.api ?? "Tüm kategoriler"}
              onClick={() => setActiveFilterApi(chip.api)}
              className={[
                "rounded-full px-3 py-1.5 text-left text-xs sm:text-sm font-medium transition-colors border max-w-full sm:max-w-[min(100%,22rem)] lg:max-w-[min(100%,26rem)]",
                isActive
                  ? "bg-primary text-primary-foreground border-primary shadow-sm"
                  : "bg-card text-foreground border-border hover:bg-muted/60",
              ].join(" ")}
            >
              <span className="line-clamp-2 sm:line-clamp-none">{chip.label}</span>
            </button>
          );
        })}
      </div>

      <div className="flex flex-col gap-3">
        {filteredThreads.map((thread) => {
          const votes = typeof thread.votes === "number" ? thread.votes : 0;
          const replies = thread.replies_count ?? thread.replies ?? 0;
          const liked = isQuestionLiked(thread);
          const initial = (thread.author || "?").trim().charAt(0).toUpperCase();

          return (
            <Card
              key={thread.id}
              className="group border-border/70 shadow-card overflow-hidden rounded-2xl bg-card"
            >
              <div className="flex flex-col sm:flex-row sm:items-stretch">
                <div className="flex sm:flex-col items-center justify-center gap-1 sm:gap-0.5 sm:py-4 px-3 py-2 sm:w-16 shrink-0 border-b sm:border-b-0 sm:border-r border-border/60 bg-muted/20">
                  <button
                    type="button"
                    title={liked ? "Beğeniyi kaldır" : "Beğen"}
                    className={[
                      "rounded-md p-1 transition-colors",
                      liked
                        ? "text-red-500"
                        : "text-muted-foreground hover:text-red-500/80",
                    ].join(" ")}
                    onClick={(e) => {
                      e.stopPropagation();
                      handleLikeQuestion(thread.id, liked);
                    }}
                  >
                    <Heart
                      className={`h-5 w-5 sm:h-5 sm:w-5 ${liked ? "fill-red-500 text-red-500" : ""}`}
                    />
                  </button>
                  <span className="text-sm font-semibold tabular-nums text-foreground min-w-[1.5rem] text-center leading-none">
                    {votes}
                  </span>
                </div>

                <button
                  type="button"
                  className="flex-1 text-left px-4 py-4 sm:py-5 min-w-0 hover:bg-muted/30 transition-colors"
                  onClick={() => navigate(`/forum/${thread.id}`)}
                >
                  <span className="inline-block rounded-md bg-secondary/35 text-secondary-foreground text-xs font-medium px-2 py-0.5 mb-2 max-w-full break-words">
                    {thread.category}
                  </span>
                  <h3 className="font-serif text-lg md:text-xl font-semibold text-foreground leading-snug pr-2">
                    {thread.title}
                  </h3>
                  <div className="flex flex-wrap items-center gap-x-3 gap-y-1 mt-3 text-xs text-muted-foreground">
                    <span className="inline-flex items-center gap-1.5">
                      <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary/15 text-primary text-[11px] font-semibold">
                        {initial}
                      </span>
                      <span className="font-medium text-foreground/90">{thread.author}</span>
                    </span>
                    <span className="inline-flex items-center gap-1">
                      <Clock className="h-3.5 w-3.5 opacity-70" />
                      {thread.time || "—"}
                    </span>
                    <span className="inline-flex items-center gap-1">
                      <MessageCircle className="h-3.5 w-3.5 opacity-70" />
                      {replies} yanıt
                    </span>
                  </div>
                </button>
              </div>
            </Card>
          );
        })}
      </div>

      {filteredThreads.length === 0 && (
        <div className="text-center py-14 rounded-2xl border border-dashed border-border bg-muted/20">
          <p className="text-muted-foreground text-sm">
            {activeFilterApi === null
              ? "Henüz başlık yok. İlk soruyu sen aç!"
              : "Bu filtrede henüz başlık yok."}
          </p>
        </div>
      )}
    </div>
  );
}
