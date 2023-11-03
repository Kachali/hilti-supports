let base_material_select = document.getElementById("base_material");
let dir_select = document.getElementById("direction_type");
let mounting_select = document.getElementById("mounting");
let support_type_select = document.getElementById("support_type");
let support_diameter_select = document.getElementById("diameter");
let distance_select = document.getElementById("distance");
let pipe_number_select = document.getElementById("pipe_number");
//let dir_select
//let mounting_select
//let support_type_select
//let support_diameter_select
//let distance_select
//let pipe_number_select
//---------------------преднастройка______________
let base_material = base_material_select.value;
//let direction_type = dir_select.value;
//let mounting = mounting_select.value;
//let support_type = support_type_select.value
//let support_diameter = support_diameter_select.value
//let distance = distance_select.value
//let pipe_number = pipe_number_select.value
//        console.log(`в самом начале ${base_material}, ${direction_type},`)
//		console.log(`в самом начале ${base_material}, ${direction_type}, ${mounting}, ${support_type}, ${support_diameter}, ${distance}, ${pipe_number}`)


//_______________CHANGE_FUNCTIONS_______________
let direction = fetch('/support_system/hot_water/' + base_material + '/direction')
.then(response => response.json())
.then(data => {
    let optionHTML = '';
    for (let direction of data.directions) {
        optionHTML += '<option value="' + direction.name + '">' + direction.name + '</option>';
    }
    dir_select = document.getElementById("direction_type");
    dir_select.innerHTML = optionHTML;
    direction_type = dir_select.value;
    console.log(`напр ${base_material} /${direction_type} `)

    fetch('/support_system/hot_water/' + base_material + '/' + direction_type + '/mounting')
    .then(response => response.json())
    .then(data => {
        let optionHTML1 = '';
        for (let fastening of data.fastenings) {
            optionHTML1 += '<option value="' + fastening.name + '">' + fastening.name + '</option>';
        }
        mounting_select.innerHTML = optionHTML1;
        mounting = mounting_select.value;
        console.log(`напр ${base_material} /${direction_type}/${mounting} `)

        fetch('/support_system/hot_water/' + direction_type + '/'+ mounting + '/support_type')
        .then(response => response.json())
        .then(function(data) {
            let optionHTML2 = '';
            for (let supp of data.support_types) {
                optionHTML2 += '<option value="' + supp.name + '">' + supp.name + '</option>';
            }
            support_type_select.innerHTML = optionHTML2;
            support_type = support_type_select.value;
            console.log(`напр ${base_material} /${direction_type}/${mounting}/${support_type} `)

            fetch('/support_system/hot_water/' + direction_type + '/'+ mounting + '/' + support_type + '/support_diameter')
            .then(response => response.json())
            .then(function(data) {
                let optionHTML3 = '';
               for (let diameter of data.support_diameters) {
                    optionHTML3 += '<option value="' + diameter.name + '">' + diameter.name + '</option>';
                }
                support_diameter_select.innerHTML = optionHTML3;
                support_diameter = support_diameter_select.value;
                console.log(`напр ${base_material} /${direction_type}/${mounting}/${support_type}/${support_diameter} `)

                fetch('/support_system/hot_water/' + direction_type + '/'+ mounting + '/' + support_type + '/' + support_diameter + '/support_distance')
                .then(response => response.json())
                .then(function(data) {
                    let optionHTML4 = '';
                    for (let distance of data.support_distances) {
                        optionHTML4 += '<option value="' + distance.name + '">' + distance.name + '</option>';
                    }
                    distance_select.innerHTML = optionHTML4;
                    support_distance = distance_select.value
                    console.log(`напр ${base_material} /${direction_type}/${mounting}/${support_type}/${support_diameter}/${support_distance} `)


                    fetch('/support_system/hot_water/' + direction_type + '/'+ mounting + '/' + support_type + '/' + support_diameter + '/' + support_distance + '/pipe_number')
                    .then(response => response.json())
                    .then(function(data) {
                        let optionHTML5 = '';

                        for (let num of data.number_of_pipes) {
                            optionHTML5 += '<option value="' + num.name + '">' + num.name + '</option>';
                        }
                        pipe_number_select.innerHTML = optionHTML5;
                        pipe_number = pipe_number_select.value

                        let row = [base_material, direction_type, mounting]
                        console.log(`напр ${base_material} /${direction_type}/${mounting}/${support_type}/${support_diameter}/${support_distance}/${pipe_number} `)
                    })
                    .then(row => {
                    console.log(`после ретерна ${base_material} /${direction_type}/${mounting}/${support_type}/${support_diameter}/${support_distance}/${pipe_number} `)
                    })
                })
            })
         });
    });
})


//---------------------AUTO CHANGE OF DIRECTION______________
        base_material_select.onchange = function()  {
            base_material = base_material_select.value;
            fetch('/support_system/hot_water/' + base_material + '/direction')
            .then(response => response.json())
            .then(function(data) {
                let optionHTML = '';
                for (let direction of data.directions) {
                    optionHTML += '<option value="' + direction.name + '">' + direction.name + '</option>';
                }
                dir_select = document.getElementById("direction_type");
                dir_select.innerHTML = optionHTML;
                direction_type = dir_select.value;
                console.log(`после смены типа разводки ${base_material}, ${direction_type}`)


            fetch('/support_system/hot_water/' + base_material + '/' + direction_type + '/mounting')
            .then(response => response.json())
            .then(function(data) {
                let optionHTML1 = '';
                for (let fastening of data.fastenings) {
                    optionHTML1 += '<option value="' + fastening.name + '">' + fastening.name + '</option>';
                }
                mounting_select.innerHTML = optionHTML1;
                mounting = mounting_select.value;


            fetch('/support_system/hot_water/' + direction_type + '/'+ mounting + '/support_type')
            .then(response => response.json())
            .then(function(data) {
                let optionHTML2 = '';
                for (let supp of data.support_types) {
                    optionHTML2 += '<option value="' + supp.name + '">' + supp.name + '</option>';
                }
                support_type_select.innerHTML = optionHTML2;
                support_type = support_type_select.value;


            fetch('/support_system/hot_water/' + direction_type + '/'+ mounting + '/' + support_type + '/support_diameter')
            .then(response => response.json())
            .then(function(data) {
                let optionHTML3 = '';
               for (let diameter of data.support_diameters) {
                    optionHTML3 += '<option value="' + diameter.name + '">' + diameter.name + '</option>';
                }
                support_diameter_select.innerHTML = optionHTML3;
                support_diameter = support_diameter_select.value;


            fetch('/support_system/hot_water/' + direction_type + '/'+ mounting + '/' + support_type + '/' + support_diameter + '/support_distance')
            .then(response => response.json())
            .then(function(data) {
                let optionHTML4 = '';
                for (let distance of data.support_distances) {
                    optionHTML4 += '<option value="' + distance.name + '">' + distance.name + '</option>';
                }
                distance_select.innerHTML = optionHTML4;
                support_distance = distance_select.value


            fetch('/support_system/hot_water/' + direction_type + '/'+ mounting + '/' + support_type + '/' + support_diameter + '/' + support_distance + '/pipe_number')
            .then(response => response.json())
            .then(function(data) {
                let optionHTML5 = '';

                for (let num of data.number_of_pipes) {
                    optionHTML5 += '<option value="' + num.name + '">' + num.name + '</option>';
                }
                pipe_number_select.innerHTML = optionHTML5;
                pipe_number = pipe_number_select.value
                console.log(`При смене базового материала ${base_material}, ${direction_type}, ${mounting}, ${support_type}, ${support_diameter}, ${support_distance}, ${pipe_number}`)
                        });
                    });
                });
            });
        });
    });
};

//---------------------AUTO CHANGE OF FASTENING CONSTRUCTION______________
        dir_select.onchange = function() {
            direction_type = dir_select.value;
            fetch('/support_system/hot_water/' + base_material + '/' + direction_type + '/mounting')
            .then(response => response.json())
            .then(function(data) {
                let optionHTML1 = '';

                for (let fastening of data.fastenings) {
                    optionHTML1 += '<option value="' + fastening.name + '">' + fastening.name + '</option>';
                }
                mounting_select.innerHTML = optionHTML1;
                mounting = mounting_select.value;
                });
                console.log(`после смены типа разводки ${direction_type}, ${mounting}`)

                fetch('/support_system/hot_water/' + direction_type + '/'+ mounting + '/support_type')
            .then(response => response.json())
            .then(function(data) {
                let optionHTML2 = '';
                for (let supp of data.support_types) {
                    optionHTML2 += '<option value="' + supp.name + '">' + supp.name + '</option>';
                }
                support_type_select.innerHTML = optionHTML2;
                support_type = support_type_select.value;


            fetch('/support_system/hot_water/' + direction_type + '/'+ mounting + '/' + support_type + '/support_diameter')
            .then(response => response.json())
            .then(function(data) {
                let optionHTML3 = '';
               for (let diameter of data.support_diameters) {
                    optionHTML3 += '<option value="' + diameter.name + '">' + diameter.name + '</option>';
                }
                support_diameter_select.innerHTML = optionHTML3;
                support_diameter = support_diameter_select.value;


            fetch('/support_system/hot_water/' + direction_type + '/'+ mounting + '/' + support_type + '/' + support_diameter + '/support_distance')
            .then(response => response.json())
            .then(function(data) {
                let optionHTML4 = '';
                for (let distance of data.support_distances) {
                    optionHTML4 += '<option value="' + distance.name + '">' + distance.name + '</option>';
                }
                distance_select.innerHTML = optionHTML4;
                support_distance = distance_select.value


            fetch('/support_system/hot_water/' + direction_type + '/'+ mounting + '/' + support_type + '/' + support_diameter + '/' + support_distance + '/pipe_number')
            .then(response => response.json())
            .then(function(data) {
                let optionHTML5 = '';

                for (let num of data.number_of_pipes) {
                    optionHTML5 += '<option value="' + num.name + '">' + num.name + '</option>';
                }
                pipe_number_select.innerHTML = optionHTML5;
                pipe_number = pipe_number_select.value
                console.log(`При смене типа разводки ${base_material}, ${direction_type}, ${mounting}, ${support_type}, ${support_diameter}, ${support_distance}, ${pipe_number}`)
                        });
                    });
                });
            });
        }

//---------------------AUTO CHANGE OF SUPPORT TYPE______________
            mounting_select.onchange = function()  {
                fetch('/support_system/hot_water/' + direction_type + '/'+ mounting + '/support_type')
                .then(response => response.json())
                .then(function(data) {
                    let optionHTML2 = '';
                    for (let supp of data.support_types) {
                        optionHTML2 += '<option value="' + supp.name + '">' + supp.name + '</option>';
                    }
                    support_type_select.innerHTML = optionHTML2;
                    support_type = support_type_select.value

                fetch('/support_system/hot_water/' + direction_type + '/'+ mounting + '/' + support_type + '/support_diameter')
                .then(response => response.json())
                .then(function(data) {
                let optionHTML3 = '';
               for (let diameter of data.support_diameters) {
                    optionHTML3 += '<option value="' + diameter.name + '">' + diameter.name + '</option>';
                }
                support_diameter_select.innerHTML = optionHTML3;
                support_diameter = support_diameter_select.value;


            fetch('/support_system/hot_water/' + direction_type + '/'+ mounting + '/' + support_type + '/' + support_diameter + '/support_distance')
            .then(response => response.json())
            .then(function(data) {
                let optionHTML4 = '';
                for (let distance of data.support_distances) {
                    optionHTML4 += '<option value="' + distance.name + '">' + distance.name + '</option>';
                }
                distance_select.innerHTML = optionHTML4;
                support_distance = distance_select.value


            fetch('/support_system/hot_water/' + direction_type + '/'+ mounting + '/' + support_type + '/' + support_diameter + '/' + support_distance + '/pipe_number')
            .then(response => response.json())
            .then(function(data) {
                let optionHTML5 = '';

                for (let num of data.number_of_pipes) {
                    optionHTML5 += '<option value="' + num.name + '">' + num.name + '</option>';
                }
                pipe_number_select.innerHTML = optionHTML5;
                pipe_number = pipe_number_select.value
                console.log(`При смене крепления ${base_material}, ${direction_type}, ${mounting}, ${support_type}, ${support_diameter}, ${support_distance}, ${pipe_number}`)
                        });
                    });
                });
                });
        }
//---------------------AUTO CHANGE OF DIAMETERS______________
         support_type_select.onchange = function()  {
                support_type = support_type_select.value
                console.log('Support type = ' + support_type)
//                alert(support_type);

            fetch('/support_system/hot_water/' + direction_type + '/'+ mounting + '/' + support_type + '/support_diameter')
            .then(response => response.json())
            .then(function(data) {
                    let optionHTML3 = '';

                    for (let diameter of data.support_diameters) {
                        optionHTML3 += '<option value="' + diameter.name + '">' + diameter.name + '</option>';
                    }
                    support_diameter_select.innerHTML = optionHTML3;
                    support_diameter = support_diameter_select.value

                    fetch('/support_system/hot_water/' + direction_type + '/'+ mounting + '/' + support_type + '/' + support_diameter + '/support_distance')
            .then(response => response.json())
            .then(function(data) {
                let optionHTML4 = '';
                for (let distance of data.support_distances) {
                    optionHTML4 += '<option value="' + distance.name + '">' + distance.name + '</option>';
                }
                distance_select.innerHTML = optionHTML4;
                support_distance = distance_select.value


            fetch('/support_system/hot_water/' + direction_type + '/'+ mounting + '/' + support_type + '/' + support_diameter + '/' + support_distance + '/pipe_number')
            .then(response => response.json())
            .then(function(data) {
                let optionHTML5 = '';

                for (let num of data.number_of_pipes) {
                    optionHTML5 += '<option value="' + num.name + '">' + num.name + '</option>';
                }
                pipe_number_select.innerHTML = optionHTML5;
                pipe_number = pipe_number_select.value
                console.log(`При смене типа опоры ${base_material}, ${direction_type}, ${mounting}, ${support_type}, ${support_diameter}, ${support_distance}, ${pipe_number}`)
                    });
                });
            });
        }

//---------------------AUTO CHANGE OF DISTANCE______________
         support_diameter_select.onchange = function()  {
                support_diameter = support_diameter_select.value
                console.log('Diameter = ' + support_diameter)
//                alert(support_diameter);

            fetch('/support_system/hot_water/' + direction_type + '/'+ mounting + '/' + support_type + '/' + support_diameter + '/support_distance')
            .then(response => response.json())
            .then(function(data) {
<!--                    console.log(data)-->
<!--                    console.table(data);-->
                    let optionHTML4 = '';

                    for (let distance of data.support_distances) {
                        optionHTML4 += '<option value="' + distance.name + '">' + distance.name + '</option>';
                    }
                    distance_select.innerHTML = optionHTML4;
                    support_distance = distance_select.value

                fetch('/support_system/hot_water/' + direction_type + '/'+ mounting + '/' + support_type + '/' + support_diameter + '/' + support_distance + '/pipe_number')
                .then(response => response.json())
                .then(function(data) {
                let optionHTML5 = '';

                for (let num of data.number_of_pipes) {
                    optionHTML5 += '<option value="' + num.name + '">' + num.name + '</option>';
                }
                pipe_number_select.innerHTML = optionHTML5;
                pipe_number = pipe_number_select.value
                console.log(`При смене диаметра ${base_material}, ${direction_type}, ${mounting}, ${support_type}, ${support_diameter}, ${support_distance}, ${pipe_number}`)
                    });
                });
        }

//--------------------- AUTO CHANGE OF PIPE NUMBER ______________
         distance_select.onchange = function()  {
            support_distance = distance_select.value
            console.log('Distance = ' + support_distance)
            console.log(typeof support_distance)
            fetch('/support_system/hot_water/' + direction_type + '/'+ mounting + '/' + support_type + '/' + support_diameter + '/' + support_distance + '/pipe_number')
            .then(response => response.json())
            .then(function(data) {
<!--                    console.log(data)-->
<!--                    console.table(data);-->
                    let optionHTML5 = '';

                    for (let num of data.number_of_pipes) {
                        optionHTML5 += '<option value="' + num.name + '">' + num.name + '</option>';
                    }
                    pipe_number_select.innerHTML = optionHTML5;
                    pipe_number = pipe_number_select.value
                    console.log(`При смене вылета ${base_material}, ${direction_type}, ${mounting}, ${support_type}, ${support_diameter}, ${support_distance}, ${pipe_number}`)
                });
        }

