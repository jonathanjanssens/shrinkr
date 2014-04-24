window.onload = function(){

    var $ = function( id ) { return document.getElementById( id ); };

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

    var convertBtn = document.getElementById('shrinkr-form-convert');

    convertBtn.onclick = function() {
        var extractorUrl = $('shrinkr-extractor-url').value;
        var urlToExtract = $('shrinkr-url').value;
        if(urlToExtract != '') {
            var url = extractorUrl + urlToExtract;
            window.location.href = url;
            return false;
        }
    }

};