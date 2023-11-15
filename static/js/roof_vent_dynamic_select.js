let duct_type_select = document.getElementById("duct_type");
let diameter_select = document.getElementById("diameter");
let load_select = document.getElementById("load");
let space_select = document.getElementById("space");
//---------------------преднастройка______________
let duct_type = duct_type_select.value;
let load = load_select.value;

let diameter = fetch('/support_system/roof_vent/' + duct_type + '/diameter')
.then(response => response.json())
.then(data => {
    let optionHTML = '';
    for (let diameter of data.diameters) {
        optionHTML += '<option value="' + diameter.name + '">' + diameter.name + '</option>';
    }
    diameter_select = document.getElementById("diameter");
    diameter_select.innerHTML = optionHTML;
    diameter = diameter_select.value;
    console.log(`напр ${duct_type} /${diameter}/${load}`)

    fetch('/support_system/roof_vent/' + duct_type + '/' + diameter + '/' + load + '/height')
    .then(response => response.json())
    .then(data => {
        let optionHTML1 = '';
        for (let height of data.heights) {
            optionHTML1 += '<option value="' + height.name + '">' + height.name + '</option>';
        }
        space_select.innerHTML = optionHTML1;
        space = space_select.value;
        console.log(`напр ${duct_type} /${diameter}/${load}/${space} `)
       })
    })

//---------------------AUTO CHANGE OF DIAMETER______________

 duct_type_select.onchange = function()  {
    duct_type = duct_type_select.value;
    fetch('/support_system/roof_vent/' + duct_type + '/diameter')
    .then(response => response.json())
    .then(function(data) {
        let optionHTML = '';
        for (let diameter of data.diameters) {
        optionHTML += '<option value="' + diameter.name + '">' + diameter.name + '</option>';
        }
        diameter_select = document.getElementById("diameter");
        diameter_select.innerHTML = optionHTML;
        diameter = diameter_select.value;
        console.log(`после смены сечения ${duct_type}/ ${diameter}/${load}`)

//        fetch('/support_system/roof_vent/' + duct_type + '/' + diameter + '/' + load + '/height')
//        .then(response => response.json())
//        .then(function(data) {
//        let optionHTML1 = '';
//        for (let height of data.heights) {
//            optionHTML1 += '<option value="' + height.name + '">' + height.name + '</option>';
//        }
//        space_select.innerHTML = optionHTML1;
//        space = space_select.value;
//        console.log(`после смены сечения ${duct_type} /${diameter}/${load}/${space} `)
//       })
     })
 }

//---------------------AUTO CHANGE OF HEIGHT depend on diameter______________
diameter_select.onchange = function()  {
    diameter = diameter_select.value;
//    load = load_select.value;
    console.log(duct_type, diameter, load);
    fetch('/support_system/roof_vent/' + duct_type + '/' + diameter + '/' + load + '/height')
    .then(response => response.json())
    .then(function(data) {
        let optionHTML2 = '';
        for (let height of data.heights) {
            optionHTML2 += '<option value="' + height.name + '">' + height.name + '</option>';
        }
        space_select.innerHTML = optionHTML2;
        space = space_select.value;
        console.log(`после смены диаметра ${duct_type} /${diameter}/${load}/${space} `);
    })
}
 //---------------------AUTO CHANGE OF HEIGHT______________

 load_select.onchange = function()  {
    duct_type = duct_type_select.value;
    diameter = diameter_select.value;
    load = load_select.value;
    console.log(duct_type, diameter, load);

    fetch('/support_system/roof_vent/' + duct_type + '/' + diameter + '/' + load + '/height')
    .then(response => response.json())
    .then(function(data) {
        let optionHTML3 = '';
        for (let height of data.heights) {
            optionHTML3 += '<option value="' + height.name + '">' + height.name + '</option>';
        }
        space_select.innerHTML = optionHTML3;
        space = space_select.value;
        console.log(`после смены нагрузки ${duct_type} /${diameter}/${load}/${space} `);
    })
}


