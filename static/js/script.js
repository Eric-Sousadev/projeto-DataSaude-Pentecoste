// DARK/LIGHT MODE
const root = document.documentElement;
const btn = document.getElementById("themeToggle");

// mantém tema salvo — garante classe exclusiva
const saved = localStorage.getItem("theme");
if (saved === "dark") {
    root.classList.add("dark");
    root.classList.remove("light");
} else if (saved === "light") {
    root.classList.add("light");
    root.classList.remove("dark");
} else {
    // nenhum preferido — mantém estado inicial (presume-se 'light')
    root.classList.add("light");
    root.classList.remove("dark");
}

// adiciona listener só se o botão existir (evita erros em páginas sem nav)
if (btn) {
    btn.addEventListener("click", () => {
        const isDark = root.classList.contains("dark");

        if (isDark) {
            root.classList.remove("dark");
            root.classList.add("light");
            localStorage.setItem("theme", "light");
        } else {
            root.classList.add("dark");
            root.classList.remove("light");
            localStorage.setItem("theme", "dark");
        }
    });
}
