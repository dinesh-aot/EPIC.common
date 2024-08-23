import { Components } from "@mui/material";
import { Palette } from "./palette";
import { color, display, fontWeight, lineHeight, padding } from "@mui/system";
import { BCDesignTokens } from "./designTokens";

const activeBorder = {
  boxShadow: "none",
  outlineOffset: ".125rem",
  outline: `.125rem solid ${BCDesignTokens.surfaceColorBorderActive}`,
};

export const ComponentStyles: Components = {
  MuiAppBar: {
    styleOverrides: {
      root: {
        boxShadow: "0px 4px 8px 0px rgba(0, 0, 0, 0.10)",
      },
    },
  },
  MuiAccordion: {
    styleOverrides: {
      root: {
        boxShadow: "none",
      },
    },
  },
  MuiDialogActions: {
    styleOverrides: {
      root: {
        "&>:not(:first-of-type)": {
          marginLeft: "16px",
        },
      },
    },
  },
  MuiDialog: {
    styleOverrides: {
      paper: ({ ownerState }) => ({
        ...(ownerState.maxWidth === "md" && {
          maxWidth: "680px",
        }),
        ...(ownerState.maxWidth === "lg" && {
          maxWidth: "832px",
        }),
      }),
    },
  },
  MuiButton: {
    styleOverrides: {
      root: ({ ownerState }) => {
        let style = {
          boxShadow: "none",
          fontFamily: "BC Sans",
          padding: "0.5rem 1rem",
        };
        if (ownerState.size === "small") {
          style = {
            ...style,
            ...{ fontSize: "0.875rem", lineHeight: "1rem", height: "2rem" },
          };
        }
        if (ownerState.size === "large") {
          style = {
            ...style,
            ...{ fontSize: "1.125rem", lineHeight: "1.5rem", height: "3rem" },
          };
        }
        if (ownerState.variant === "contained") {
          if (ownerState.color === "primary") {
            style = {
              ...style,
              ...{
                backgroundColor:
                  BCDesignTokens.surfaceColorPrimaryButtonDefault,
                color: BCDesignTokens.typographyColorPrimaryInvert,
                "&:hover": {
                  backgroundColor:
                    BCDesignTokens.surfaceColorPrimaryButtonHover,
                  boxShadow: "none",
                },
                "&:active": {
                  ...activeBorder,
                  backgroundColor:
                    BCDesignTokens.surfaceColorPrimaryButtonDefault,
                },
                "&:disabled": {
                  backgroundColor:
                    BCDesignTokens.surfaceColorPrimaryButtonDisabled,
                  color: BCDesignTokens.typographyColorDisabled,
                },
              },
            };
          } else if (ownerState.color === "secondary") {
            style = {
              ...style,
              ...{
                backgroundColor:
                  BCDesignTokens.surfaceColorSecondaryButtonDefault,
                border: `1px solid ${BCDesignTokens.surfaceColorBorderDark}`,
                padding: "0.438rem 1rem",
                color: BCDesignTokens.typographyColorPrimary,
                "&:hover": {
                  backgroundColor:
                    BCDesignTokens.surfaceColorSecondaryButtonHover,
                  boxShadow: "none",
                },
                "&:active": {
                  ...activeBorder,
                  backgroundColor:
                    BCDesignTokens.surfaceColorSecondaryButtonDefault,
                },
                "&:disabled": {
                  backgroundColor:
                    BCDesignTokens.surfaceColorSecondaryButtonDisabled,
                  color: BCDesignTokens.typographyColorDisabled,
                  borderColor: BCDesignTokens.surfaceColorBorderDefault,
                },
              },
            };
          } else if (ownerState.color === "error") {
            style = {
              ...style,
              ...{
                backgroundColor:
                  BCDesignTokens.surfaceColorPrimaryDangerButtonDefault,
                color: BCDesignTokens.typographyColorPrimaryInvert,
                "&:hover": {
                  backgroundColor:
                    BCDesignTokens.surfaceColorPrimaryDangerButtonHover,
                  boxShadow: "none",
                },
                "&:active": {
                  ...activeBorder,
                  backgroundColor:
                    BCDesignTokens.surfaceColorPrimaryDangerButtonHover,
                },
                "&:disabled": {
                  backgroundColor:
                    BCDesignTokens.surfaceColorPrimaryDangerButtonDisabled,
                  color: BCDesignTokens.typographyColorDisabled,
                },
              },
            };
          }
        } else if (
          ownerState.variant === "outlined" &&
          ownerState.color === "error"
        ) {
          style = {
            ...style,
            ...{
              backgroundColor:
                BCDesignTokens.surfaceColorSecondaryButtonDefault,
              border: `1px solid ${BCDesignTokens.surfaceColorPrimaryDangerButtonDefault}`,
              padding: "0.438rem 1rem",
              color: BCDesignTokens.typographyColorDanger,
              "&:hover": {
                backgroundColor: BCDesignTokens.supportSurfaceColorDanger,
                boxShadow: "none",
              },
              "&:active": {
                ...activeBorder,
                backgroundColor: BCDesignTokens.supportSurfaceColorDanger,
              },
              "&:disabled": {
                backgroundColor:
                  BCDesignTokens.surfaceColorPrimaryDangerButtonDisabled,
                color: BCDesignTokens.typographyColorDisabled,
                borderColor: BCDesignTokens.surfaceColorBorderDefault,
              },
            },
          };
        } else if (ownerState.variant === "text") {
          if (ownerState.color === "primary") {
            style = {
              ...style,
              ...{
                background: BCDesignTokens.surfaceColorTertiaryButtonDefault,
                color: BCDesignTokens.typographyColorPrimary,
                "&:hover": {
                  background: BCDesignTokens.surfaceColorTertiaryButtonHover,
                  boxShadow: "none",
                },
                "&:active": {
                  ...activeBorder,
                  backgroundColor:
                    BCDesignTokens.surfaceColorTertiaryButtonHover,
                },
                "&:disabled": {
                  color: BCDesignTokens.typographyColorDisabled,
                },
              },
            };
          } else if (ownerState.color === "secondary") {
            style = {
              ...style,
              ...{
                backgroundColor: BCDesignTokens.surfaceColorTertiaryButtonHover,
                color: BCDesignTokens.typographyColorLink,
                textDecoration: "underline",
                border: "none",
                "&:active": activeBorder,
                "&:disabled": {
                  color: BCDesignTokens.typographyColorDisabled,
                },
              },
            };
          } else if (ownerState.color === "error") {
            style = {
              ...style,
              ...{
                background: BCDesignTokens.surfaceColorTertiaryButtonHover,
                color: BCDesignTokens.typographyColorDanger,
                "&:hover": {
                  background: BCDesignTokens.supportSurfaceColorDanger,
                  boxShadow: "none",
                },
                "&:active": {
                  ...activeBorder,
                  backgroundColor: BCDesignTokens.supportSurfaceColorDanger,
                },
                "&:disabled": {
                  color: BCDesignTokens.typographyColorDisabled,
                },
              },
            };
          }
        }

        return style;
      },
    },
    defaultProps: {
      variant: "contained",
      color: "primary",
      disableRipple: true,
    },
    variants: [
      {
        props: { variant: "dashed" },
        style: {
          textTransform: "none",
          border: `2px dashed ${Palette.primary.accent.light}`,
        },
      },
    ],
  },
  MuiRadio: {
    defaultProps: {
      disableRipple: true,
    },
    styleOverrides: {
      root: {
        "&.Mui-checked": {
          color: Palette.primary.accent.main,
        },
      },
    },
  },
  MuiInputBase: {
    styleOverrides: {
      root: {
        "&.MuiOutlinedInput-root": {
          backgroundColor: Palette.white,
          "&.Mui-disabled": {
            backgroundColor: Palette.neutral.bg.dark,
          },
          "& fieldset": {
            border: `2px solid ${Palette.neutral.accent.light}`,
          },
          "&:hover fieldset": {
            borderColor: Palette.primary.accent.light,
          },
          "&.Mui-focused fieldset": {
            borderColor: Palette.primary.accent.light,
          },
          "&.Mui-disabled fieldset": {
            borderColor: Palette.neutral.accent.light,
          },
        },
      },
    },
  },
  MuiCheckbox: {
    styleOverrides: {
      root: {
        "&.Mui-disabled svg": {
          fill: `${Palette.neutral.bg.dark} !important`,
        },
      },
    },
  },
  MuiTextField: {
    styleOverrides: {
      root: {
        "& .MuiInputBase-root": {
          fontSize: BCDesignTokens.typographyFontSizeBody,
          color: BCDesignTokens.typographyColorPrimary,
          backgroundColor: BCDesignTokens.surfaceColorFormsDefault,
          backgroundClip: "padding-box",
          border: `1px solid ${BCDesignTokens.surfaceColorBorderDefault}`,
          borderRadius: BCDesignTokens.layoutBorderRadiusMedium,
          boxShadow: "none",
          transition:
            "border-color .15s ease-in-out, box-shadow .15s ease-in-out",
          ":hover": {
            borderColor: BCDesignTokens.surfaceColorBorderDark,
          },
          ":active": {
            ...activeBorder,
            ...{
              borderColor: BCDesignTokens.surfaceColorBorderDark,
            },
          },
          ":focus-within": {
            borderColor: BCDesignTokens.surfaceColorBorderActive,
          },
          ".MuiInputBase-input": {
            padding: "7px 12px",
            height: "24px",
          },
          fieldset: {
            display: "none",
          },
          "MuiInputAdornment-root": {
            color: BCDesignTokens.typographyColorPrimary,
          },
        },
        "& .MuiInputBase-root.MuiInputBase-sizeSmall": {
          height: "2.25rem",
          fontSize: BCDesignTokens.typographyFontSizeSmallBody,
        },
        "& .MuiInputBase-root.Mui-error": {
          borderColor: BCDesignTokens.typographyColorDanger,
        },
        "& .MuiInputBase-root.Mui-disabled": {
          backgroundColor: BCDesignTokens.surfaceColorFormsDisabled,
          outline: "none",
          borderColor: BCDesignTokens.surfaceColorBorderDefault,
        },
        "& .MuiInputLabel-root": {
          position: "static",
          transform: "none",
          fontSize: "0.875rem",
          lineHeight: "1.5rem",
          color: BCDesignTokens.typographyColorSecondary,
        },
        "& .MuiInputLabel-shrink": {
          transform: "none",
        },
        "& .MuiFormHelperText-root": {
          fontSize: "0.875rem",
          color: BCDesignTokens.typographyColorSecondary,
          marginLeft: "0",
        },
        "& .MuiFormHelperText-root.Mui-error": {
          color: BCDesignTokens.typographyColorDanger,
        },
      },
    },
    defaultProps: {
      size: "medium",
    },
  },
  MuiAutocomplete: {
    styleOverrides: {
      root: {
        "& .MuiAutocomplete-inputRoot": {
          padding: "7px 12px",
          ".MuiAutocomplete-input": {
            padding: "0 !important",
          }
        }
      },
    },
  },
  MuiFormControl: {
    styleOverrides: {
      root: {
        marginBottom: "1.5rem",
      },
    },
  },
  MuiLink: {
    defaultProps: {
      color: BCDesignTokens.typographyColorLink,
    },
  },
  MuiIconButton: {
    styleOverrides: {
      root: {
        color: BCDesignTokens.iconsColorPrimary,
      },
    },
  },
  MuiFormLabel: {
    defaultProps: {
      focused: false,
    },
  },
  MuiTooltip: {
    styleOverrides: {
      tooltip: {
        backgroundColor: Palette.neutral.accent.dark,
        color: Palette.white,
        borderRadius: "4px",
        padding: "4px 8px",
        fontSize: "0.75rem",
        maxWidth: "300px",
        margin: "2px",
        overflowWrap: "break-word",
        fontWeight: 400,
        lineHeight: "1rem",
        textAlign: "center",
      },
      tooltipArrow: {
        backgroundColor: Palette.neutral.accent.dark,
      },
    },
  },
  MuiTableCell: {
    styleOverrides: {
      root: {
        fontSize: "1rem",
      },
    },
  },
  MuiCssBaseline: {
    styleOverrides: {
      "*": {
        scrollbarWidth: "thin",
        scrollbarColor: "#B7B7B7 transparent",
        "&::-webkit-scrollbar": {
          width: 6,
          height: 6,
          backgroundColor: "transparent",
        },
        "&::-webkit-scrollbar-track": {
          backgroundColor: "transparent",
        },
        "&::-webkit-scrollbar-thumb": {
          borderRadius: 6,
          backgroundColor: "#B7B7B7",
          minHeight: 24,
          minWidth: 24,
        },
        "&::-webkit-scrollbar-thumb:focus": {
          backgroundColor: "#adadad",
        },
        "&::-webkit-scrollbar-thumb:active": {
          backgroundColor: "#adadad",
        },
        "&::-webkit-scrollbar-thumb:hover": {
          backgroundColor: "#adadad",
        },
        "&::-webkit-scrollbar-corner": {
          backgroundColor: "transparent",
        },
      },
    },
  },
};

export default ComponentStyles;
