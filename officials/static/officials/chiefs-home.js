function openNav() {
    document.getElementById("mySidenav").style.width = "300px";
}
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

function showList1(id) {
    if(id == "absent") {
        document.getElementById("absent-wrapper").style.display = "block";
        document.getElementById("present-wrapper").style.display = "none";
        console.log('clicked absent');
        
    }

    else if(id == "present") {
        document.getElementById("absent-wrapper").style.display = "none";
        document.getElementById("present-wrapper").style.display = "block";
        console.log('clicked present');
    } 
}