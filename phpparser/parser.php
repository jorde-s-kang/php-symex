<?php
require __DIR__ . '/vendor/autoload.php';
use PhpParser\ParserFactory;
header('Content-Type: application/json');

$code = "";
if($argv[1] == "inline") {
    $code = $argv[2];
} elseif($argv[1] == "file") {
    $code = file_get_contents($argv[2]);
}
$parser = (new ParserFactory)->create(ParserFactory::PREFER_PHP7);

try {
    $ast = $parser->parse($code);
    echo json_encode($ast);
} catch  (PhpParser\Error $e) {
    echo $e->getMessage();
}
