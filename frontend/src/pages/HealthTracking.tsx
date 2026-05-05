import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { FileDown } from "lucide-react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";
import { toast } from "sonner";

const tansiyon = [
  { d: "01.05", sis: 115, dia: 75 },
  { d: "05.05", sis: 118, dia: 76 },
  { d: "10.05", sis: 116, dia: 74 },
  { d: "15.05", sis: 120, dia: 78 },
  { d: "20.05", sis: 117, dia: 75 },
  { d: "25.05", sis: 119, dia: 77 },
];

export default function HealthTracking() {
  return (
    <div className="p-4 md:p-8 space-y-6 max-w-[1400px] mx-auto">
      <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-3">
        <div>
          <h1 className="font-serif text-3xl">Sağlık Takibi</h1>
          <p className="text-muted-foreground mt-1">
            Ölçümlerini kaydet, gelişimini grafik üzerinden izle.
          </p>
        </div>
        <Button onClick={() => toast.success("PDF raporu oluşturuldu (mock)")}>
          <FileDown className="h-4 w-4 mr-2" />
          PDF Rapor Oluştur
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Veri Giriş Formu */}
        <Card className="shadow-card border-border/60">
          <CardHeader>
            <CardTitle className="font-serif text-xl">Yeni Ölçüm</CardTitle>
            <p className="text-sm text-muted-foreground">Bugünkü değerlerini gir.</p>
          </CardHeader>
          <CardContent>
            <form
              className="space-y-4"
              onSubmit={(e) => {
                e.preventDefault();
                toast.success("Ölçüm kaydedildi");
              }}
            >
              <div className="grid grid-cols-2 gap-4">
                <Field id="kilo" label="Kilo (kg)" placeholder="69.4" />
                <Field id="su" label="Su (litre)" placeholder="2.0" />
                <Field id="sis" label="Sistolik" placeholder="118" />
                <Field id="dia" label="Diastolik" placeholder="76" />
                <Field id="seker" label="Kan şekeri (mg/dL)" placeholder="92" />
                <Field id="nabiz" label="Nabız" placeholder="78" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="not">Notlar</Label>
                <Input id="not" placeholder="Bugün hafif baş dönmesi vardı..." />
              </div>
              <Button type="submit" className="w-full">Kaydet</Button>
            </form>
          </CardContent>
        </Card>

        {/* Grafik */}
        <Card className="shadow-card border-border/60">
          <CardHeader>
            <CardTitle className="font-serif text-xl">Trend</CardTitle>
            <Tabs defaultValue="tansiyon" className="mt-2">
              <TabsList>
                <TabsTrigger value="tansiyon">Tansiyon</TabsTrigger>
                <TabsTrigger value="kilo">Kilo</TabsTrigger>
                <TabsTrigger value="seker">Şeker</TabsTrigger>
              </TabsList>
              <TabsContent value="tansiyon" className="mt-4">
                <div className="h-[280px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={tansiyon} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                      <XAxis dataKey="d" stroke="hsl(var(--muted-foreground))" fontSize={12} />
                      <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} />
                      <Tooltip
                        contentStyle={{
                          background: "hsl(var(--card))",
                          border: "1px solid hsl(var(--border))",
                          borderRadius: 12,
                        }}
                      />
                      <Line type="monotone" dataKey="sis" stroke="hsl(var(--accent))" strokeWidth={2.5} dot={{ r: 3 }} />
                      <Line type="monotone" dataKey="dia" stroke="hsl(var(--accent-pink))" strokeWidth={2.5} dot={{ r: 3 }} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </TabsContent>
              <TabsContent value="kilo" className="mt-4">
                <EmptyChart text="Kilo grafiği burada gösterilecek" />
              </TabsContent>
              <TabsContent value="seker" className="mt-4">
                <EmptyChart text="Kan şekeri grafiği burada gösterilecek" />
              </TabsContent>
            </Tabs>
          </CardHeader>
        </Card>
      </div>
    </div>
  );
}

function Field({ id, label, placeholder }: { id: string; label: string; placeholder: string }) {
  return (
    <div className="space-y-2">
      <Label htmlFor={id}>{label}</Label>
      <Input id={id} placeholder={placeholder} />
    </div>
  );
}

function EmptyChart({ text }: { text: string }) {
  return (
    <div className="h-[280px] grid place-items-center rounded-xl bg-muted/40 text-muted-foreground text-sm">
      {text}
    </div>
  );
}
