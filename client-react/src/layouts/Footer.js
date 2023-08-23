import GitHubIcon from "@mui/icons-material/GitHub";
import OndemandVideoIcon from "@mui/icons-material/OndemandVideo";
import { BottomNavigation, BottomNavigationAction } from "@mui/material";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import themeColors from "../components/themeColors.js";
import "../styles.css";

function Footer({ theme }) {
    const color = theme === "dark" ? themeColors.grayishBlue : themeColors.darkBlue;

    const themeMUI = createTheme({
        components: {
            MuiBottomNavigationAction: {
                variants: [{
                    props: { variant: "hover" },
                    style: {
                        color: color,
                        "&:hover": {
                            color: themeColors.vividBlue
                        }
                    }
                }]
            }
        }
    });

    return (
        <>
            <ThemeProvider theme={themeMUI}>
                <BottomNavigation showLabels style={{ background: "transparent" }}>
                    <BottomNavigationAction
                        variant="hover"
                        label="Github"
                        href="/"
                        icon={<GitHubIcon />}
                    ></BottomNavigationAction>

                    <BottomNavigationAction
                        variant="hover"
                        label="Demo"
                        href="/"
                        icon={<OndemandVideoIcon />}
                    ></BottomNavigationAction>
                </BottomNavigation>
            </ThemeProvider>
        </>
    );
};

export default Footer;