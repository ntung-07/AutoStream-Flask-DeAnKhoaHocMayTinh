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

function getVehicleTypesByGender(gender) {
    switch (gender) {
        case 'Nam':
            return ['SUV', 'Bán tải'];  // Giới tính nam thường chọn các loại xe mạnh mẽ
        case 'Nữ':
            return ['Sedan', 'Hatchback'];  // Giới tính nữ có thể chọn xe nhẹ nhàng hơn
        default:
            return [];
    }
}

function getVehicleTypesByFamilySize(familySize) {
    if (familySize <= 2) {
        return ['Sedan', 'Hatchback'];  // Quy mô gia đình nhỏ có thể chọn sedan hoặc hatchback
    } else {
        return ['SUV', 'Bán tải'];  // Gia đình lớn hơn sẽ thích xe rộng rãi như SUV hoặc bán tải
    }
}

function getSuggestedVehicleTypes(occupation, gender, familySize) {
    // Lấy vehicle types từ nghề nghiệp, giới tính và quy mô gia đình
    let occupationTypes = getVehicleTypesByOccupation(occupation);
    let genderTypes = getVehicleTypesByGender(gender);
    let familySizeTypes = getVehicleTypesByFamilySize(familySize);

    // Kết hợp tất cả các loại xe, ưu tiên nghề nghiệp hơn
    let suggestedTypes = [...new Set([
        ...occupationTypes,
        ...genderTypes,
        ...familySizeTypes
    ])];

    return suggestedTypes;
}

//let userFengshui = "{{ fengshui | safe }}";
//let userOccupation = "{{ occupation | safe }}";
//let userGender = "{{ gender | safe }}";
//let userFamilySize = "{{ family_size | safe }}";

console.log(userFengshui, userOccupation)

let matchingColors = getColorsByFengshui(userFengshui);
let matchingTypes = getSuggestedVehicleTypes(userOccupation, userGender, userFamilySize);

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

// =====================================================================================
// Phần User_window
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
// =====================================================================================