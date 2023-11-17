let base_material_select = document.getElementById("base_material");
let dir_select = document.getElementById("direction_type");
let support_diameter_select = document.getElementById("diameter");

let base_material = base_material_select.value;
let direction_type = dir_select.value;

//_______________CHANGE_FUNCTIONS_______________
let direction = fetch('/support_system/sprinkler/' + base_material + '/' + direction_type + '/support_diameter')
.then(response => response.json())
.then(data => {
    let optionHTML = '';
    for (let diameter of data.support_diameters) {
        optionHTML += '<option value="' + diameter.name + '">' + diameter.name + '</option>';
    }
    support_diameter_select.innerHTML = optionHTML;
    support_diameter = support_diameter_select.value;
    console.log(`напр ${base_material} /${direction_type}/${support_diameter} `)
});

//---------------------AUTO CHANGE OF DIAMETERS______________
base_material_select.onchange = function()  {
base_material = base_material_select.value
fetch('/support_system/sprinkler/' + base_material + '/' + direction_type + '/support_diameter')
.then(response => response.json())
.then(data => {
    let optionHTML = '';
    for (let diameter of data.support_diameters) {
        optionHTML += '<option value="' + diameter.name + '">' + diameter.name + '</option>';
    }
    support_diameter_select.innerHTML = optionHTML;
    support_diameter = support_diameter_select.value;
    console.log(`после смены базового материала ${base_material} /${direction_type}/${support_diameter} `)
});
}
