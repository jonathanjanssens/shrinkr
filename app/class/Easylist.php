<?php

class Easylist
{

    public $easylistLocation;

    function __construct()
    {
        $this->easylistLocation = APP_PATH . '/misc/easylist_general_block.txt';
    }

    function loadList()
    {
        return file($this->easylistLocation);
    }

    function updateFilters()
    {

    }

}