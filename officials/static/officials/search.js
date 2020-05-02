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
        document.getElementById('yearCheck').checked = false;
        document.getElementById('branchCheck').checked = false;
        document.getElementById('blockCheck').checked = false;
        year.disabled = true;
        branch.disabled = true;
        block.disabled = true;

    }else{
        regno.disabled = true;
    }

    if(document.getElementById('yearCheck').checked == true){
        year.disabled = false;
    }else{
        year.disabled = true;
    }

    if(document.getElementById('branchCheck').checked == true){
        branch.disabled = false;
    }else{
        branch.disabled = true;
    }

    if(document.getElementById('blockCheck').checked == true){
        block.disabled = false;
    }else{
        block.disabled= true;
    }

}