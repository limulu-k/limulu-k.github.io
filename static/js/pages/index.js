export function toggleSidebar() {
    let sidebar = document.getElementById('sidebar');
    let toggleButton = document.getElementById('sidebar-toggle');
    let content = document.querySelector('.content');

    if (!sidebar || !toggleButton || !content) {
        console.error("Sidebar, Toggle 버튼 또는 Content 요소를 찾을 수 없습니다.");
        return;
    }

    let isCollapsed = document.body.classList.contains("sidebar-collapsed");

    if (isCollapsed) {
        sidebar.style.transform = "translateX(0)";
        toggleButton.style.left = "250px";
        content.style.marginLeft = "250px";
        document.body.classList.remove("sidebar-collapsed");
    } else {
        sidebar.style.transform = "translateX(-240px)";
        toggleButton.style.left = "10px";
        content.style.marginLeft = "20px";
        document.body.classList.add("sidebar-collapsed");
    }
}



export function toggleMenu(id) {
    let submenu = document.getElementById(id);
    let menuItem = document.querySelector(`[onclick="toggleMenu('${id}')"]`);
    let arrow = menuItem.querySelector('.arrow');

    if (submenu) {
        let isOpen = submenu.style.maxHeight && submenu.style.maxHeight !== "0px";

        if (isOpen) {
            submenu.style.maxHeight = "0px";  // 닫힘 애니메이션 적용
            arrow.style.transform = "rotate(0deg)";
            setTimeout(() => {
                submenu.style.display = "none";  // 애니메이션 후 display: none; 적용
            }, 300);  // 0.3초 후 실행 (CSS 애니메이션 시간과 동일)
        } else {
            submenu.style.display = "block"; // 먼저 표시
            submenu.style.maxHeight = submenu.scrollHeight + "px";  // 펼쳐짐
            arrow.style.transform = "rotate(180deg)";
        }
    } else {
        console.error(`Element with ID '${id}' not found.`);
    }
}


