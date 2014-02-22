<?php

define("APP_PATH", dirname(__FILE__));
define("BASE_URL", "http://shrinkr.loc/?url=");

$classes = scandir(APP_PATH . '/class/');

foreach($classes as $class) {
    if(substr($class, 0, 1) != '.') {
        $includePath = APP_PATH . '/class/' . $class;
        include $includePath;
    }
}