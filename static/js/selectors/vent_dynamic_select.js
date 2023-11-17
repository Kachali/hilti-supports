let base_material_select = document.getElementById("base_material");
let dir_select = document.getElementById("direction_type");
let mounting_select = document.getElementById("mounting");
let duct_type_select = document.getElementById("duct_type");
let support_diameter_select = document.getElementById("diameter");

let base_material = base_material_select.value;

//_______________CHANGE_FUNCTIONS_______________
let direction = fetch('/support_system/ventilation/' + base_material + '/direction')
.then(response => response.json())
.then(data => {
    let optionHTML = '';
    for (let direction of data.directions) {
        optionHTML += '<option value="' + direction.name + '">' + direction.name + '</option>';
    }
    dir_select = document.getElementById("direction_type");
    dir_select.innerHTML = optionHTML;
    direction_type = dir_select.value;
//    console.log(`напр ${base_material} /${direction_type} `)

    fetch('/support_system/ventilation/' + base_material + '/' + direction_type + '/mounting')
    .then(response => response.json())
    .then(data => {
        let optionHTML1 = '';
        for (let fastening of data.fastenings) {
            optionHTML1 += '<option value="' + fastening.name + '">' + fastening.name + '</option>';
        }
        mounting_select.innerHTML = optionHTML1;
        mounting = mounting_select.value;
//        console.log(`напр ${base_material} /${direction_type}/${mounting} `)

        fetch('/support_system/ventilation/' + base_material + '/' + direction_type + '/'+ mounting + '/duct_type')
        .then(response => response.json())
        .then(function(data) {
            let optionHTML2 = '';
            for (let supp of data.duct_types) {
                optionHTML2 += '<option value="' + supp.name + '">' + supp.name + '</option>';
            }
            duct_type_select.innerHTML = optionHTML2;
            duct_type = duct_type_select.value;
//            console.log(`напр ${base_material} /${direction_type}/${mounting}/${duct_type} `)

            fetch('/support_system/ventilation/' + base_material + '/' + direction_type + '/'+ mounting + '/' + duct_type + '/support_diameter')
            .then(response => response.json())
            .then(function(data) {
                let optionHTML3 = '';
               for (let diameter of data.support_diameters) {
                    optionHTML3 += '<option value="' + diameter.name + '">' + diameter.name + '</option>';
                }
                support_diameter_select.innerHTML = optionHTML3;
                support_diameter = support_diameter_select.value;
//                console.log(`напр ${base_material} /${direction_type}/${mounting}/${duct_type}/${support_diameter} `)
            })
         });
    });
})

//---------------------AUTO CHANGE OF DIRECTION______________
    base_material_select.onchange = function()  {
        base_material = base_material_select.value;
        fetch('/support_system/ventilation/' + base_material + '/direction')
        .then(response => response.json())
        .then(function(data) {
            let optionHTML = '';
            for (let direction of data.directions) {
                optionHTML += '<option value="' + direction.name + '">' + direction.name + '</option>';
            }
            dir_select = document.getElementById("direction_type");
            dir_select.innerHTML = optionHTML;
            direction_type = dir_select.value;

        fetch('/support_system/ventilation/' + base_material + '/' + direction_type + '/mounting')
        .then(response => response.json())
        .then(function(data) {
            let optionHTML1 = '';
            for (let fastening of data.fastenings) {
                optionHTML1 += '<option value="' + fastening.name + '">' + fastening.name + '</option>';
            }
            mounting_select.innerHTML = optionHTML1;
            mounting = mounting_select.value;


        fetch('/support_system/ventilation/' + base_material + '/' + direction_type + '/'+ mounting + '/duct_type')
        .then(response => response.json())
        .then(function(data) {
            let optionHTML2 = '';
            for (let supp of data.duct_types) {
                optionHTML2 += '<option value="' + supp.name + '">' + supp.name + '</option>';
            }
            duct_type_select.innerHTML = optionHTML2;
            duct_type = duct_type_select.value;


        fetch('/support_system/ventilation/' + base_material + '/' + direction_type + '/'+ mounting + '/' + duct_type + '/support_diameter')
        .then(response => response.json())
        .then(function(data) {
            let optionHTML3 = '';
           for (let diameter of data.support_diameters) {
                optionHTML3 += '<option value="' + diameter.name + '">' + diameter.name + '</option>';
            }
            support_diameter_select.innerHTML = optionHTML3;
            support_diameter = support_diameter_select.value;
            console.log(`При смене базового материала ${base_material}, ${direction_type}, ${mounting}, ${duct_type}, ${support_diameter}`)

 });
            });
        });
    });
};

//---------------------AUTO CHANGE OF FASTENING CONSTRUCTION______________
dir_select.onchange = function() {
    direction_type = dir_select.value;
    fetch('/support_system/ventilation/' + base_material + '/' + direction_type + '/mounting')
    .then(response => response.json())
    .then(function(data) {
        let optionHTML1 = '';

        for (let fastening of data.fastenings) {
            optionHTML1 += '<option value="' + fastening.name + '">' + fastening.name + '</option>';
        }
        mounting_select.innerHTML = optionHTML1;
        mounting = mounting_select.value;

        fetch('/support_system/ventilation/' + base_material + '/' + direction_type + '/'+ mounting + '/duct_type')
        .then(response => response.json())
        .then(function(data) {
            let optionHTML2 = '';
            for (let supp of data.duct_types) {
                optionHTML2 += '<option value="' + supp.name + '">' + supp.name + '</option>';
            }
            duct_type_select.innerHTML = optionHTML2;
            duct_type = duct_type_select.value;

            fetch('/support_system/ventilation/' + base_material + '/' + direction_type + '/'+ mounting + '/' + duct_type + '/support_diameter')
            .then(response => response.json())
            .then(function(data) {
                let optionHTML3 = '';
               for (let diameter of data.support_diameters) {
                    optionHTML3 += '<option value="' + diameter.name + '">' + diameter.name + '</option>';
                }
                support_diameter_select.innerHTML = optionHTML3;
                support_diameter = support_diameter_select.value;
//                console.log(`после смены типа разводки ${base_material}, ${direction_type}, ${mounting}, ${duct_type}, ${support_diameter}`)

            });
        });
    });
}

//---------------------AUTO CHANGE OF SUPPORT TYPE______________
mounting_select.onchange = function()  {
    mounting = mounting_select.value;
    fetch('/support_system/ventilation/' + base_material + '/' + direction_type + '/'+ mounting + '/duct_type')
    .then(response => response.json())
    .then(function(data) {
        let optionHTML2 = '';
        for (let supp of data.duct_types) {
            optionHTML2 += '<option value="' + supp.name + '">' + supp.name + '</option>';
        }
        duct_type_select.innerHTML = optionHTML2;
        duct_type = duct_type_select.value

        fetch('/support_system/ventilation/' + base_material + '/' + direction_type + '/'+ mounting + '/' + duct_type + '/support_diameter')
        .then(response => response.json())
        .then(function(data) {
        let optionHTML3 = '';
       for (let diameter of data.support_diameters) {
            optionHTML3 += '<option value="' + diameter.name + '">' + diameter.name + '</option>';
        }
        support_diameter_select.innerHTML = optionHTML3;
        support_diameter = support_diameter_select.value;
//        console.log(`после смены конструкции для крепления ${base_material}, ${direction_type}, ${mounting}, ${duct_type}, ${support_diameter}`)

        });
    });
}

//---------------------AUTO CHANGE OF DIAMETERS______________
 duct_type_select.onchange = function()  {
    duct_type = duct_type_select.value
    fetch('/support_system/ventilation/' + base_material + '/' + direction_type + '/'+ mounting + '/' + duct_type + '/support_diameter')
    .then(response => response.json())
    .then(function(data) {
            let optionHTML3 = '';

            for (let diameter of data.support_diameters) {
                optionHTML3 += '<option value="' + diameter.name + '">' + diameter.name + '</option>';
            }
            support_diameter_select.innerHTML = optionHTML3;
            support_diameter = support_diameter_select.value;
    });
}