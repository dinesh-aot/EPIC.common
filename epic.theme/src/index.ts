import "./fonts.css";

declare module "@mui/material/Button" {
  interface ButtonPropsVariantOverrides {
    dashed: true;
  }
}

export { BCDesignTokens } from "./designTokens";

export { EAOColors } from "./eaoColors";

export { default as createAppTheme } from "./theme";
