import { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Search, Clock, BookOpen } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { apiClient } from "@/lib/api";
import { toast } from "sonner";

export default function Library() {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState("");
  const [articles, setArticles] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Makaleleri yükle
  useEffect(() => {
    const loadArticles = async () => {
      try {
        const articlesData = await apiClient.getLibraryArticles(searchTerm) as any[];
        setArticles(articlesData);
      } catch (error) {
        console.error('Makaleler yüklenemedi:', error);
        toast.error('Makaleler yüklenemedi');
      } finally {
        setIsLoading(false);
      }
    };

    loadArticles();
  }, [searchTerm]);

  // Arama filtreleme fonksiyonu (backend'e delegasyon)
  const filteredArticles = articles;

  return (
    <div className="p-4 md:p-8 space-y-6 max-w-[1400px] mx-auto">
      <div>
        <h1 className="font-serif text-3xl">Kütüphane</h1>
        <p className="text-muted-foreground mt-1">Hamilelik yolculuğun için rehber yazılar.</p>
      </div>

      <div className="relative max-w-xl">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input 
          placeholder="Konu ara..." 
          className="pl-9 bg-card"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {/* Arama sonuçları */}
      {searchTerm && filteredArticles.length === 0 && (
        <div className="text-center py-12">
          <p className="text-muted-foreground">"{searchTerm}" için sonuç bulunamadı.</p>
          <p className="text-sm text-muted-foreground mt-2">Farklı anahtar kelimeler deneyin.</p>
        </div>
      )}

      {searchTerm && filteredArticles.length > 0 && (
        <div className="mb-4">
          <p className="text-sm text-muted-foreground">
            "{searchTerm}" için {filteredArticles.length} sonuç bulundu
          </p>
        </div>
      )}

      {isLoading ? (
        <div className="text-center py-12">
          <p className="text-muted-foreground">Yükleniyor...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filteredArticles.map((a) => (
            <Card
              key={a.id}
              className="group cursor-pointer shadow-card border-border/60 hover:-translate-y-1 hover:shadow-soft transition overflow-hidden"
              onClick={() => navigate(`/kutuphane/${a.id}`)}
            >
              <div className="h-32 overflow-hidden bg-gradient-soft">
                <img 
                  src={a.image_url || `https://picsum.photos/seed/${a.title}/400/250.jpg`} 
                  alt={a.title}
                  className="w-full h-full object-cover group-hover:scale-105 transition duration-300"
                  onError={(e) => {
                    e.currentTarget.src = `https://picsum.photos/seed/${a.title}/400/250.jpg`;
                  }}
                />
              </div>
              <CardContent className="p-5 space-y-2">
                <Badge variant="secondary" className="bg-accent/15 text-foreground hover:bg-accent/20">
                  {a.category}
                </Badge>
                <h3 className="font-serif text-lg leading-snug">{a.title}</h3>
                <p className="text-sm text-muted-foreground line-clamp-2">{a.description}</p>
                <div className="flex items-center gap-1 text-xs text-muted-foreground pt-2">
                  <Clock className="h-3 w-3" /> {a.read_minutes != null ? `${a.read_minutes} dk okuma` : "Okuma süresi —"}
                </div>
                <div className="flex items-center gap-1 text-xs text-muted-foreground">
                  <BookOpen className="h-3 w-3" /> {a.likes_count || 0} beğeni
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
