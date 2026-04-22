import React from "react";
import { StyleSheet, Text, TouchableOpacity } from "react-native";
import { colors, radius, spacing } from "../../theme/tokens";

interface AppButtonProps {
  title: string;
  onPress: () => void;
  secondary?: boolean;
  disabled?: boolean;
}

export function AppButton({ title, onPress, secondary = false, disabled = false }: AppButtonProps) {
  return (
    <TouchableOpacity
      activeOpacity={0.85}
      disabled={disabled}
      onPress={onPress}
      style={[
        styles.button,
        secondary ? styles.secondary : styles.primary,
        disabled ? styles.disabled : undefined,
      ]}
    >
      <Text style={[styles.text, secondary ? styles.secondaryText : styles.primaryText]}>{title}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: {
    borderRadius: radius.full,
    paddingVertical: spacing.s3,
    paddingHorizontal: spacing.s4,
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 2,
    minHeight: 48,
  },
  primary: { backgroundColor: colors.primary, borderColor: colors.primary },
  secondary: { backgroundColor: colors.primaryPale, borderColor: colors.primary },
  disabled: { opacity: 0.6 },
  text: { fontSize: 15, fontWeight: "600" },
  primaryText: { color: colors.textOnPrimary },
  secondaryText: { color: colors.primary },
});
