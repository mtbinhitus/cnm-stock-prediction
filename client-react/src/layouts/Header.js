import { createContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import SearchIcon from "@mui/icons-material/Search";
import Box from "@mui/material/Box";
import AppBar from "@mui/material/AppBar";
import Button from "@mui/material/Button";
import Toolbar from "@mui/material/Toolbar";
import Container from "@mui/material/Container";
import InputBase from "@mui/material/InputBase";
import { alpha, createTheme, styled, ThemeProvider } from "@mui/material/styles";
import ToggleButton from "../components/ToggleButton.js";
import themeColors from "../components/themeColors.js";
import "../styles.css";

export const ThemeContext = createContext(null);

const Search = styled("div")(({ theme }) => ({
    position: "relative",
    borderRadius: theme.shape.borderRadius,
    backgroundColor: alpha(theme.palette.common.white, 0.15),
    "&:hover": {
        backgroundColor: alpha(theme.palette.common.white, 0.25)
    },
    marginLeft: 0,
    width: "100%",
    [theme.breakpoints.up("sm")]: {
        marginLeft: theme.spacing(1),
        width: "auto"
    }
}));

const SearchIconWrapper = styled("div")(({ theme }) => ({
    padding: theme.spacing(0, 2),
    height: "100%",
    position: "absolute",
    pointerEvents: "none",
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
    color: "inherit",
    "& .MuiInputBase-input": {
        padding: theme.spacing(1, 1, 1, 0),
        paddingLeft: `calc(1em + ${theme.spacing(4)})`,
        transition: theme.transitions.create("width"),
        width: "100%",
        [theme.breakpoints.up("sm")]: {
            width: "20ch",
            "&:focus": {
                width: "30ch"
            }
        }
    }
}));

function Header({ updateTheme, theme, showSearchBar }) {
    const toggleTheme = () => {
        const newTheme = theme === "light" ? "dark" : "light";
        updateTheme(newTheme);
    };

    const borderColor = theme === "dark" ? themeColors.darkBlue2 : themeColors.grayishBlue2;
    const color = theme === "dark" ? themeColors.grayishBlue : themeColors.darkBlue;

    const commonButtonStyle = {
        fontWeight: 600,
        fontSize: 20,
        background: "transparent !important",
        textTransform: "none",
        borderRadius: "0px",
        "&:hover": {
            color: themeColors.vividBlue
        }
    };

    const themeMUI = createTheme({
        components: {
            MuiButton: {
                variants: [{
                    props: { variant: "light" },
                    style: {
                        ...commonButtonStyle,
                        color: themeColors.darkBlue
                    }
                },
                {
                    props: { variant: "dark" },
                    style: {
                        ...commonButtonStyle,
                        color: themeColors.grayishBlue
                    }
                }]
            }
        }
    });

    const [searchQuery, setSearchQuery] = useState("");
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();
        navigate(`/search/${encodeURIComponent(searchQuery)}`);
        setSearchQuery("");
    };

    return (
        <>
            <ThemeContext.Provider value={{ theme, toggleTheme }}>
                <ThemeProvider theme={themeMUI}>
                    <AppBar position="static">
                        <Container maxWidth="xl">
                            <Toolbar disableGutters>
                                <Box sx={{ flexGrow: 1, display: { xs: "none", md: "flex" } }}>
                                    <Button
                                        className="button"
                                        variant={theme}
                                        href="/"
                                    >Market</Button>

                                    <Button
                                        className="button"
                                        variant={theme}
                                        href="/prediction"
                                    >Prediction</Button>
                                </Box>

                                {showSearchBar && <form onSubmit={handleSubmit}>
                                    <Search style={{ background: "transparent", border: `1px solid ${borderColor}`, borderRadius: "0px" }}>
                                        <SearchIconWrapper>
                                            <SearchIcon style={{ color: color }} />
                                        </SearchIconWrapper>

                                        <StyledInputBase
                                            placeholder="BINANCE:BTCUSDT"
                                            style={{ color: color }}
                                            value={searchQuery}
                                            onChange={(e) => setSearchQuery(e.target.value)}
                                        ></StyledInputBase>
                                    </Search>
                                </form>}

                                <ToggleButton
                                    onChange={toggleTheme}
                                    checked={theme === "dark"}
                                ></ToggleButton>
                            </Toolbar>
                        </Container>
                    </AppBar>
                </ThemeProvider>
            </ThemeContext.Provider>
        </>
    );
};

export default Header;