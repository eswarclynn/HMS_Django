function openNav() {
    document.getElementById("mySidenav").style.width = "300px";
}
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
  });


function editDetails(id) {
    let element;

    if(id == "phone-icon") {
        element = document.getElementById("phone-field");        
    }
    else if(id == "mail-icon") {
        element = document.getElementById("mail-field");
    }
    else if(id == "address-icon") {
        element = document.getElementById("address-field");
    }

    element.innerHTML = "";
    newElement = document.createElement("input");
    newElement.type = "text";


    element.appendChild(newElement);

    document.getElementById("subbtn").style.display = "contents";

}
