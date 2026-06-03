import { useCallback, useEffect, useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { Sparkles, Send, Loader2, Plus, Trash2 } from "lucide-react";
import { apiClient } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";
import { cn } from "@/lib/utils";

type Msg = { id?: number; from: "baby" | "me"; text: string };
type Session = { id: number; title: string; created_at?: string; updated_at?: string };

export default function BabyChat() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<number | null>(null);
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [isLoadingSessions, setIsLoadingSessions] = useState(true);
  const [isLoadingMessages, setIsLoadingMessages] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const messagesScrollRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();

  const scrollMessagesToBottom = useCallback(() => {
    const el = messagesScrollRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, []);

  const loadMessages = useCallback(async (sessionId: number) => {
    setIsLoadingMessages(true);
    try {
      const data = await apiClient.getSessionMessages(sessionId);
      setMessages(data);
    } catch (error) {
      toast({
        title: "Mesajlar yüklenemedi",
        description: error instanceof Error ? error.message : "Bir hata oluştu.",
        variant: "destructive",
      });
      setMessages([]);
    } finally {
      setIsLoadingMessages(false);
    }
  }, [toast]);

  useEffect(() => {
    const init = async () => {
      try {
        let list = await apiClient.getChatSessions();
        if (list.length === 0) {
          const created = await apiClient.createChatSession();
          list = [created];
        }
        setSessions(list);
        const firstId = list[0]?.id ?? null;
        setActiveSessionId(firstId);
      } catch (error) {
        toast({
          title: "Sohbetler yüklenemedi",
          description: error instanceof Error ? error.message : "Bir hata oluştu.",
          variant: "destructive",
        });
      } finally {
        setIsLoadingSessions(false);
      }
    };
    init();
  }, [toast]);

  useEffect(() => {
    if (activeSessionId == null) return;
    loadMessages(activeSessionId);
  }, [activeSessionId, loadMessages]);

  useEffect(() => {
    requestAnimationFrame(() => scrollMessagesToBottom());
  }, [messages, isSending, isLoadingMessages, scrollMessagesToBottom]);

  const handleNewChat = async () => {
    try {
      const session = await apiClient.createChatSession();
      setSessions((s) => [session, ...s]);
      setActiveSessionId(session.id);
      const msgs = await apiClient.getSessionMessages(session.id);
      setMessages(msgs);
    } catch (error) {
      toast({
        title: "Yeni sohbet oluşturulamadı",
        description: error instanceof Error ? error.message : "Bir hata oluştu.",
        variant: "destructive",
      });
    }
  };

  const handleSelectSession = (sessionId: number) => {
    if (sessionId === activeSessionId) return;
    setActiveSessionId(sessionId);
  };

  const handleDeleteSession = async (sessionId: number, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await apiClient.deleteChatSession(sessionId);
      const remaining = sessions.filter((s) => s.id !== sessionId);
      setSessions(remaining);

      if (activeSessionId !== sessionId) return;

      if (remaining.length > 0) {
        setActiveSessionId(remaining[0].id);
        return;
      }

      const created = await apiClient.createChatSession();
      setSessions([created]);
      setActiveSessionId(created.id);
      const msgs = await apiClient.getSessionMessages(created.id);
      setMessages(msgs);
    } catch (error) {
      toast({
        title: "Sohbet silinemedi",
        description: error instanceof Error ? error.message : "Bir hata oluştu.",
        variant: "destructive",
      });
    }
  };

  const send = async (e: React.FormEvent) => {
    e.preventDefault();
    const text = input.trim();
    if (!text || isSending || activeSessionId == null) return;

    setInput("");
    setIsSending(true);

    const optimistic: Msg = { from: "me", text };
    setMessages((m) => [...m, optimistic]);

    try {
      const result = await apiClient.sendAssistantMessage(activeSessionId, text);
      setMessages((m) => {
        const withoutOptimistic = m.slice(0, -1);
        return [...withoutOptimistic, result.user_message, result.assistant_message];
      });
      setSessions((s) =>
        s.map((item) =>
          item.id === result.session.id ? { ...item, title: result.session.title } : item
        )
      );
    } catch (error) {
      setMessages((m) => m.slice(0, -1));
      toast({
        title: "Mesaj gönderilemedi",
        description: error instanceof Error ? error.message : "Bir hata oluştu.",
        variant: "destructive",
      });
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100dvh-4rem)] max-h-[calc(100dvh-4rem)] overflow-hidden p-4 md:p-6 max-w-[1400px] mx-auto w-full">
      <div className="flex items-center gap-3 shrink-0 mb-4">
        <div className="h-12 w-12 rounded-full bg-secondary text-secondary-foreground grid place-items-center shadow-glow">
          <Sparkles className="h-5 w-5" />
        </div>
        <div>
          <h1 className="font-serif text-2xl md:text-3xl">Gebelik Asistanı</h1>
          <p className="text-sm md:text-base text-muted-foreground">
            Gebelik sürecin, bebeğinin gelişimi ve sağlık kayıtların hakkında sor
          </p>
        </div>
      </div>

      <div className="flex flex-col lg:flex-row gap-4 flex-1 min-h-0 overflow-hidden">
        {/* Sol: Sohbet geçmişi — sabit yükseklik, liste kaydırılır */}
        <Card className="shadow-card border-border/60 flex flex-col w-full lg:w-72 xl:w-80 shrink-0 h-[220px] lg:h-full min-h-0 overflow-hidden">
          <CardHeader className="py-3 px-4 border-b border-border shrink-0 space-y-0">
            <CardTitle className="font-serif text-base md:text-lg">Sohbet Geçmişi</CardTitle>
          </CardHeader>
          <div className="flex flex-col flex-1 min-h-0 overflow-hidden p-3 gap-3">
            <Button
              type="button"
              variant="outline"
              className="w-full justify-start gap-2 shrink-0 border-secondary/50 hover:bg-secondary/10"
              onClick={handleNewChat}
              disabled={isLoadingSessions}
            >
              <Plus className="h-4 w-4" />
              Yeni Sohbet
            </Button>

            <div className="flex-1 min-h-0 overflow-y-auto overscroll-contain space-y-1 -mx-1 px-1">
              {isLoadingSessions ? (
                <div className="flex items-center justify-center py-8 text-muted-foreground gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span className="text-sm">Yükleniyor...</span>
                </div>
              ) : sessions.length === 0 ? (
                <p className="text-sm text-muted-foreground text-center py-6">
                  Henüz sohbet yok.
                </p>
              ) : (
                sessions.map((s) => (
                  <div
                    key={s.id}
                    role="button"
                    tabIndex={0}
                    onClick={() => handleSelectSession(s.id)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter" || e.key === " ") {
                        e.preventDefault();
                        handleSelectSession(s.id);
                      }
                    }}
                    className={cn(
                      "w-full flex items-center gap-2 rounded-lg px-3 py-2.5 text-left text-sm transition-colors cursor-pointer",
                      activeSessionId === s.id
                        ? "bg-secondary/30 text-foreground"
                        : "hover:bg-muted/60 text-muted-foreground hover:text-foreground"
                    )}
                  >
                    <span className="flex-1 truncate font-medium">{s.title}</span>
                    <button
                      type="button"
                      aria-label="Sohbeti sil"
                      className="shrink-0 p-1 rounded-md opacity-60 hover:opacity-100 hover:bg-destructive/10 hover:text-destructive transition-opacity"
                      onClick={(e) => handleDeleteSession(s.id, e)}
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                ))
              )}
            </div>
          </div>
        </Card>

        {/* Sağ: Mesajlar kaydırılır, giriş kutusu altta sabit */}
        <Card className="shadow-card border-border/60 flex flex-col flex-1 min-h-0 h-full overflow-hidden">
          <div
            ref={messagesScrollRef}
            className="flex-1 min-h-0 overflow-y-auto overscroll-contain p-4 md:p-6 space-y-4"
          >
            {isLoadingMessages ? (
              <div className="flex items-center justify-center min-h-[120px] text-muted-foreground gap-2">
                <Loader2 className="h-5 w-5 animate-spin" />
                <span className="text-sm">Sohbet yükleniyor...</span>
              </div>
            ) : messages.length === 0 ? (
              <p className="text-sm md:text-base text-muted-foreground text-center py-16">
                Henüz mesaj yok. Aşağıdan bir soru yazabilirsin.
              </p>
            ) : (
              messages.map((m, i) => (
                <div
                  key={m.id ?? i}
                  className={`flex ${m.from === "me" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-[min(85%,42rem)] rounded-2xl px-4 py-3 text-sm md:text-base leading-relaxed whitespace-pre-wrap ${
                      m.from === "me"
                        ? "bg-primary text-primary-foreground rounded-br-sm"
                        : "bg-secondary/40 text-foreground rounded-bl-sm"
                    }`}
                  >
                    {m.text}
                  </div>
                </div>
              ))
            )}
            {isSending && (
              <div className="flex justify-start">
                <div className="rounded-2xl px-4 py-3 text-sm md:text-base bg-secondary/40 text-muted-foreground rounded-bl-sm flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Yanıt hazırlanıyor...
                </div>
              </div>
            )}
          </div>

          <form
            onSubmit={send}
            className="shrink-0 p-4 md:p-5 border-t border-border flex gap-2 md:gap-3 bg-card"
          >
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Gebelik hakkında bir soru yaz..."
              className="bg-muted/40 h-11 md:h-12 text-base flex-1"
              disabled={isLoadingMessages || isSending || activeSessionId == null}
            />
            <Button
              type="submit"
              size="lg"
              className="bg-secondary text-secondary-foreground hover:brightness-105 h-11 md:h-12 px-4 md:px-6 shrink-0"
              disabled={isLoadingMessages || isSending || !input.trim() || activeSessionId == null}
            >
              {isSending ? (
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                <Send className="h-5 w-5" />
              )}
            </Button>
          </form>
        </Card>
      </div>

      <p className="text-xs text-muted-foreground text-center shrink-0 pt-2">
        Gebelik Asistanı tıbbi tavsiye vermez. Acil durumlarda doktorunuza veya acil servise başvurun.
      </p>
    </div>
  );
}
