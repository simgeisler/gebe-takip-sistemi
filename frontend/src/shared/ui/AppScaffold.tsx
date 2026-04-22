import React, { PropsWithChildren } from "react";
import { SafeAreaView, ScrollView, StyleSheet, View } from "react-native";
import { colors, spacing } from "../../theme/tokens";

interface AppScaffoldProps extends PropsWithChildren {
  isScrollable?: boolean;
}

export function AppScaffold({ children, isScrollable = false }: AppScaffoldProps) {
  if (isScrollable) {
    return (
      <SafeAreaView style={styles.safe}>
        <ScrollView contentContainerStyle={styles.scroll}>{children}</ScrollView>
      </SafeAreaView>
    );
  }
  return (
    <SafeAreaView style={styles.safe}>
      <View style={styles.content}>{children}</View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.surface },
  scroll: { padding: spacing.s4, gap: spacing.s3 },
  content: { flex: 1, padding: spacing.s4, gap: spacing.s3 },
});
