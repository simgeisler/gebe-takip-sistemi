import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Baby } from "lucide-react";
import { apiClient } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";

export default function Login() {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [email, setEmail] = useState("");
  const [pw, setPw] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  return (
    <div className="min-h-screen grid lg:grid-cols-2 bg-background">
      {/* Hero side */}
      <div className="hidden lg:flex relative bg-gradient-soft p-12 flex-col justify-between overflow-hidden">
        <div className="absolute -top-20 -right-20 h-72 w-72 rounded-full bg-secondary/30 blur-3xl" />
        <div className="absolute bottom-10 -left-20 h-80 w-80 rounded-full bg-accent/20 blur-3xl" />
        <div className="relative flex items-center gap-2 text-foreground">
          <div className="h-10 w-10 grid place-items-center rounded-full bg-primary text-primary-foreground">
            <Baby className="h-5 w-5" />
          </div>
          <span className="font-serif text-xl">Bebeğim- Gebelik Takip</span>
        </div>
        <div className="relative">
          <h2 className="font-serif text-4xl leading-tight">
            Yolculuğun her anı, <br /> kalbinde ve burada.
          </h2>
          <p className="mt-4 text-muted-foreground max-w-md">
            Hamileliğini güvenle takip et. Sağlık verilerin, randevuların ve bebeğinle bağın hep elinin altında.
          </p>
        </div>
        <p className="relative text-xs text-muted-foreground">© 2026 Bebeğim- Gebelik Takip · Sevgiyle tasarlandı</p>
      </div>

      {/* Form side */}
      <div className="flex items-center justify-center p-6 md:p-12">
        <Card className="w-full max-w-md shadow-card border-border/60">
          <CardContent className="p-8 space-y-6">
            <div className="text-center space-y-1">
              <h1 className="font-serif text-3xl">Hoş geldin</h1>
              <p className="text-sm text-muted-foreground">Hesabına giriş yap.</p>
            </div>
            <form
              className="space-y-4"
              onSubmit={async (e) => {
                e.preventDefault();
                setIsLoading(true);
                try {
                  const response = await apiClient.login(email, pw) as { access_token: string; user_name?: string };
                  localStorage.setItem('access_token', response.access_token);
                  
                  // Backend'den user_name gelmezse email'den oluştur
                  const userName = response.user_name || email.split('@')[0];
                  localStorage.setItem('user_name', userName);
                  
                  toast({
                    title: "Giriş başarılı",
                    description: "Hoş geldiniz!",
                  });
                  navigate("/dashboard");
                } catch (error) {
                  toast({
                    title: "Giriş başarısız",
                    description: error instanceof Error ? error.message : "Bir hata oluştu",
                    variant: "destructive",
                  });
                } finally {
                  setIsLoading(false);
                }
              }}
            >
              <div className="space-y-2">
                <Label htmlFor="email">E-posta</Label>
                <Input id="email" type="email" placeholder="senin@email.com" value={email} onChange={(e) => setEmail(e.target.value)} />
              </div>
              <div className="space-y-2">
                <Label htmlFor="pw">Şifre</Label>
                <Input id="pw" type="password" placeholder="••••••••" value={pw} onChange={(e) => setPw(e.target.value)} />
              </div>
              <div className="text-right">
                <button type="button" className="text-xs text-primary hover:underline">
                  Şifremi unuttum
                </button>
              </div>
              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? "Giriş yapılıyor..." : "Giriş Yap"}
              </Button>
            </form>
            <p className="text-center text-sm text-muted-foreground">
              Hesabın yok mu?{" "}
              <Link to="/kayit" className="text-primary hover:underline font-medium">
                Kayıt ol
              </Link>
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
