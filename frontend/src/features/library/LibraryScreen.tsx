import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Text, View } from "react-native";
import { requestApi } from "../../shared/api/client";
import { AppButton } from "../../shared/ui/AppButton";
import { AppScaffold } from "../../shared/ui/AppScaffold";
import { AppTextInput } from "../../shared/ui/AppTextInput";

interface LibraryScreenProps {
  token: string;
}

interface LibraryItem {
  id: number;
  category: string;
  title: string;
  content: string;
}

export function LibraryScreen({ token }: LibraryScreenProps) {
  const [query, setQuery] = useState("");
  const [search, setSearch] = useState("");
  const { data, refetch } = useQuery({
    queryKey: ["library", token, search],
    queryFn: () => requestApi<LibraryItem[]>({ token, method: "GET" }, `/library/search?q=${encodeURIComponent(search)}`),
  });

  return (
    <AppScaffold isScrollable>
      <AppTextInput value={query} onChangeText={setQuery} placeholder="Arama" />
      <AppButton
        title="Ara"
        onPress={async () => {
          setSearch(query);
          await refetch();
        }}
      />
      {(data ?? []).map((item) => (
        <View key={item.id}>
          <Text>{item.category}</Text>
          <Text>{item.title}</Text>
          <Text>{item.content}</Text>
        </View>
      ))}
    </AppScaffold>
  );
}
