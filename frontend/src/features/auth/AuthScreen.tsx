import React, { useState } from "react";
import { Alert, StyleSheet, Text } from "react-native";
import { FirebaseError } from "firebase/app";
import { createUserWithEmailAndPassword, signInWithEmailAndPassword } from "firebase/auth";
import { AppButton } from "../../shared/ui/AppButton";
import { AppScaffold } from "../../shared/ui/AppScaffold";
import { AppTextInput } from "../../shared/ui/AppTextInput";
import { firebaseAuth, isFirebaseConfigured } from "../../shared/firebase/firebase";
import { colors } from "../../theme/tokens";

export function AuthScreen() {
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [pressCount, setPressCount] = useState(0);

  function getAuthErrorMessage(error: unknown): string {
    if (error instanceof FirebaseError) {
      const code = error.code;
      if (code === "auth/operation-not-allowed") return "Firebase'de Email/Password girisi kapali. Firebase Console > Authentication > Sign-in method altindan etkinlestirin.";
      if (code === "auth/unauthorized-domain") return "Bu domain yetkisiz. Firebase Console > Authentication > Settings > Authorized domains listesine localhost ekleyin.";
      if (code === "auth/invalid-email") return "E-posta formati gecersiz.";
      if (code === "auth/email-already-in-use") return "Bu e-posta zaten kayitli.";
      if (code === "auth/weak-password") return "Sifre en az 6 karakter olmali.";
      if (code === "auth/user-not-found" || code === "auth/wrong-password" || code === "auth/invalid-credential") return "E-posta veya sifre hatali.";
      if (code === "auth/too-many-requests") return "Cok fazla deneme yapildi. Lutfen biraz bekleyip tekrar deneyin.";
      if (code === "auth/network-request-failed") return "Ag baglantisi hatasi. Internet baglantinizi kontrol edin.";
      return `Firebase hatasi: ${code}`;
    }
    return String(error);
  }

  async function handleSubmit() {
    setPressCount((value) => value + 1);
    if (isSubmitting) return;
    setErrorMessage("");

    if (!isFirebaseConfigured) {
      Alert.alert("Firebase Ayari Eksik", "src/shared/firebase/firebase.ts dosyasindaki FILL_ME alanlarini doldurun.");
      return;
    }

    if (!email.trim() || !password.trim()) {
      Alert.alert("Eksik Bilgi", "Lutfen e-posta ve sifre alanlarini doldurun.");
      return;
    }

    try {
      setIsSubmitting(true);
      const normalizedEmail = email.trim().toLowerCase();
      if (isRegister) await createUserWithEmailAndPassword(firebaseAuth, normalizedEmail, password);
      else await signInWithEmailAndPassword(firebaseAuth, normalizedEmail, password);
    } catch (error) {
      const message = getAuthErrorMessage(error);
      setErrorMessage(message);
      Alert.alert("Auth Hatasi", message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <AppScaffold>
      <Text style={styles.title}>{isRegister ? "Uye Ol" : "Giris Yap"}</Text>
      <Text style={styles.debugText}>Buton tiklama sayisi: {pressCount}</Text>
      {!isFirebaseConfigured && (
        <Text style={styles.warningText}>
          Firebase ayari eksik. Kayit/giris icin once `src/shared/firebase/firebase.ts` icindeki FILL_ME alanlarini doldurun.
        </Text>
      )}
      <AppTextInput autoCapitalize="none" placeholder="E-posta" value={email} onChangeText={setEmail} />
      <AppTextInput placeholder="Sifre" secureTextEntry value={password} onChangeText={setPassword} />
      {errorMessage ? <Text style={styles.errorText}>{errorMessage}</Text> : null}
      <AppButton
        title={isSubmitting ? "Isleniyor..." : isRegister ? "Uye Ol" : "Giris Yap"}
        onPress={handleSubmit}
        disabled={isSubmitting}
      />
      <AppButton
        secondary
        title={isRegister ? "Hesabin var mi? Giris yap" : "Uye degil misin? Uye ol"}
        onPress={() => setIsRegister((value) => !value)}
      />
    </AppScaffold>
  );
}

const styles = StyleSheet.create({
  title: { fontSize: 28, fontWeight: "800", color: colors.primary },
  debugText: { color: colors.textSecondary, fontSize: 12 },
  warningText: { color: "#B45309", backgroundColor: "#FEF3C7", borderRadius: 10, padding: 10 },
  errorText: { color: "#991B1B", backgroundColor: "#FEE2E2", borderRadius: 10, padding: 10 },
});
