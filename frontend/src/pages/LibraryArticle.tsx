import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Clock, BookOpen, Heart, Share2 } from "lucide-react";
import { apiClient } from "@/lib/api";
import { toast } from "sonner";

export default function LibraryArticle() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [article, setArticle] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isLiked, setIsLiked] = useState(false);

  // Makaleyi yükle
  useEffect(() => {
    const loadArticle = async () => {
      if (!id) return;

      try {
        const articleData = await apiClient.getLibraryArticle(parseInt(id)) as any;
        setArticle(articleData);
        setIsLiked(Boolean(articleData.liked_by_me));
      } catch (error) {
        console.error('Makale yüklenemedi:', error);
        toast.error('Makale yüklenemedi');
        navigate('/kutuphane');
      } finally {
        setIsLoading(false);
      }
    };

    loadArticle();
  }, [id, navigate]);

  const handleLike = async () => {
    if (!article) return;

    try {
      if (isLiked) {
        await apiClient.unlikeLibraryArticle(article.id);
        toast.success("Beğeni kaldırıldı");
      } else {
        await apiClient.likeLibraryArticle(article.id);
        toast.success("Beğenildi");
      }
      setIsLiked(!isLiked);
      setArticle((prev) =>
        prev
          ? {
              ...prev,
              likes_count: Math.max(0, (prev.likes_count ?? 0) + (isLiked ? -1 : 1)),
            }
          : prev
      );
    } catch (error) {
      console.error('Beğeni işlemi başarısız:', error);
      toast.error("Beğeni işlemi başarısız");
    }
  };

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: article?.title,
          text: article?.description,
          url: window.location.href,
        });
      } catch (error) {
        console.error('Paylaşım başarısız:', error);
      }
    } else {
      // Fallback: kopyala
      navigator.clipboard.writeText(window.location.href);
      toast.success("Link kopyalandı");
    }
  };

  if (isLoading) {
    return (
      <div className="p-4 md:p-8 space-y-6 max-w-[1400px] mx-auto">
        <div className="text-center py-12">
          <p className="text-muted-foreground">Yükleniyor...</p>
        </div>
      </div>
    );
  }

  if (!article) {
    return (
      <div className="p-4 md:p-8 space-y-6 max-w-[1400px] mx-auto">
        <div className="text-center py-12">
          <p className="text-muted-foreground">Makale bulunamadı.</p>
          <Button onClick={() => navigate('/kutuphane')} className="mt-4">
            Kütüphane'ye Dön
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 md:p-8 space-y-6 max-w-[1400px] mx-auto">
      <Button
        variant="ghost"
        onClick={() => navigate('/kutuphane')}
        className="mb-4"
      >
        <ArrowLeft className="h-4 w-4 mr-2" />
        Kütüphane'ye Dön
      </Button>

      {/* Makale Başlık */}
      <Card className="shadow-card border-border/60">
        <CardContent className="p-6 space-y-4">
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1">
              <Badge variant="secondary" className="bg-accent/15 text-foreground hover:bg-accent/20 mb-3">
                {article.category}
              </Badge>
              <h1 className="font-serif text-2xl md:text-3xl leading-tight mb-4">
                {article.title}
              </h1>
              <p className="text-muted-foreground text-lg mb-4">
                {article.description}
              </p>
            </div>
          </div>

          <div className="flex items-center justify-between pt-4 border-t">
            <div className="flex items-center gap-4 text-sm text-muted-foreground">
              <span className="flex items-center gap-1">
                <Clock className="h-4 w-4" />
                {article.read_minutes} dk okuma
              </span>
              <span className="flex items-center gap-1">
                <BookOpen className="h-4 w-4" />
                {article.likes_count || 0} beğeni
              </span>
            </div>

            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={handleLike}
                className={isLiked ? "text-red-500 border-red-500" : ""}
              >
                <Heart className={`h-4 w-4 mr-2 ${isLiked ? 'fill-current' : ''}`} />
                {isLiked ? 'Beğenildi' : 'Beğen'}
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={handleShare}
              >
                <Share2 className="h-4 w-4 mr-2" />
                Paylaş
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Makale Görseli */}
      {article.image_url && (
        <Card className="shadow-card border-border/60 overflow-hidden">
          <div className="h-64 md:h-96">
            <img
              src={article.image_url}
              alt={article.title}
              className="w-full h-full object-cover"
              onError={(e) => {
                e.currentTarget.src = `https://picsum.photos/seed/${article.title}/800/400.jpg`;
              }}
            />
          </div>
        </Card>
      )}

      {/* Makale İçeriği */}
      <Card className="shadow-card border-border/60">
        <CardContent className="p-6">
          <div className="prose prose-sm md:prose-base max-w-none whitespace-pre-wrap text-foreground">
            {article.body || ""}
          </div>
        </CardContent>
      </Card>

      {/* İlgili içerik */}
      <div className="space-y-4">
        <h3 className="font-serif text-lg">Daha fazlası</h3>
        <p className="text-sm text-muted-foreground">
          Diğer rehber yazılar için kütüphane listesine dönebilirsin.
        </p>
      </div>
    </div>
  );
}
