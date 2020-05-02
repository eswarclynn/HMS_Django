function openNav() {
    document.getElementById("mySidenav").style.width = "300px";
}
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

function setEnabled() {
    let type = document.getElementById("comp-type").value;
    let regno = document.getElementById("comp-regno") ;
    let summary = document.getElementById("comp-summary");
    let detail = document.getElementById("comp-detail");

    if(type === ""){
        regno.disabled = true;
        summary.disabled = true;
        detail.disabled = true;
    }

    else if(type === "Indisciplinary" || type ==="Discrimination/Harassment" || type ==="Damage to property"){
        regno.disabled = false;
        summary.disabled = false;
        detail.disabled = false;
    }

    else{
        regno.disabled = true;
        summary.disabled = false;
        detail.disabled = false;
    }
}