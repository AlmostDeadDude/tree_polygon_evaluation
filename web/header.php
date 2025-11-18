<?php
$scriptName = $_SERVER['SCRIPT_NAME'] ?? '';
$isVisualisationContext = stripos($scriptName, '/visualisation/') !== false || stripos($scriptName, '\\visualisation\\') !== false;
$webPrefix = $isVisualisationContext ? '../web/' : '';
$visualisationPrefix = $isVisualisationContext ? '' : '../visualisation/';
$currentPage = basename($scriptName);
if ($currentPage === '') {
    $currentPage = 'index.php';
}
$taskClass = 'nav-link' . ($currentPage === 'index.php' ? ' active' : '');
$aboutClass = 'nav-link' . ($currentPage === 'about.php' ? ' active' : '');
$resultsClass = 'nav-link' . ($currentPage === 'visu.php' ? ' active' : '');

echo <<<HTML
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" integrity="sha512-1ycn6IcaQQ40/MKBW2W4Rhis/DbILU74C1vSrLJxCq57o941Ym01SwNsOMqvEBFlcgUa6xLiPY/NS5R+E6ztJQ==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <script src="https://kit.fontawesome.com/d6065b6a9b.js" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="css/style.css">
    <title>Tree Polygon Evaluation</title>
</head>
<body>
    <header>
        <div class="brand">
            <span>Tree Polygon Evaluation</span>
            <small>Demo version</small>
        </div>
        <nav aria-label="Primary">
            <a class="{$aboutClass}" href="{$webPrefix}about.php">About</a>
            <a class="{$taskClass}" href="{$webPrefix}index.php">Task demo</a>
            <a class="{$resultsClass}" href="{$visualisationPrefix}visu.php">Results</a>
        </nav>
    </header>
    <main>
HTML;
