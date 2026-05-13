import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Navigate, Route, Routes, useParams } from "react-router-dom";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import Index from "./pages/Index.tsx";
import NotFound from "./pages/NotFound.tsx";
import Login from "./pages/Login.tsx";
import SignUp from "./pages/SignUp.tsx";
import AppLayout from "./components/AppLayout.tsx";
import Dashboard from "./pages/Dashboard.tsx";
import HealthTracking from "./pages/HealthTracking.tsx";
import CalendarPage from "./pages/CalendarPage.tsx";
import Library from "./pages/Library.tsx";
import LibraryArticle from "./pages/LibraryArticle.tsx";
import Forum from "./pages/Forum.tsx";
import ForumQuestion from "./pages/ForumQuestion.tsx";
import BabyChat from "./pages/BabyChat.tsx";

const queryClient = new QueryClient();

function ForumQuestionLegacyRedirect() {
  const { id } = useParams<{ id: string }>();
  return <Navigate to={`/forum/${id ?? ""}`} replace />;
}

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/giris" element={<Login />} />
          <Route path="/kayit" element={<SignUp />} />
          <Route element={<AppLayout />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/saglik" element={<HealthTracking />} />
            <Route path="/takvim" element={<CalendarPage />} />
            <Route path="/kutuphane" element={<Library />} />
            <Route path="/kutuphane/:id" element={<LibraryArticle />} />
            <Route path="/forum" element={<Forum />} />
            <Route path="/forum/question/:id" element={<ForumQuestionLegacyRedirect />} />
            <Route path="/forum/:id" element={<ForumQuestion />} />
            <Route path="/bebegimle-konus" element={<BabyChat />} />
          </Route>
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
