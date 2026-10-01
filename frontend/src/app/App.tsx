import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes } from "react-router";

import { LessonListPage } from "../features/lesson/LessonListPage.tsx";
import { LessonWorkspacePage } from "../features/lesson/LessonWorkspacePage.tsx";

const queryClient = new QueryClient();

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LessonListPage />} />
          <Route path="/lessons/:id" element={<LessonWorkspacePage />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
