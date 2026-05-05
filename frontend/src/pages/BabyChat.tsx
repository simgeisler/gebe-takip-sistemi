import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { Sparkles, Send } from "lucide-react";

type Msg = { from: "baby" | "me"; text: string };

export default function BabyChat() {
  const [messages, setMessages] = useState<Msg[]>([
    { from: "baby", text: "Merhaba anne 💛 Bugün nasıl hissediyorsun?" },
    { from: "me", text: "Biraz yorgunum ama mutluyum." },
    { from: "baby", text: "Dinlenmeyi unutma. Birlikteyiz, hep buradayım 🌸" },
  ]);
  const [input, setInput] = useState("");

  const send = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    const text = input.trim();
    setMessages((m) => [...m, { from: "me", text }]);
    setInput("");
    setTimeout(() => {
      setMessages((m) => [
        ...m,
        { from: "baby", text: "Seni duyuyorum anne. Yazdıkların bana iyi geldi 💛" },
      ]);
    }, 700);
  };

  return (
    <div className="p-4 md:p-8 max-w-3xl mx-auto space-y-6">
      <div className="flex items-center gap-3">
        <div className="h-12 w-12 rounded-full bg-secondary text-secondary-foreground grid place-items-center shadow-glow">
          <Sparkles className="h-5 w-5" />
        </div>
        <div>
          <h1 className="font-serif text-2xl">Bebeğimle Konuş</h1>
          <p className="text-sm text-muted-foreground">AI eşliğinde duygusal bir sohbet</p>
        </div>
      </div>

      <Card className="shadow-card border-border/60 min-h-[60vh] flex flex-col">
        <CardContent className="flex-1 p-5 space-y-3 overflow-y-auto">
          {messages.map((m, i) => (
            <div key={i} className={`flex ${m.from === "me" ? "justify-end" : "justify-start"}`}>
              <div
                className={`max-w-[75%] rounded-2xl px-4 py-2.5 text-sm ${
                  m.from === "me"
                    ? "bg-primary text-primary-foreground rounded-br-sm"
                    : "bg-secondary/40 text-foreground rounded-bl-sm"
                }`}
              >
                {m.text}
              </div>
            </div>
          ))}
        </CardContent>
        <form onSubmit={send} className="p-4 border-t border-border flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Bebeğine bir şey yaz..."
            className="bg-muted/40"
          />
          <Button type="submit" className="bg-secondary text-secondary-foreground hover:brightness-105">
            <Send className="h-4 w-4" />
          </Button>
        </form>
      </Card>
    </div>
  );
}
