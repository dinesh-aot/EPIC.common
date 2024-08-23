import "./fonts.css";

declare module "@mui/material/Button" {
  interface ButtonPropsVariantOverrides {
    dashed: true;
  }
}

export { BCDesignTokens } from "./designTokens";

export { default as createAppTheme } from "./theme";

export { EAOColors } from "./eaoColors";
