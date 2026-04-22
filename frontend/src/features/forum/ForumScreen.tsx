import React from "react";
import { useQuery } from "@tanstack/react-query";
import { Text, View } from "react-native";
import { requestApi } from "../../shared/api/client";
import { AppButton } from "../../shared/ui/AppButton";
import { AppScaffold } from "../../shared/ui/AppScaffold";

interface ForumScreenProps {
  token: string;
}

interface Category {
  id: number;
  name: string;
}

interface ThreadItem {
  id: number;
  title: string;
  body: string;
}

export function ForumScreen({ token }: ForumScreenProps) {
  const categoriesQuery = useQuery({
    queryKey: ["forum-categories", token],
    queryFn: () => requestApi<Category[]>({ token, method: "GET" }, "/forum/categories"),
  });
  const threadsQuery = useQuery({
    queryKey: ["forum-threads", token],
    queryFn: () => requestApi<ThreadItem[]>({ token, method: "GET" }, "/forum/threads"),
  });

  async function createSampleThread() {
    const firstCategory = categoriesQuery.data?.[0];
    if (!firstCategory) return;
    await requestApi(
      { token, method: "POST", body: JSON.stringify({ category_id: firstCategory.id, title: "Merhaba", body: "Ilk gonderi" }) },
      "/forum/threads"
    );
    await threadsQuery.refetch();
  }

  return (
    <AppScaffold isScrollable>
      <AppButton title="Ornek Thread Ac" onPress={createSampleThread} />
      {(categoriesQuery.data ?? []).map((item) => (
        <Text key={item.id}>{item.name}</Text>
      ))}
      {(threadsQuery.data ?? []).map((item) => (
        <View key={item.id}>
          <Text>{item.title}</Text>
          <Text>{item.body}</Text>
        </View>
      ))}
    </AppScaffold>
  );
}
