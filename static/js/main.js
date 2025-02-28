import { toggleSidebar, toggleMenu } from './pages/index.js';

document.addEventListener('DOMContentLoaded', () => {
    // 사이드바 토글 버튼 클릭 시 toggleSidebar 실행
    const sidebarToggleBtn = document.getElementById('sidebar-toggle');
    if (sidebarToggleBtn) {
        sidebarToggleBtn.addEventListener('click', toggleSidebar);
    } else {
        console.error("Sidebar toggle 버튼을 찾을 수 없습니다.");
    }

    // 모든 메뉴 아이템에 이벤트 리스너 추가
    document.querySelectorAll('.menu-item').forEach(item => {
        item.addEventListener('click', () => {
            const targetId = item.getAttribute('onclick')?.match(/'([^']+)'/)?.[1]; // onclick 속성에서 ID 추출
            if (targetId) {
                toggleMenu(targetId);
            }
        });
    });
});
