import Checkbox from "@mui/material/Checkbox";
import FormControl from "@mui/material/FormControl";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormGroup from "@mui/material/FormGroup";
import FormLabel from "@mui/material/FormLabel";
import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import ThemeColors from "./ThemeColors.js";

const ChartMenu = ({ theme, candle, smaCount, crypto, model, indicator, setCandle, setSmaCount, setCrypto, setModel, setIndicator }) => {
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

    const handleSmaCount = (event) => {
        const arrayOfSmaCount = [...smaCount];
        const indexOfSelected = arrayOfSmaCount.indexOf(event.target.value);

        if (indexOfSelected === -1) {
            arrayOfSmaCount.push(event.target.value);
        } else {
            arrayOfSmaCount.splice(indexOfSelected, 1);
        }

        setSmaCount(arrayOfSmaCount);
    };

    const handleCandle = (event) => {
        setCandle(event.target.value);
    };

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
            <div className="menu-1" style={{ display: "flex", justifyContent: "space-between" }}>
                <FormControl id="menu-1-1">
                    <FormLabel style={{ color: textColor, fontWeight: 600 }}>Number of candles</FormLabel>
                    <div style={{ display: "flex" }}>
                        <div>
                            <RadioGroup sx={{ flexWrap: "nowrap" }} row value={candle} onChange={handleCandle}>
                                <div style={{ marginRight: "20px" }}>
                                    <FormControlLabel
                                        id="menu-1-2"
                                        value="250"
                                        label="250 candles"
                                        control={<Radio variant="theme" />}
                                        style={{ color: textColor }}
                                    ></FormControlLabel>
                                </div>

                                <div style={{ marginRight: "20px" }}>
                                    <FormControlLabel
                                        id="menu-1-2"
                                        value="500"
                                        label="500 candles"
                                        control={<Radio variant="theme" />}
                                        style={{ color: textColor }}
                                    ></FormControlLabel>
                                </div>

                                <div style={{ marginRight: "20px" }}>
                                    <FormControlLabel
                                        id="menu-1-2"
                                        value="1000"
                                        label="1000 candles"
                                        control={<Radio variant="theme" />}
                                        style={{ color: textColor }}
                                    ></FormControlLabel>
                                </div>

                                <div>
                                    <FormControlLabel
                                        id="menu-1-2"
                                        value="2000"
                                        label="2000 candles"
                                        control={<Radio variant="theme" />}
                                        style={{ color: textColor }}
                                    ></FormControlLabel>
                                </div>
                            </RadioGroup>
                        </div>
                    </div>
                </FormControl>

                <div style={{ borderRight: `1px solid ${seperateLineColor}` }} />

                <FormControl id="menu-1-1">
                    <FormLabel style={{ color: textColor, fontWeight: 600 }}>Simple moving average</FormLabel>
                    <div style={{ display: "flex" }}>
                        <div style={{ marginRight: "20px" }}>
                            <FormGroup>
                                <FormControlLabel
                                    id="menu-1-2"
                                    onChange={handleSmaCount}
                                    value="5"
                                    label="5 data points"
                                    control={
                                        <Checkbox
                                            variant="theme"
                                            checked={smaCount.includes("5")}
                                        ></Checkbox>
                                    }
                                    style={{ color: textColor }}
                                ></FormControlLabel>
                            </FormGroup>
                        </div>

                        <div style={{ marginRight: "20px" }}>
                            <FormGroup>
                                <FormControlLabel
                                    id="menu-1-2"
                                    onChange={handleSmaCount}
                                    value="10"
                                    label="10 data points"
                                    control={
                                        <Checkbox
                                            variant="theme"
                                            checked={smaCount.includes("10")}
                                        ></Checkbox>
                                    }
                                    style={{ color: textColor }}
                                ></FormControlLabel>
                            </FormGroup>
                        </div>

                        <div style={{ marginRight: "20px" }}>
                            <FormGroup>
                                <FormControlLabel
                                    id="menu-1-2"
                                    onChange={handleSmaCount}
                                    value="20"
                                    label="20 data points"
                                    control={
                                        <Checkbox
                                            variant="theme"
                                            checked={smaCount.includes("20")}
                                        ></Checkbox>
                                    }
                                    style={{ color: textColor }}
                                ></FormControlLabel>
                            </FormGroup>
                        </div>

                        <div>
                            <FormGroup>
                                <FormControlLabel
                                    id="menu-1-2"
                                    onChange={handleSmaCount}
                                    value="40"
                                    label="40 data points"
                                    control={
                                        <Checkbox
                                            variant="theme"
                                            checked={smaCount.includes("40")}
                                        ></Checkbox>
                                    }
                                    style={{ color: textColor }}
                                ></FormControlLabel>
                            </FormGroup>
                        </div>
                    </div>
                </FormControl>
            </div>

            <div className="menu-2" style={{ display: "flex", justifyContent: "space-between", borderTop: `1px solid ${seperateLineColor}` }}>
                <FormControl id="menu-1-1">
                    <FormLabel style={{ color: textColor, fontWeight: 600 }}>Crypto</FormLabel>
                    <div style={{ display: "flex" }}>
                        <div>
                            <RadioGroup value={crypto} onChange={handleCrypto}>
                                <FormControlLabel
                                    id="menu-1-2"
                                    value="btcusdt"
                                    label="BTCUSDT"
                                    control={<Radio variant="theme" />}
                                    style={{ color: textColor }}
                                ></FormControlLabel>

                                <FormControlLabel
                                    id="menu-1-2"
                                    value="ethusdt"
                                    label="ETHUSDT"
                                    control={<Radio variant="theme" />}
                                    style={{ color: textColor, textDecoration: "line-through" }}
                                    disabled
                                ></FormControlLabel>
                            </RadioGroup>
                        </div>
                    </div>
                </FormControl>

                <div style={{ borderRight: `1px solid ${seperateLineColor}` }} />

                <FormControl id="menu-1-1">
                    <FormLabel style={{ color: textColor, fontWeight: 600 }}>Model</FormLabel>
                    <div style={{ display: "flex" }}>
                        <div style={{ marginRight: "20px" }}>
                            <RadioGroup value={model} onChange={handleModel}>
                                <FormControlLabel
                                    id="menu-1-2"
                                    value="lstm"
                                    label="LSTM"
                                    control={<Radio variant="theme" />}
                                    style={{ color: textColor }}
                                ></FormControlLabel>

                                <FormControlLabel
                                    id="menu-1-2"
                                    value="transte"
                                    label="TransTE"
                                    control={<Radio variant="theme" />}
                                    style={{ color: textColor, textDecoration: "line-through" }}
                                    disabled
                                ></FormControlLabel>
                            </RadioGroup>
                        </div>

                        <div>
                            <RadioGroup value={model} onChange={handleModel}>
                                <FormControlLabel
                                    id="menu-1-2"
                                    value="rnn"
                                    label="RNN"
                                    control={<Radio variant="theme" />}
                                    style={{ color: textColor }}
                                ></FormControlLabel>

                                <FormControlLabel
                                    id="menu-1-2"
                                    value="xgboost"
                                    label="XGBoost"
                                    control={<Radio variant="theme" />}
                                    style={{ color: textColor }}
                                ></FormControlLabel>
                            </RadioGroup>
                        </div>
                    </div>
                </FormControl>

                <div style={{ borderRight: `1px solid ${seperateLineColor}` }} />

                <FormControl id="menu-1-1">
                    <FormLabel style={{ color: textColor, fontWeight: 600 }}>Indicator</FormLabel>
                    <div style={{ display: "flex" }}>
                        <div style={{ marginRight: "20px" }}>
                            <FormGroup>
                                <FormControlLabel
                                    id="menu-1-2"
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
                                    id="menu-1-2"
                                    onChange={handleIndicator}
                                    value="roc"
                                    label="Rate of Change"
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

                        <div style={{ marginRight: "20px" }}>
                            <FormGroup>
                                <FormControlLabel
                                    id="menu-1-2"
                                    onChange={handleIndicator}
                                    value="close"
                                    label="Closing Price"
                                    control={
                                        <Checkbox
                                            disabled={indicator.length === 1 && indicator.includes("close")}
                                            variant="theme"
                                        ></Checkbox>
                                    }
                                    style={{ color: textColor }}
                                ></FormControlLabel>

                                <FormControlLabel
                                    id="menu-1-2"
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
                                    id="menu-1-2"
                                    onChange={handleIndicator}
                                    value="ma"
                                    label="Moving Average"
                                    control={
                                        <Checkbox
                                            disabled={indicator.length === 1 && indicator.includes("ma")}
                                            variant="theme"
                                        ></Checkbox>
                                    }
                                    style={{ color: textColor }}
                                ></FormControlLabel>

                                <FormControlLabel
                                    id="menu-1-2"
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
                                    id="menu-1-2"
                                    onChange={handleIndicator}
                                    value="macd"
                                    label="Moving Average C/D"
                                    control={
                                        <Checkbox
                                            disabled={indicator.length === 1 && indicator.includes("macd")}
                                            variant="theme"
                                        ></Checkbox>
                                    }
                                    style={{ color: textColor }}
                                ></FormControlLabel>

                                <FormControlLabel
                                    id="menu-1-2"
                                    onChange={handleIndicator}
                                    value="ic"
                                    label="Ichimoku Cloud"
                                    control={
                                        <Checkbox
                                            disabled={indicator.length === 1 && indicator.includes("ic")}
                                            variant="theme"
                                        ></Checkbox>
                                    }
                                    style={{ color: textColor, textDecoration: "line-through" }}
                                    disabled
                                ></FormControlLabel>
                            </FormGroup>
                        </div>
                    </div>
                </FormControl>
            </div>
        </ThemeProvider>
    );
};

export default ChartMenu;