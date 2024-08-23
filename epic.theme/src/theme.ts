import { createTheme, ThemeOptions, Theme } from "@mui/material/styles";
import { Palette } from "./palette";
import TypographyStyles from "./typography";
import ComponentStyles from "./components";
import { BCDesignTokens } from "./designTokens";

const baseThemeOptions: ThemeOptions = {
  palette: {
    primary: {
      main: BCDesignTokens.themePrimaryBlue,
      light: BCDesignTokens.themeBlue10,
      dark: BCDesignTokens.themeBlue90,
      contrastText: BCDesignTokens.typographyColorPrimaryInvert,
    },
    secondary: {
      main: BCDesignTokens.themePrimaryGold,
      light: BCDesignTokens.themeGold10,
      dark: BCDesignTokens.themeGold90,
      contrastText: BCDesignTokens.typographyColorSecondaryInvert,
    },
    error: {
      main: Palette.error.main,
      dark: Palette.error.dark,
      light: Palette.error.light,
    },
    text: {
      primary: BCDesignTokens.typographyColorPrimary,
      secondary: BCDesignTokens.typographyColorSecondary,
      disabled: BCDesignTokens.typographyColorDisabled,
    },
    background: {
      default: BCDesignTokens.surfaceColorBackgroundWhite,
    },
    common: {
      white: BCDesignTokens.themeGrayWhite,
      black: BCDesignTokens.themeGray110,
    },
  },
  components: ComponentStyles,
  typography: TypographyStyles,
};

const createAppTheme = (customOptions?: ThemeOptions): Theme => {
  return createTheme({
    ...baseThemeOptions,
    ...customOptions,
  });
};

export default createAppTheme;
