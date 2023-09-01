import "../styles.css";

const ThemeColors = {
    darkBlue: getComputedStyle(document.body).getPropertyValue("--darkBlue"),
    darkBlue2: getComputedStyle(document.body).getPropertyValue("--darkBlue2"),
    grayishBlue: getComputedStyle(document.body).getPropertyValue("--grayishBlue"),
    grayishBlue2: getComputedStyle(document.body).getPropertyValue("--grayishBlue2"),
    white: getComputedStyle(document.body).getPropertyValue("--white"),
    vividBlue: getComputedStyle(document.body).getPropertyValue("--vividBlue"),
    candlePositive: getComputedStyle(document.body).getPropertyValue("--candlePositive"),
    candleNegative: getComputedStyle(document.body).getPropertyValue("--candleNegative"),
    predictionColor: getComputedStyle(document.body).getPropertyValue("--predictionColor"),
    placeholderLight: getComputedStyle(document.body).getPropertyValue("--placeholderLight"),
    placeholderDark: getComputedStyle(document.body).getPropertyValue("--placeholderDark"),
    sma5Color: getComputedStyle(document.body).getPropertyValue("--sma5Color"),
    sma10Color: getComputedStyle(document.body).getPropertyValue("--sma10Color"),
    sma20Color: getComputedStyle(document.body).getPropertyValue("--sma20Color"),
    sma40Color: getComputedStyle(document.body).getPropertyValue("--sma40Color")
};

export default ThemeColors;
