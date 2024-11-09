function getColorsByFengshui(fengshui) {
    switch (fengshui) {
        case 'Mệnh Thủy':
            return ['Xanh', 'Đen'];
        case 'Mệnh Hỏa':
            return ['Đỏ', 'Hồng', 'Cam', 'Tím'];
        case 'Mệnh Mộc':
            return ['Xanh lá cây', 'Nâu'];
        case 'Mệnh Kim':
            return ['Trắng', 'Vàng'];
        case 'Mệnh Thổ':
            return ['Nâu', 'Vàng'];
        default:
            return [];
    }
}

function getVehicleTypesByOccupation(occupation) {
    switch (occupation) {
        case 'Kỹ sư xây dựng':
            return ['SUV', 'Bán tải'];
        case 'Kế toán':
            return ['Sedan'];
        default:
            return [];
    }
}

//let userFengshui = "{{ fengshui | safe }}";
//let userOccupation = "{{ occupation | safe }}";

console.log(userFengshui, userOccupation)

let matchingColors = getColorsByFengshui(userFengshui);
let matchingTypes = getVehicleTypesByOccupation(userOccupation);

const vehicles = document.querySelectorAll('.vehicle-tile');
let filteredVehicles = [];

vehicles.forEach(vehicle => {
    const color = vehicle.querySelector('.vehicle-color').innerText.split(': ')[1];
    const type = vehicle.querySelector('.vehicle-type').innerText.split(': ')[1];
    if (matchingColors.some(c => color.includes(c)) && matchingTypes.includes(type)) {
        filteredVehicles.push(vehicle);
    }
});
// Đầu ra của thuật toán: filteredVehicles.

const suggestedList = document.querySelector('.suggested-vehicle-list');
// Khởi tạo suggestedList để hiển thị lên HTML

suggestedList.innerHTML = '';
// Xóa danh sách cũ mỗi lần tái tạo lại danh sách gợi ý.

filteredVehicles.forEach(vehicle => {
    suggestedList.appendChild(vehicle.cloneNode(true));
});
// Truyền danh sách từ filteredVehicles (đầu ra thuật toán)
// vào suggestedList (trên màn hình)


function toggleChatWindow() {
    var chatWindow = document.getElementById("chatWindow");
    // Toggle the visibility of the chat window
    if (chatWindow.style.display === "none" || chatWindow.style.display === "") {
        chatWindow.style.display = "flex";
    } else {
        chatWindow.style.display = "none";
    }
}

const section = document.getElementById("vehicle-grid");

// Lấy tất cả các thẻ div với class "my-class"
const divElements = section.querySelectorAll("div.vehicle-tile");

// Đếm số lượng thẻ div
const totalDivs = divElements.length;

// Hiển thị tổng số lượng thẻ div có class "my-class"
document.getElementById("section-title").innerText = "Mua bán ô tô. Tổng: " + totalDivs + " tin.";
