import React, { useEffect, useState } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { onAuthStateChanged } from "firebase/auth";
import * as Notifications from "expo-notifications";
import { StyleSheet, Text, View } from "react-native";
import { SafeAreaProvider } from "react-native-safe-area-context";
import { requestApi } from "../shared/api/client";
import { firebaseAuth } from "../shared/firebase/firebase";
import { colors } from "../theme/tokens";
import { RootNavigator } from "./navigation/RootNavigator";

const queryClient = new QueryClient();

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState("");
  const [isProfileComplete, setIsProfileComplete] = useState(false);
  const [authDebug, setAuthDebug] = useState("auth: waiting");

  useEffect(
    () =>
      onAuthStateChanged(firebaseAuth, async (user) => {
        if (!user) {
          setAuthDebug("auth: no user");
          setIsAuthenticated(false);
          setToken("");
          setIsProfileComplete(false);
          return;
        }

        setIsAuthenticated(true);
        setAuthDebug(`auth: user ${user.uid.slice(0, 6)}...`);

        try {
          const idToken = await user.getIdToken();
          setToken(idToken);
          const me = await requestApi<{ profile_complete: boolean }>({ token: idToken, method: "GET" }, "/me");
          const profileComplete = Boolean(me.profile_complete);
          setIsProfileComplete(profileComplete);
          setAuthDebug(profileComplete ? "auth: profile complete" : "auth: onboarding required");
        } catch (error) {
          setIsProfileComplete(false);
          setAuthDebug(`auth: token/api error (${String(error)})`);
        }
      }),
    []
  );

  useEffect(() => {
    async function registerNotificationToken() {
      if (!token) return;
      const permission = await Notifications.requestPermissionsAsync();
      if (permission.status !== "granted") return;
      const pushToken = await Notifications.getExpoPushTokenAsync();
      await requestApi({ token, method: "POST", body: JSON.stringify({ token: pushToken.data }) }, "/notifications/fcm-token");
    }
    registerNotificationToken().catch(() => null);
  }, [token]);

  return (
    <QueryClientProvider client={queryClient}>
      <SafeAreaProvider>
        <RootNavigator
          token={token}
          isAuthenticated={isAuthenticated}
          isProfileComplete={isProfileComplete}
          onProfileCompleted={() => setIsProfileComplete(true)}
        />
        <View pointerEvents="none" style={styles.debugBanner}>
          <Text style={styles.debugText}>
            {authDebug} | isAuthenticated={String(isAuthenticated)} | isProfileComplete={String(isProfileComplete)}
          </Text>
        </View>
      </SafeAreaProvider>
    </QueryClientProvider>
  );
}

const styles = StyleSheet.create({
  debugBanner: {
    position: "absolute",
    left: 8,
    right: 8,
    bottom: 8,
    backgroundColor: "#111827",
    borderRadius: 8,
    paddingHorizontal: 10,
    paddingVertical: 8,
    opacity: 0.9,
  },
  debugText: { color: colors.white, fontSize: 11 },
});
