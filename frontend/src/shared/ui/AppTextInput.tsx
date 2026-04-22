import React from "react";
import { StyleSheet, TextInput, TextInputProps } from "react-native";
import { colors, radius, spacing } from "../../theme/tokens";

export function AppTextInput(props: TextInputProps) {
  return <TextInput placeholderTextColor={colors.textMuted} style={styles.input} {...props} />;
}

const styles = StyleSheet.create({
  input: {
    borderWidth: 2,
    borderColor: colors.border,
    borderRadius: radius.md,
    backgroundColor: colors.white,
    paddingHorizontal: spacing.s4,
    paddingVertical: spacing.s3,
    color: colors.textPrimary,
  },
});
