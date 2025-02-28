export function toggleSidebar() {
    let sidebar = document.getElementById('sidebar');
    let toggleButton = document.getElementById('sidebar-toggle');
    let content = document.querySelector('.content');

    if (!sidebar || !toggleButton || !content) {
        console.error("Sidebar, Toggle 버튼 또는 Content 요소를 찾을 수 없습니다.");
        return;
    }

    if (sidebar.style.transform === "translateX(-250px)" || !sidebar.style.transform) {
        sidebar.style.transform = "translateX(0)";
        toggleButton.style.left = "260px";
        content.style.marginLeft = "270px"; // 메인 페이지 이동
    } else {
        sidebar.style.transform = "translateX(-250px)";
        toggleButton.style.left = "10px";
        content.style.marginLeft = "20px"; // 메인 페이지 왼쪽으로 이동
    }
}


export function toggleMenu(id) {
    let submenu = document.getElementById(id);
    if (submenu) {
        submenu.style.display = submenu.style.display === "block" ? "none" : "block";
    } else {
        console.error(`Element with ID '${id}' not found.`);
    }
}
