function openNav() {
    document.getElementById("mySidenav").style.width = "300px";
}
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

function setEnabled() {
    
    let regno = document.getElementById("regno") ;
    let year = document.getElementById("year");
    let branch = document.getElementById("branch");
    let block = document.getElementById("block");


    if(document.getElementById('regCheck').checked == true){
        regno.disabled = false;
        document.getElementById('blockCheck').checked = false;
        block.disabled = true;

    }else{
        regno.disabled = true;
    }

    if(document.getElementById('blockCheck').checked == true){
        block.disabled = false;
    }else{
        block.disabled= true;
    }

}