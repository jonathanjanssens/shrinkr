<?php

class Easylist
{

    public $easylistBlock;
    public $easylistHide;

    function __construct()
    {
        $this->easylistBlock = file(APP_PATH . '/misc/easylist_general_block.txt');
        $this->easylistHide = file(APP_PATH . '/misc/easylist_general_hide.txt');
    }

    function updateFilters()
    {

    }

}