import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ArrowLeft, MessageCircle, Heart, Clock, User } from "lucide-react";
import { apiClient } from "@/lib/api";
import { toast } from "sonner";

export default function ForumQuestion() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [question, setQuestion] = useState<any>(null);
  const [replies, setReplies] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [replyContent, setReplyContent] = useState("");
  const [isLiked, setIsLiked] = useState(false);

  // Soru ve yanıtları yükle
  useEffect(() => {
    const loadQuestionData = async () => {
      if (!id) return;

      const qid = parseInt(id, 10);
      if (!Number.isFinite(qid) || qid < 1) {
        toast.error("Geçersiz adres");
        navigate("/forum");
        setIsLoading(false);
        return;
      }

      try {
        // Soruyu getir
        const questionData = (await apiClient.getForumQuestion(qid)) as any;
        setQuestion(questionData);

        // Yanıtları getir
        const repliesData = (await apiClient.listForumReplies(qid)) as any[];
        setReplies(repliesData);

        // Beğeni durumu (giriş yoksa API boş döner)
        const likesData = (await apiClient.listForumLikes(qid)) as any[];
        setIsLiked(likesData.length > 0);
      } catch (error) {
        console.error("Soru yüklenemedi:", error);
        toast.error("Soru yüklenemedi");
        navigate("/forum");
      } finally {
        setIsLoading(false);
      }
    };

    loadQuestionData();
  }, [id, navigate]);

  const handleLike = async () => {
    if (!question) return;

    try {
      if (isLiked) {
        await apiClient.unlikeForumQuestion(question.id);
        toast.success("Beğeni kaldırıldı");
      } else {
        await apiClient.likeForumQuestion(question.id);
        toast.success("Beğenildi");
      }
      setIsLiked(!isLiked);
    } catch (error) {
      console.error('Beğeni işlemi başarısız:', error);
      toast.error("Beğeni işlemi başarısız");
    }
  };

  const handleReply = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!replyContent.trim() || !question) return;

    try {
      await apiClient.createForumReply(question.id, { content: replyContent });
      toast.success("Yanıt eklendi");
      setReplyContent("");

      // Yanıtları yenile
      const repliesData = await apiClient.listForumReplies(question.id) as any[];
      setReplies(repliesData);
    } catch (error) {
      console.error('Yanıt eklenemedi:', error);
      toast.error("Yanıt eklenemedi");
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

  if (!question) {
    return (
      <div className="p-4 md:p-8 space-y-6 max-w-[1400px] mx-auto">
        <div className="text-center py-12">
          <p className="text-muted-foreground">Soru bulunamadı.</p>
          <Button onClick={() => navigate('/forum')} className="mt-4">
            Forum'a Dön
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 md:p-8 space-y-6 max-w-[1400px] mx-auto">
      <Button
        variant="ghost"
        onClick={() => navigate('/forum')}
        className="mb-4"
      >
        <ArrowLeft className="h-4 w-4 mr-2" />
        Forum'a Dön
      </Button>

      {/* Soru Detayı */}
      <Card className="shadow-card border-border/60">
        <CardContent className="p-6 space-y-4">
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1">
              <Badge variant="secondary" className="bg-accent/15 text-foreground hover:bg-accent/20 mb-3">
                {question.category}
              </Badge>
              <h1 className="font-serif text-2xl md:text-3xl leading-tight mb-4">
                {question.title}
              </h1>
              <div className="prose prose-sm max-w-none text-muted-foreground mb-4 whitespace-pre-wrap">
                {question.detail ?? ""}
              </div>
            </div>
          </div>

          <div className="flex items-center justify-between pt-4 border-t">
            <div className="flex items-center gap-4 text-sm text-muted-foreground">
              <span className="flex items-center gap-1">
                <User className="h-4 w-4" />
                {question.author}
              </span>
              <span className="flex items-center gap-1">
                <Clock className="h-4 w-4" />
                {question.time}
              </span>
              <span className="flex items-center gap-1">
                <MessageCircle className="h-4 w-4" />
                {replies.length} yanıt
              </span>
            </div>

            <Button
              variant="outline"
              size="sm"
              onClick={handleLike}
              className={isLiked ? "text-red-500 border-red-500" : ""}
            >
              <Heart className={`h-4 w-4 mr-2 ${isLiked ? 'fill-current' : ''}`} />
              {isLiked ? 'Beğenildi' : 'Beğen'}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Yanıt Formu */}
      <Card className="shadow-card border-border/60">
        <CardContent className="p-6">
          <h3 className="font-serif text-lg mb-4">Yanıt Ekle</h3>
          <form onSubmit={handleReply} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="reply">Yanıtınız</Label>
              <Input
                id="reply"
                placeholder="Yanıtınızı yazın..."
                value={replyContent}
                onChange={(e) => setReplyContent(e.target.value)}
                required
              />
            </div>
            <Button type="submit" disabled={!replyContent.trim()}>
              Yanıt Gönder
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Yanıtlar */}
      <div className="space-y-4">
        <h3 className="font-serif text-lg">Yanıtlar ({replies.length})</h3>
        
        {replies.length === 0 ? (
          <Card className="shadow-card border-border/60">
            <CardContent className="p-6 text-center">
              <p className="text-muted-foreground">Henüz yanıt yok.</p>
            </CardContent>
          </Card>
        ) : (
          replies.map((reply) => (
            <Card key={reply.id} className="shadow-card border-border/60">
              <CardContent className="p-6">
                <div className="flex items-start justify-between gap-4 mb-3">
                  <div className="flex items-center gap-2">
                    <div className="w-8 h-8 bg-accent rounded-full flex items-center justify-center">
                      <User className="h-4 w-4" />
                    </div>
                    <div>
                      <p className="font-medium">{reply.author}</p>
                      <p className="text-xs text-muted-foreground">{reply.time}</p>
                    </div>
                  </div>
                </div>
                <div className="prose prose-sm max-w-none text-muted-foreground">
                  {reply.content}
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
