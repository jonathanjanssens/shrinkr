<?php

include 'app/bootstrap.php';

$s = new Shrinkr($_GET['url']);

$s->show();