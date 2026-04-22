import React, { useState } from "react";
import { Text } from "react-native";
import { requestApi } from "../../shared/api/client";
import { AppButton } from "../../shared/ui/AppButton";
import { AppScaffold } from "../../shared/ui/AppScaffold";

interface CountersScreenProps {
  token: string;
}

interface AnalyzeResponse {
  message: string;
}

export function CountersScreen({ token }: CountersScreenProps) {
  const [message, setMessage] = useState("-");

  async function handleAnalyze() {
    await requestApi(
      { token, method: "POST", body: JSON.stringify({ start_time: new Date(Date.now() - 60000).toISOString(), end_time: new Date().toISOString() }) },
      "/counters/contraction-event"
    );
    const result = await requestApi<AnalyzeResponse>({ token, method: "POST" }, "/counters/contraction-session/analyze");
    setMessage(result.message);
  }

  return (
    <AppScaffold>
      <AppButton
        title="Tekme Oturumu Kaydet"
        onPress={() =>
          requestApi(
            {
              token,
              method: "POST",
              body: JSON.stringify({
                start_time: new Date(Date.now() - 3600000).toISOString(),
                end_time: new Date().toISOString(),
                total_count: 20,
              }),
            },
            "/counters/kick-session"
          )
        }
      />
      <AppButton title="Kasılma Analizi" onPress={handleAnalyze} />
      <Text>{message}</Text>
    </AppScaffold>
  );
}
