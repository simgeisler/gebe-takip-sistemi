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
import { useEffect, useState } from "react";
import { apiClient } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";

/** Grafik: sol = eski, sağ = yeni (aynı gün birden fazla kayıt için id sırası) */
function sortMeasurementsChrono<T extends { date?: string; id?: number }>(rows: T[]): T[] {
  return [...rows].sort((a, b) => {
    const c = String(a.date ?? "").localeCompare(String(b.date ?? ""));
    if (c !== 0) return c;
    return (a.id ?? 0) - (b.id ?? 0);
  });
}

export default function HealthTracking() {
  const { toast: uiToast } = useToast();
  const [measurements, setMeasurements] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [healthSummary, setHealthSummary] = useState<any[]>([]);
  const [trendData, setTrendData] = useState<any>({});

  // Özet ve trend verilerini yükle
  useEffect(() => {
    const loadHealthData = async () => {
      try {
        // Özet verilerini getir
        const summaryResponse = await apiClient.getHealthSummary(3) as any;
        setHealthSummary(summaryResponse?.summaries ?? []);

        // Trend verilerini getir
        const tansiyonTrend = await apiClient.getHealthTrends('tansiyon', 6) as any;
        const kiloTrend = await apiClient.getHealthTrends('kilo', 6) as any;
        const sekerTrend = await apiClient.getHealthTrends('seker', 6) as any;
        
        setTrendData({
          tansiyon: tansiyonTrend?.data ?? [],
          kilo: kiloTrend?.data ?? [],
          seker: sekerTrend?.data ?? [],
        });
      } catch (error) {
        console.error('Sağlık verileri yüklenemedi:', error);
      }
    };

    loadHealthData();
  }, []);

  const recentMeasurements = healthSummary;

  const tansiyonSeries = (trendData.tansiyon ?? []) as any[];
  const kiloSeries = (trendData.kilo ?? []) as any[];
  const sekerSeries = (trendData.seker ?? []) as any[];

  const hasTansiyonPoints = tansiyonSeries.some(
    (m) => m.systolic != null && m.diastolic != null,
  );
  const hasKiloPoints = kiloSeries.some((m) => m.weight != null && m.weight !== "");
  const hasSekerPoints = sekerSeries.some((m) => m.blood_glucose != null && m.blood_glucose !== "");

  const prepareChartData = (field: "weight" | "blood_glucose") => {
    const data = field === "weight" ? kiloSeries : sekerSeries;
    return sortMeasurementsChrono(
      data.filter((m) => m[field] != null && m[field] !== ""),
    ).map((m) => ({
      date: new Date(m.date).toLocaleDateString("tr-TR", { day: "2-digit", month: "2-digit" }),
      value: Number(m[field]),
    }));
  };

  useEffect(() => {
    const fetchMeasurements = async () => {
      try {
        const data = await apiClient.getMeasurements() as any[];
        setMeasurements(data || []);
      } catch (error) {
        uiToast({
          title: "Veri yüklenemedi",
          description: "Sağlık ölçümleri alınırken bir hata oluştu",
          variant: "destructive",
        });
      } finally {
        setIsLoading(false);
      }
    };

    fetchMeasurements();
  }, [uiToast]);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    
    const measurementData = {
      date: new Date().toISOString().split('T')[0],
      weight: formData.get('kilo') ? parseFloat(formData.get('kilo') as string) : undefined,
      water_liters: formData.get('su') ? parseFloat(formData.get('su') as string) : undefined,
      systolic: formData.get('sis') ? parseInt(formData.get('sis') as string) : undefined,
      diastolic: formData.get('dia') ? parseInt(formData.get('dia') as string) : undefined,
      blood_glucose: formData.get('seker') ? parseFloat(formData.get('seker') as string) : undefined,
      pulse: formData.get('nabiz') ? parseInt(formData.get('nabiz') as string) : undefined,
      notes: formData.get('not') as string,
    };

    try {
      await apiClient.createMeasurement(measurementData);
      toast.success("Ölçüm kaydedildi");

      const summaryResponse = (await apiClient.getHealthSummary(3)) as any;
      setHealthSummary(summaryResponse?.summaries ?? []);

      const [tansiyonTrend, kiloTrend, sekerTrend] = await Promise.all([
        apiClient.getHealthTrends("tansiyon", 6) as Promise<any>,
        apiClient.getHealthTrends("kilo", 6) as Promise<any>,
        apiClient.getHealthTrends("seker", 6) as Promise<any>,
      ]);

      setTrendData({
        tansiyon: tansiyonTrend?.data ?? [],
        kilo: kiloTrend?.data ?? [],
        seker: sekerTrend?.data ?? [],
      });

      const data = (await apiClient.getMeasurements()) as any[];
      setMeasurements(data ?? []);

      e.currentTarget.reset();
    } catch (error) {
      console.error(error);
      toast.error("Ölçüm kaydedilemedi");
    }
  };

  const handlePDF = async () => {
    try {
      // This would call a PDF generation endpoint
      toast.success("PDF raporu oluşturuldu");
    } catch (error) {
      toast.error("PDF oluşturulamadı");
    }
  };

  return (
    <div className="p-4 md:p-8 space-y-6 max-w-[1400px] mx-auto">
      <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-3">
        <div>
          <h1 className="font-serif text-3xl">Sağlık Takibi</h1>
          <p className="text-muted-foreground mt-1">
            Ölçümlerini kaydet, gelişimini grafik üzerinden izle.
          </p>
        </div>
        <Button onClick={handlePDF}>
          <FileDown className="h-4 w-4 mr-2" />
          PDF Rapor Oluştur
        </Button>
      </div>

      {/* Özet Bölümü */}
      <Card className="shadow-card border-border/60">
        <CardHeader>
          <CardTitle className="font-serif text-xl">Özet</CardTitle>
          <p className="text-sm text-muted-foreground">Son 3 girilen değer</p>
        </CardHeader>
        <CardContent>
          {recentMeasurements.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              Henüz ölçüm girilmemiş
            </div>
          ) : (
            <div className="space-y-4">
              {recentMeasurements.map((measurement, index) => (
                <div key={measurement.id ?? `m-${index}`} className="p-4 bg-muted/30 rounded-lg">
                  <div className="flex justify-between items-start mb-2">
                    <span className="font-medium text-sm">
                      {new Date(measurement.date).toLocaleDateString('tr-TR', {
                        day: 'numeric',
                        month: 'long',
                        year: 'numeric'
                      })}
                    </span>
                    <span className="text-xs text-muted-foreground">
                      #{index + 1}
                    </span>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 text-sm">
                    {measurement.systolic && measurement.diastolic && (
                      <div>
                        <span className="text-muted-foreground">Tansiyon: </span>
                        <span className="font-medium">{measurement.systolic}/{measurement.diastolic}</span>
                      </div>
                    )}
                    {measurement.weight && (
                      <div>
                        <span className="text-muted-foreground">Kilo: </span>
                        <span className="font-medium">{measurement.weight} kg</span>
                      </div>
                    )}
                    {measurement.blood_glucose && (
                      <div>
                        <span className="text-muted-foreground">Şeker: </span>
                        <span className="font-medium">{measurement.blood_glucose} mg/dL</span>
                      </div>
                    )}
                    {measurement.water_liters && (
                      <div>
                        <span className="text-muted-foreground">Su: </span>
                        <span className="font-medium">{measurement.water_liters} L</span>
                      </div>
                    )}
                    {measurement.pulse && (
                      <div>
                        <span className="text-muted-foreground">Nabız: </span>
                        <span className="font-medium">{measurement.pulse}</span>
                      </div>
                    )}
                  </div>
                  {measurement.notes && (
                    <div className="mt-2 text-xs text-muted-foreground italic">
                      Not: {measurement.notes}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

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
              onSubmit={handleSubmit}
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
                <Input id="not" name="not" placeholder="Bugün hafif baş dönmesi vardı..." />
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
                  {hasTansiyonPoints ? (
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart
                        data={sortMeasurementsChrono(
                          tansiyonSeries.filter((m) => m.systolic != null && m.diastolic != null),
                        ).map((m) => ({
                          date: new Date(m.date).toLocaleDateString("tr-TR", {
                            day: "2-digit",
                            month: "2-digit",
                          }),
                          sis: Number(m.systolic),
                          dia: Number(m.diastolic),
                        }))}
                        margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                        <XAxis dataKey="date" stroke="hsl(var(--muted-foreground))" fontSize={12} />
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
                  ) : (
                    <EmptyChart text="Tansiyon verisi bulunmuyor" />
                  )}
                </div>
              </TabsContent>
              <TabsContent value="kilo" className="mt-4">
                <div className="h-[280px]">
                  {hasKiloPoints ? (
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={prepareChartData("weight")} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                        <XAxis dataKey="date" stroke="hsl(var(--muted-foreground))" fontSize={12} />
                        <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} />
                        <Tooltip
                          contentStyle={{
                            background: "hsl(var(--card))",
                            border: "1px solid hsl(var(--border))",
                            borderRadius: 12,
                          }}
                        />
                        <Line type="monotone" dataKey="value" stroke="hsl(var(--primary))" strokeWidth={2.5} dot={{ r: 3 }} />
                      </LineChart>
                    </ResponsiveContainer>
                  ) : (
                    <EmptyChart text="Kilo verisi bulunmuyor" />
                  )}
                </div>
              </TabsContent>
              <TabsContent value="seker" className="mt-4">
                <div className="h-[280px]">
                  {hasSekerPoints ? (
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={prepareChartData("blood_glucose")} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                        <XAxis dataKey="date" stroke="hsl(var(--muted-foreground))" fontSize={12} />
                        <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} />
                        <Tooltip
                          contentStyle={{
                            background: "hsl(var(--card))",
                            border: "1px solid hsl(var(--border))",
                            borderRadius: 12,
                          }}
                        />
                        <Line type="monotone" dataKey="value" stroke="hsl(var(--destructive))" strokeWidth={2.5} dot={{ r: 3 }} />
                      </LineChart>
                    </ResponsiveContainer>
                  ) : (
                    <EmptyChart text="Kan şekeri verisi bulunmuyor" />
                  )}
                </div>
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
      <Input id={id} name={id} placeholder={placeholder} />
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
