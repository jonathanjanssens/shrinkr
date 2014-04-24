window.onload = function(){

    var showMenu = document.getElementById('show-shrinkr-menu');
        
    showMenu.onclick = function() {
        var menu = document.getElementById('shrinkr-menu');
        if(menu.style['display'] == 'block') {
            menu.style['display'] = 'none';
        } 
        else {
            menu.style['display'] = 'block';
        }
        return false;
    };

};