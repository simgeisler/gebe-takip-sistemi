import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Text, View } from "react-native";
import { LineChart } from "react-native-chart-kit";
import { requestApi } from "../../shared/api/client";
import { AppButton } from "../../shared/ui/AppButton";
import { AppScaffold } from "../../shared/ui/AppScaffold";
import { AppTextInput } from "../../shared/ui/AppTextInput";

interface TrackingScreenProps {
  token: string;
}

interface WeightLog {
  value: number;
}

interface BloodPressureLog {
  systolic: number;
  diastolic: number;
  is_risky: boolean;
}

interface WeekData {
  week_number: number;
  comparison_object_name: string;
}

export function TrackingScreen({ token }: TrackingScreenProps) {
  const [weight, setWeight] = useState("");
  const [systolic, setSystolic] = useState("");
  const [diastolic, setDiastolic] = useState("");
  const weightQuery = useQuery({ queryKey: ["weights", token], queryFn: () => requestApi<WeightLog[]>({ token, method: "GET" }, "/logs/weight") });
  const bpQuery = useQuery({ queryKey: ["bps", token], queryFn: () => requestApi<BloodPressureLog[]>({ token, method: "GET" }, "/logs/blood-pressure") });
  const weekQuery = useQuery({ queryKey: ["week", token], queryFn: () => requestApi<WeekData>({ token, method: "GET" }, "/weekly-metadata/24") });

  async function saveWeight() {
    await requestApi({ token, method: "POST", body: JSON.stringify({ value: Number(weight) }) }, "/logs/weight");
    await weightQuery.refetch();
  }

  async function saveBloodPressure() {
    await requestApi(
      { token, method: "POST", body: JSON.stringify({ systolic: Number(systolic), diastolic: Number(diastolic) }) },
      "/logs/blood-pressure"
    );
    await bpQuery.refetch();
  }

  const chartData = (weightQuery.data ?? []).slice(0, 6).reverse().map((item) => item.value);

  return (
    <AppScaffold isScrollable>
      <Text>Hafta: {weekQuery.data?.week_number ?? "-"} / Kiyas: {weekQuery.data?.comparison_object_name ?? "-"}</Text>
      <AppTextInput placeholder="Kilo" keyboardType="numeric" value={weight} onChangeText={setWeight} />
      <AppButton title="Kilo Kaydet" onPress={saveWeight} />
      {chartData.length > 0 && (
        <LineChart
          width={330}
          height={180}
          data={{ labels: chartData.map((_, index) => String(index + 1)), datasets: [{ data: chartData }] }}
          chartConfig={{ backgroundGradientFrom: "#FFFFFF", backgroundGradientTo: "#FFFFFF", color: () => "#D63B7A" }}
        />
      )}
      <AppTextInput placeholder="Sistolik" keyboardType="numeric" value={systolic} onChangeText={setSystolic} />
      <AppTextInput placeholder="Diyastolik" keyboardType="numeric" value={diastolic} onChangeText={setDiastolic} />
      <AppButton title="Tansiyon Kaydet" onPress={saveBloodPressure} />
      {(bpQuery.data ?? []).map((item, index) => (
        <View key={index}>
          <Text style={{ color: item.is_risky ? "#EF5350" : "#2C1A2E" }}>{item.systolic}/{item.diastolic}</Text>
        </View>
      ))}
    </AppScaffold>
  );
}
