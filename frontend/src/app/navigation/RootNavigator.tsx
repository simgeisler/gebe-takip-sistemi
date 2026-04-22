import React from "react";
import { Button, View } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { signOut } from "firebase/auth";
import { AuthScreen } from "../../features/auth/AuthScreen";
import { CountersScreen } from "../../features/counters/CountersScreen";
import { DashboardScreen } from "../../features/dashboard/DashboardScreen";
import { ForumScreen } from "../../features/forum/ForumScreen";
import { LibraryScreen } from "../../features/library/LibraryScreen";
import { OnboardingScreen } from "../../features/onboarding/OnboardingScreen";
import { TrackingScreen } from "../../features/tracking/TrackingScreen";
import { firebaseAuth } from "../../shared/firebase/firebase";

interface RootNavigatorProps {
  token: string;
  isAuthenticated: boolean;
  isProfileComplete: boolean;
  onProfileCompleted: () => void;
}

const stack = createNativeStackNavigator();
const tab = createBottomTabNavigator();

function MainTabs({ token }: { token: string }) {
  return (
    <tab.Navigator>
      <tab.Screen name="Dashboard">{() => <DashboardScreen token={token} />}</tab.Screen>
      <tab.Screen name="Takip">{() => <TrackingScreen token={token} />}</tab.Screen>
      <tab.Screen name="Sayaclar">{() => <CountersScreen token={token} />}</tab.Screen>
      <tab.Screen name="Forum">{() => <ForumScreen token={token} />}</tab.Screen>
      <tab.Screen name="Kutuphane">{() => <LibraryScreen token={token} />}</tab.Screen>
    </tab.Navigator>
  );
}

export function RootNavigator({ token, isAuthenticated, isProfileComplete, onProfileCompleted }: RootNavigatorProps) {
  return (
    <NavigationContainer>
      <stack.Navigator>
        {!isAuthenticated && <stack.Screen name="Auth" component={AuthScreen} />}
        {isAuthenticated && !isProfileComplete && (
          <stack.Screen name="Onboarding">
            {() => <OnboardingScreen token={token} onCompleted={onProfileCompleted} />}
          </stack.Screen>
        )}
        {isAuthenticated && isProfileComplete && (
          <stack.Screen name="Home">
            {() => (
              <View style={{ flex: 1 }}>
                <Button title="Cikis Yap" onPress={() => signOut(firebaseAuth)} />
                <MainTabs token={token} />
              </View>
            )}
          </stack.Screen>
        )}
      </stack.Navigator>
    </NavigationContainer>
  );
}
