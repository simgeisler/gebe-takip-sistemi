import React, { useState } from "react";
import { Alert, Text } from "react-native";
import { requestApi } from "../../shared/api/client";
import { AppButton } from "../../shared/ui/AppButton";
import { AppScaffold } from "../../shared/ui/AppScaffold";
import { AppTextInput } from "../../shared/ui/AppTextInput";

interface OnboardingScreenProps {
  token: string;
  onCompleted: () => void;
}

export function OnboardingScreen({ token, onCompleted }: OnboardingScreenProps) {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [sat, setSat] = useState("");
  const [edd, setEdd] = useState("");
  const [startingWeight, setStartingWeight] = useState("");

  async function handleSubmit() {
    try {
      await requestApi(
        {
          token,
          method: "POST",
          body: JSON.stringify({
            full_name: fullName,
            email,
            last_menstrual_period: sat || null,
            expected_due_date: edd || null,
            starting_weight: Number(startingWeight),
          }),
        },
        "/me/profile"
      );
      onCompleted();
    } catch (error) {
      Alert.alert("Onboarding Hatasi", String(error));
    }
  }

  return (
    <AppScaffold isScrollable>
      <Text>Ilk Kurulum</Text>
      <AppTextInput placeholder="Ad Soyad" value={fullName} onChangeText={setFullName} />
      <AppTextInput autoCapitalize="none" placeholder="E-posta" value={email} onChangeText={setEmail} />
      <AppTextInput placeholder="SAT (YYYY-MM-DD)" value={sat} onChangeText={setSat} />
      <Text>veya</Text>
      <AppTextInput placeholder="EDD (YYYY-MM-DD)" value={edd} onChangeText={setEdd} />
      <AppTextInput placeholder="Baslangic Kilo (kg)" keyboardType="numeric" value={startingWeight} onChangeText={setStartingWeight} />
      <AppButton title="Kaydet ve Devam Et" onPress={handleSubmit} />
    </AppScaffold>
  );
}
