// Сценарий для отображения/скрытия выплывающего меню
const menuButton = document.querySelector('.user-buttons');
const menuOverlay = document.querySelector('.menu-overlay');
const menu = document.createElement('div');
menu.className = 'menu';
menu.innerHTML = `
    <ul>
        <li><a href="#">Profile</a></li>
        <li><a href="#">Settings</a></li>
        <li><a href="#">Logout</a></li>
    </ul>
`;

menuButton.addEventListener('click', () => {
    menu.style.display = 'block';
    menuOverlay.style.display = 'block';
});

menuOverlay.addEventListener('click', () => {
    menu.style.display = 'none';
    menuOverlay.style.display = 'none';
});

document.body.appendChild(menu);
