import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { format } from "date-fns";
import { tr } from "date-fns/locale";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Calendar } from "@/components/ui/calendar";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Baby, CalendarIcon, ArrowRight, ArrowLeft } from "lucide-react";
import { cn } from "@/lib/utils";

export default function SignUp() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [data, setData] = useState({ name: "", email: "", pw: "", sat: undefined as Date | undefined, kilo: "" });

  return (
    <div className="min-h-screen grid lg:grid-cols-2 bg-background">
      <div className="hidden lg:flex relative bg-gradient-soft p-12 flex-col justify-between overflow-hidden">
        <div className="absolute -top-20 -right-20 h-72 w-72 rounded-full bg-accent-pink/30 blur-3xl" />
        <div className="absolute bottom-10 -left-20 h-80 w-80 rounded-full bg-secondary/20 blur-3xl" />
        <div className="relative flex items-center gap-2">
          <div className="h-10 w-10 grid place-items-center rounded-full bg-primary text-primary-foreground">
            <Baby className="h-5 w-5" />
          </div>
          <span className="font-serif text-xl">Bebeğim- Gebelik Takip</span>
        </div>
        <div className="relative">
          <h2 className="font-serif text-4xl leading-tight">
            Bu güzel yolculuğa <br /> birlikte başlayalım.
          </h2>
          <p className="mt-4 text-muted-foreground max-w-md">
            Birkaç bilgi ile sana özel bir gebelik takip alanı oluşturuyoruz.
          </p>
        </div>
        <p className="relative text-xs text-muted-foreground">© 2026 Bebeğim- Gebelik Takip</p>
      </div>

      <div className="flex items-center justify-center p-6 md:p-12">
        <Card className="w-full max-w-md shadow-card border-border/60">
          <CardContent className="p-8 space-y-6">
            <div className="space-y-3">
              <div className="flex justify-between text-xs text-muted-foreground">
                <span>Adım {step} / 2</span>
                <span>{step === 1 ? "Hesap" : "Bebek bilgileri"}</span>
              </div>
              <Progress value={step * 50} className="h-2" />
            </div>

            <div className="text-center space-y-1">
              <h1 className="font-serif text-3xl">
                {step === 1 ? "Hesabını oluştur" : "Sana özel ayarlayalım"}
              </h1>
              <p className="text-sm text-muted-foreground">
                {step === 1 ? "Birkaç bilgi yeterli." : "Bu bilgileri sonra değiştirebilirsin."}
              </p>
            </div>

            {step === 1 ? (
              <form
                className="space-y-4"
                onSubmit={(e) => {
                  e.preventDefault();
                  setStep(2);
                }}
              >
                <div className="space-y-2">
                  <Label htmlFor="name">Ad Soyad</Label>
                  <Input id="name" placeholder="Elif Yıldız" value={data.name} onChange={(e) => setData({ ...data, name: e.target.value })} required />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email">E-posta</Label>
                  <Input id="email" type="email" placeholder="elif@email.com" value={data.email} onChange={(e) => setData({ ...data, email: e.target.value })} required />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="pw">Şifre</Label>
                  <Input id="pw" type="password" placeholder="••••••••" value={data.pw} onChange={(e) => setData({ ...data, pw: e.target.value })} required />
                </div>
                <Button type="submit" className="w-full">
                  Devam Et <ArrowRight className="h-4 w-4 ml-1" />
                </Button>
              </form>
            ) : (
              <form
                className="space-y-4"
                onSubmit={(e) => {
                  e.preventDefault();
                  navigate("/dashboard");
                }}
              >
                <div className="space-y-2">
                  <Label>Son Adet Tarihi (SAT)</Label>
                  <Popover>
                    <PopoverTrigger asChild>
                      <Button
                        type="button"
                        variant="outline"
                        className={cn("w-full justify-start font-normal", !data.sat && "text-muted-foreground")}
                      >
                        <CalendarIcon className="h-4 w-4 mr-2" />
                        {data.sat ? format(data.sat, "PPP", { locale: tr }) : "Tarih seç"}
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0" align="start">
                      <Calendar
                        mode="single"
                        selected={data.sat}
                        onSelect={(d) => setData({ ...data, sat: d })}
                        disabled={(d) => d > new Date()}
                        initialFocus
                        className={cn("p-3 pointer-events-auto")}
                      />
                    </PopoverContent>
                  </Popover>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="kilo">Başlangıç Kilosu (kg)</Label>
                  <Input id="kilo" type="number" placeholder="62" value={data.kilo} onChange={(e) => setData({ ...data, kilo: e.target.value })} required />
                </div>

                <div className="flex gap-2 pt-2">
                  <Button type="button" variant="outline" className="flex-1" onClick={() => setStep(1)}>
                    <ArrowLeft className="h-4 w-4 mr-1" /> Geri
                  </Button>
                  <Button type="submit" className="flex-1">
                    Başla
                  </Button>
                </div>
              </form>
            )}

            <p className="text-center text-sm text-muted-foreground">
              Zaten hesabın var mı?{" "}
              <Link to="/giris" className="text-primary hover:underline font-medium">
                Giriş yap
              </Link>
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
