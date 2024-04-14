function show(){
    var popup = document.getElementById("popup");
    popup.style.display = "block";   
}

function hide(){
    var popup = document.getElementById("popup");
    popup.style.display = "none";
}

function show(id){
    if(id == null){
        id = "";
    }
    var popup = document.getElementById("popup"+id);
    popup.style.display = "block";
}

function hide(id){
    if(id == null){
        id = "";
    }
    var popup = document.getElementById("popup"+id);
    popup.style.display = "none";
}

function showEditModal(){
    var popup = document.getElementById("popup");
    popup.style.display = "block";   
}

function hideEditModal(){
    document.getElementById('editModal').style.display = 'none';
}

