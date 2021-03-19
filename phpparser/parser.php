<?php
require __DIR__ . '/vendor/autoload.php';
use PhpParser\ParserFactory;
header('Content-Type: application/json');

$code = "";
if($_GET["mode"] == "inline") {
    $code = $_GET["data"];
} elseif($_GET["mode"] == "file") {
    $code = file_get_contents($_GET["data"]);
}
$parser = (new ParserFactory)->create(ParserFactory::PREFER_PHP7);

try {
    $ast = $parser->parse($code);
    echo json_encode($ast);
} catch  (PhpParser\Error $e) {
    echo $e->getMessage();
}