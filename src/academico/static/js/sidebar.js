function changeSidebarState() {
    let sidebar = document.getElementById("page_sidebar_content");
    let main_content = document.getElementById("page_main_content");
    let sidebarState = sidebar.style.display;
    
    if( sidebarState === "" ) {
        let width = window.innerWidth;
        if (width > 768) {
            sidebarState = "block";
        } else {
            sidebarState = "none";
        }
    }

    if (sidebarState === "none") {
        sidebar.style.display = "block";
        main_content.classList.add("col");
        main_content.classList.add("pb-3");
    } else {
        main_content.classList.remove("col");
        main_content.classList.remove("pb-3");
        sidebar.style.display = "none";
    }
}