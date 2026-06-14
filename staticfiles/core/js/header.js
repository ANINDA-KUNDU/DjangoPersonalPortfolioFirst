const burger = document.getElementById("ham");
const menu = document.getElementById("menu");

if (burger && menu) {
    burger.addEventListener("click", () => {
        burger.classList.toggle("show");
        menu.classList.toggle("show");
        document.body.classList.toggle("no-scroll");
    });
}