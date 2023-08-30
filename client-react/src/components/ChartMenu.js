import Checkbox from "@mui/material/Checkbox";
import FormControl from "@mui/material/FormControl";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormGroup from "@mui/material/FormGroup";
import FormLabel from "@mui/material/FormLabel";
import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import ThemeColors from "./ThemeColors.js";

const ChartMenu = ({ theme, crypto, model, indicator, setCrypto, setModel, setIndicator }) => {
    const textColor = theme === "dark" ? ThemeColors.grayishBlue : ThemeColors.darkBlue;
    const borderColor = theme === "dark" ? ThemeColors.grayishBlue2 : ThemeColors.darkBlue2;
    const seperateLineColor = theme === "dark" ? ThemeColors.darkBlue2 : ThemeColors.grayishBlue2;
    const placeholderColor = theme === "dark" ? ThemeColors.placeholderDark : ThemeColors.placeholderLight;

    const themeMUI = createTheme({
        components: {
            MuiRadio: {
                variants: [{
                    props: { variant: "theme" },
                    style: {
                        color: borderColor
                    }
                }],
                styleOverrides: {
                    root: {
                        "&.Mui-disabled": {
                            color: placeholderColor,
                            "&+.MuiFormControlLabel-label": {
                                color: placeholderColor
                            }
                        }
                    }
                }
            },
            MuiCheckbox: {
                variants: [{
                    props: { variant: "theme" },
                    style: {
                        color: borderColor
                    }
                }],
                styleOverrides: {
                    root: {
                        "&.Mui-disabled": {
                            color: placeholderColor,
                            "&+.MuiFormControlLabel-label": {
                                color: placeholderColor
                            }
                        }
                    }
                }
            }
        }
    });

    const handleCrypto = (event) => {
        setCrypto(event.target.value);
    };

    const handleModel = (event) => {
        setModel(event.target.value);
    };

    const handleIndicator = (event) => {
        const arrayOfIndicator = [...indicator];
        const indexOfSelected = arrayOfIndicator.indexOf(event.target.value);

        if (arrayOfIndicator.length === 1 && indexOfSelected !== -1) {
            return;
        }

        if (indexOfSelected === -1) {
            arrayOfIndicator.push(event.target.value);
        } else {
            arrayOfIndicator.splice(indexOfSelected, 1);
        }

        setIndicator(arrayOfIndicator);
    };

    return (
        <ThemeProvider theme={themeMUI}>
            <FormControl className="FormControl-1">
                <FormLabel style={{ color: textColor, fontWeight: 600 }}>Crypto</FormLabel>
                <RadioGroup value={crypto} onChange={handleCrypto}>
                    <FormControlLabel
                        value="btcusdt"
                        label="BTCUSDT"
                        control={<Radio variant="theme" />}
                        style={{ color: textColor }}
                    ></FormControlLabel>

                    <FormControlLabel
                        value="ethusdt"
                        label="ETHUSDT"
                        control={<Radio variant="theme" />}
                        style={{ color: textColor }}
                        disabled
                    ></FormControlLabel>
                </RadioGroup>
            </FormControl>

            <div style={{ borderRight: `1px solid ${seperateLineColor}` }}></div>
            <FormControl className="FormControl-2">
                <FormLabel style={{ color: textColor, fontWeight: 600 }}>Model</FormLabel>
                <div style={{ display: "flex" }}>
                    <div style={{ marginRight: "20px" }}>
                        <RadioGroup value={model} onChange={handleModel}>
                            <FormControlLabel
                                value="lstm"
                                label="LSTM"
                                control={<Radio variant="theme" />}
                                style={{ color: textColor }}
                            ></FormControlLabel>

                            <FormControlLabel
                                value="transte"
                                label="TransTE"
                                control={<Radio variant="theme" />}
                                style={{ color: textColor }}
                            ></FormControlLabel>
                        </RadioGroup>
                    </div>

                    <div>
                        <RadioGroup value={model} onChange={handleModel}>
                            <FormControlLabel
                                value="rnn"
                                label="RNN"
                                control={<Radio variant="theme" />}
                                style={{ color: textColor }}
                            ></FormControlLabel>

                            <FormControlLabel
                                value="xgboost"
                                label="XGBoost"
                                control={<Radio variant="theme" />}
                                style={{ color: textColor }}
                            ></FormControlLabel>
                        </RadioGroup>
                    </div>
                </div>
            </FormControl>

            <div style={{ borderRight: `1px solid ${seperateLineColor}` }}></div>
            <FormControl className="FormControl-3">
                <FormLabel style={{ color: textColor, fontWeight: 600 }}>Indicator</FormLabel>
                <div style={{ display: "flex" }}>
                    <div style={{ marginRight: "20px" }}>
                        <FormGroup>
                            <FormControlLabel
                                onChange={handleIndicator}
                                value="bb"
                                label="Bollinger Bands"
                                control={
                                    <Checkbox
                                        disabled={indicator.length === 1 && indicator.includes("bb")}
                                        variant="theme"
                                        defaultChecked
                                    ></Checkbox>
                                }
                                style={{ color: textColor }}
                            ></FormControlLabel>

                            <FormControlLabel
                                onChange={handleIndicator}
                                value="rsi"
                                label="Relative Strength Index"
                                control={
                                    <Checkbox
                                        disabled={indicator.length === 1 && indicator.includes("rsi")}
                                        variant="theme"
                                    ></Checkbox>
                                }
                                style={{ color: textColor }}
                            ></FormControlLabel>
                        </FormGroup>
                    </div>

                    <div style={{ marginRight: "20px" }}>
                        <FormGroup>
                            <FormControlLabel
                                onChange={handleIndicator}
                                value="close"
                                label="Closing Price Prediction"
                                control={
                                    <Checkbox
                                        disabled={indicator.length === 1 && indicator.includes("close")}
                                        variant="theme"
                                    ></Checkbox>
                                }
                                style={{ color: textColor }}
                            ></FormControlLabel>

                            <FormControlLabel
                                onChange={handleIndicator}
                                value="sma"
                                label="Simple Moving Average"
                                control={
                                    <Checkbox
                                        disabled={indicator.length === 1 && indicator.includes("sma")}
                                        variant="theme"
                                    ></Checkbox>
                                }
                                style={{ color: textColor }}
                            ></FormControlLabel>
                        </FormGroup>
                    </div>

                    <div style={{ marginRight: "20px" }}>
                        <FormGroup>
                            <FormControlLabel
                                onChange={handleIndicator}
                                value="macd"
                                label="Moving Average Convergence Divergence"
                                control={
                                    <Checkbox
                                        disabled={indicator.length === 1 && indicator.includes("macd")}
                                        variant="theme"
                                    ></Checkbox>
                                }
                                style={{ color: textColor }}
                            ></FormControlLabel>

                            <FormControlLabel
                                onChange={handleIndicator}
                                value="sd"
                                label="Standard Deviation"
                                control={
                                    <Checkbox
                                        disabled={indicator.length === 1 && indicator.includes("sd")}
                                        variant="theme"
                                    ></Checkbox>
                                }
                                style={{ color: textColor }}
                            ></FormControlLabel>
                        </FormGroup>
                    </div>

                    <div>
                        <FormGroup>
                            <FormControlLabel
                                onChange={handleIndicator}
                                value="roc"
                                label="Price Rate of Change"
                                control={
                                    <Checkbox
                                        disabled={indicator.length === 1 && indicator.includes("roc")}
                                        variant="theme"
                                    ></Checkbox>
                                }
                                style={{ color: textColor }}
                            ></FormControlLabel>
                        </FormGroup>
                    </div>
                </div>
            </FormControl>
        </ThemeProvider>
    );
};

export default ChartMenu;