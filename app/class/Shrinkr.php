<?php

class Shrinkr {

    private $adBlockFilters;
    private $url;
    private $dom;
    private $xpath;
    private $domElementsToRemove;


    function __construct($url)
    {
        $this->domElementsToRemove = new SplObjectStorage();
        $this->loadAdBlockFilters();
        $this->url = $this->prepareUrl($url);
        $this->loadDom();
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

    function loadDom()
    {
        if($this->url) {
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $this->url);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
            $html = curl_exec($ch);

            $this->dom = new DOMDocument();
            $this->dom->preserveWhiteSpace = false;
            @$this->dom->loadHTML($html);
            $this->xpath = new DOMXPath($this->dom);
        }
    }

    function loadAdBlockFilters()
    {
        $easylist = new Easylist();
        $this->adBlockFilters = array(
            ['block'] = $easylist->easylistBlock,
            ['hide'] = $easylist->easylistHide
        );
    }

    function removeAds()
    {

    }

    function show()
    {
        echo $this->dom->saveHtml();
    }

}