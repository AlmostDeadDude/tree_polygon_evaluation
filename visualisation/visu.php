<?php
@require_once '../web/header.php';
echo '<section class="info-block hero">
<h1>Historical results visualisation</h1>
<p>This dashboard was originally limited to campaign owners. For the Tree Polygon Evaluation demo it is publicly accessible so clients can see how crowdsourced ratings translated into actionable insights.</p>
<div class="demo-actions">
<a class="primary-link" href="../web/index.php">Back to the task demo</a>
</div>
</section>';

echo '<div class="title-wrapper">
<div id="titleString">
<h1>Results visualisation (<span id="actual">NaN</span>/<span id="total">NaN</span> shown)</h1>
<small>(sorted high to low)</small>
</div>
<div id="filter">
<label for="filterMax">Show only scores between:</label>
<div>
<input type="number" id="filterMin" name="filterMin" min="0" max="100" value="0">
<input type="number" id="filterMax" name="filterMax" min="0" max="100" value="100">
</div>
</div>
</div>
<div id="wrapper-container"></div>
<div id="hidden-wrapper" style="display: none;">
';

#iterate through the jobs folder in the web directory and save the contents in an array
$jobs_folder = '../web/jobs';
$jobs = array();
$files = scandir($jobs_folder);
$data = array();

foreach ($files as $file) {
    if (is_dir($file)) {
        continue;
    }
    $handle = fopen($jobs_folder . '/' . $file, "r");
    while (($line = fgets($handle)) !== false) {
        // Skip empty lines
        if (trim($line) === '') {
            echo 'Skipping empty line' . '<br>';
            continue;
        }

        // Parse JSON from each line
        $json_data = json_decode($line, true);
        if ($json_data === null) {
            echo 'Error parsing JSON: ' . json_last_error_msg() . PHP_EOL;
            continue;
        }

        // Append parsed JSON to data array
        $data[] = $json_data;
    }
    fclose($handle);
}
echo '</div>';

#then get the final results from the post_processing folder
$final_results = '../post_processing/final_results.txt';
$final_results_json = '';
if (!file_exists($final_results)) {
    echo '<section class="info-block">
    <h2>Missing aggregated data</h2>
    <p>The file <code>post_processing/final_results.txt</code> was not found, so the visualisation cannot load scores. Please generate it by running the aggregation script.</p>
    </section>';
    @require_once '../web/footer.php';
    exit;
}
$handle = fopen($final_results, "r");
#simply read the json
$final_results_json = fgets($handle);
fclose($handle);
#decode the json
$final_results_array = json_decode($final_results_json, true);

#get the picture name from the final results - it is the key of the top level
$picture_name = array_keys($final_results_array)[0];
#get the picture full path
$picture_path = '../web/' . $picture_name;
#get the picture size
$picture_size = getimagesize($picture_path);
$picture_width = $picture_size[0];
$picture_height = $picture_size[1];

#iterate through the data array and get the points and use them as coordinates to draw on canvas
foreach ($data as $index => $json_obj) {
    #extract data
    $points = $json_obj[0]['points'];
    $number_points = $json_obj[0]['number_points'];
    $ID = $json_obj[0]['ID'];
    #for this id we search for final results
    $avg_score = $final_results_array[$picture_name]['task_' . $ID]["average"];
    $num_scores = count($final_results_array[$picture_name]['task_' . $ID]["scores"]);

    #calculate canvas size
    $canvas_width = $picture_width;
    $canvas_height = $picture_height;

    #draw the canvas
    echo '<div class="canvas-wrapper">';
    echo '<h1>Task #' . $ID . ': <small>' . $number_points . ' points | ' . $num_scores . ' samples | Mean score: <span class="avg" id="avg_' . $ID . '">' . number_format($avg_score, 2) . '</span></small></h1>';
    echo '<canvas id="canvas_' . $ID . '" width="' . $canvas_width . '" height="' . $canvas_height . '" style="border:1px solid #000000; background-image: url(' . $picture_path . ')"></canvas>';
    echo '<script>
    var canvas_' . $ID . ' = document.getElementById("canvas_' . $ID . '");
    var ctx_' . $ID . ' = canvas_' . $ID . '.getContext("2d");
    ctx_' . $ID . '.fillStyle = "rgba(255,255,255,0.1)";
    ctx_' . $ID . '.lineWidth = "5";
    ctx_' . $ID . '.strokeStyle = "black";
    // Draw points and lines on canvas
    ';
    foreach ($points as $i => $point) {
        echo 'var x' . $i . ' = ' . $point['x'] . ';
    var y' . $i . ' = ' . $point['y'] . ';
    ctx_' . $ID . '.arc(x' . $i . ', y' . $i . ', 2, 0, 2 * Math.PI);
    ';
    }
    echo 'ctx_' . $ID . '.fill();
    ';
    echo 'ctx_' . $ID . '.beginPath();
    ctx_' . $ID . '.moveTo(x0, y0);
    ';
    for ($i = 1; $i < count($points); $i++) {
        echo 'ctx_' . $ID . '.lineTo(x' . $i . ', y' . $i . ');
    ';
    }
    echo 'ctx_' . $ID . '.lineTo(x0, y0);
    ctx_' . $ID . '.stroke();
    ctx_' . $ID . '.closePath();
    ';
    echo '</script>';
    echo '</div>';
}
echo '</div>';

@require_once '../web/footer.php';
