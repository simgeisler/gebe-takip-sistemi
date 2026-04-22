import React from "react";
import { useQuery } from "@tanstack/react-query";
import { Text } from "react-native";
import { requestApi } from "../../shared/api/client";
import { AppScaffold } from "../../shared/ui/AppScaffold";

interface DashboardScreenProps {
  token: string;
}

interface DashboardResponse {
  week_label: string;
  trimester: number;
  days_until_due: number;
  latest_weight: number | null;
}

export function DashboardScreen({ token }: DashboardScreenProps) {
  const { data } = useQuery({
    queryKey: ["status", token],
    queryFn: () => requestApi<DashboardResponse>({ token, method: "GET" }, "/status/current"),
  });

  return (
    <AppScaffold>
      <Text>{data?.week_label ?? "-"}</Text>
      <Text>Trimester: {data?.trimester ?? "-"}</Text>
      <Text>Doguma kalan gun: {data?.days_until_due ?? "-"}</Text>
      <Text>Son kilo: {data?.latest_weight ?? "-"}</Text>
    </AppScaffold>
  );
}
