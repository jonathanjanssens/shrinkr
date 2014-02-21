<?php

class Shrinkr {

    private $adBlockFilters;
    private $url;

    function __construct($url)
    {
        $this->loadAdBlockFilters();
        $this->url = $this->prepareUrl($url);
    }

    function prepareUrl($url)
    {
        if(substr($url, 0, 4) != 'http') {
            return 'http://' . $url;
        }
        else {
            return $url;
        }
    }

    function loadAdBlockFilters()
    {
        $easylist = new Easylist();
        $this->adBlockFilters = $easylist->loadList();
    }

    function removeAds()
    {

    }

}